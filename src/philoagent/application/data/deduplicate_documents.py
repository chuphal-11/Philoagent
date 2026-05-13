import re 
from typing import List , Tuple
from datasketch import MinHash , MinHashLSH
from langchain_core.documents import Document 
from loguru import logger

from philoagent.config import settings


def deduplicate_documents(documents:List[Document],threshold:float=0.7)->List[Document]:
    """
    remove duplicate documnets based on content similarity using MinHash and LSH based on a specified similarity.

    args:
    documents: list[documnets] to check for deduplicate
    threshold : similarity to consider 
    """
    if not documents:
        logger.warning("No documents provided for deduplication.")
        return []
    
    duplicates = find_duplicates(documents, threshold)
    logger.info(f"Found {len(duplicates)} duplicate pairs.")

    indices_to_remove = set()
    for i,j,_ in duplicates:
        if len(documents[i].page_content)>= len(documents[j].page_content):
            indices_to_remove.add(j)
        else:
            indices_to_remove.add(i)
    return [doc for idx, doc in enumerate(documents) if idx not in indices_to_remove]


def  find_duplicates(documents:List[Document],threshold:float,num_perm:int=int(settings.RAG_CHUNK_SIZE*0.5))->List[Tuple[int,int]]:
    """
    find duplicate documnets based on content similarity using MinHash and LSH based on a specified similarity.

    args:
    documents: list[documnets] to check for deduplicate
    threshold : similarity to consider
    return :
    list of tuple of duplicate documnets indexlist of tuple containing (doc_idx_1,doc_idx_2 ,simmilatity_score)
    for doc pairs that exceed the similarity threshold. 
    """
    minhashes = []
    for doc in documents:
        minhash = MinHash(num_perm=num_perm)
        text = doc.page_content.lower()
        words = re.findall(r'\w+', text)

        for i in range(len(words)-3):
            shingle = " ".join(words[i:i+3])
            minhash.update(shingle.encode("utf-8"))
        minhashes.append(minhash)

    # find similar doc pairs using LSH(local senetitive hashing)
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

    for idx,minhash in enumerate(minhashes):
        lsh.insert(idx, minhash)
    duplicates = []
    for idx ,minhash in enumerate(minhashes):
        similar_docs = lsh.query(minhash)
        similar_docs = [doc for doc in similar_docs if doc != idx]
        for j in similar_docs:
            similarity = minhash.jaccard(minhashes[j])
            if similarity >= threshold:
                pair = tuple(sorted((idx,j)))
                duplicates_info = (*pair,similarity)
                if duplicates_info not in duplicates:
                    duplicates.append(duplicates_info)
    return duplicates

