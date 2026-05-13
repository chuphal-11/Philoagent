from langchain_text_splitters import RecursiveCharacterTextSplitter

from loguru import logger

Splitter = RecursiveCharacterTextSplitter
def get_splitter(chunk_size:int)->Splitter:
    chunk_overlap=int(0.15*chunk_size)

    return RecursiveCharacterTextSplitter(
        encodding_name="cl100k_base",
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )

