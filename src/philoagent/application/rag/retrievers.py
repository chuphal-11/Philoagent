from langchain_huggingface import HuggingFaceEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers import (MongoDBAtlasHybridSearchRetriever)

from philoagent.config import settings
from .embeddings import get_embedding_model

Retriver = MongoDBAtlasHybridSearchRetriever

def get_retriever(
        embedding_model_id:str,
        k:int=3,
        device:str="cpu",
        )->Retriver:
    embedding_model=get_embedding_model(embedding_model_id,device)
    return get_hybrid_search_retriever(embedding_model,k)

def get_hybrid_search_retriever(embedding_model, k)->Retriver:
   vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
       connection_string = settings.MONGO_URI,
       embedding_model=embedding_model,
       namespace = f"{settings.MONGO_DB_NAME}.{settings.MONGO_LONG_TERM_MEMORY_COLLECTION}",
       text_key="chunk",
       embedding_key="embedding",
       relevence_score_fn="dotProduct",
   )
   

   retriver = MongoDBAtlasHybridSearchRetriever(
       vectorstore=vectorstore,
       search_index_name="hybrid_search_index",
       top_k=k,
       vector_penalty=50,
       fulltext_penalty=50,
   )
   return retriver

