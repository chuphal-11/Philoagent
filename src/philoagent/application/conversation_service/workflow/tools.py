from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional


class RetrieverInput(BaseModel):
    query: str = Field(description="Search query for philosopher information")


class RetrieverTool(BaseTool):
    """Tool for retrieving philosopher context from knowledge base."""
    
    name: str = "retrieve_philosopher_context"
    description: str = "Search and return information about a specific philosopher. Always use this tool when the user asks you about a philosopher, their works, ideas or historical context."
    args_schema: type[BaseModel] = RetrieverInput
    retriever: Optional[object] = None
    _retriever_initialized: bool = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.retriever = None
        self._retriever_initialized = False
    
    def _init_retriever_lazy(self):
        """Lazily initialize retriever only when needed."""
        if self._retriever_initialized:
            return
        try:
            from philoagent.application.rag.retrievers import get_retriever
            from philoagent.config import settings
            
            self.retriever = get_retriever(
                embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
                k=settings.RAG_TOP_K,
                device=settings.RAG_DEVICE,
            )
        except Exception:
            pass
        finally:
            self._retriever_initialized = True
    
    def _run(self, query: str) -> str:
        """Run the retriever tool."""
        self._init_retriever_lazy()
        if self.retriever is None:
            return "Retriever not initialized"
        try:
            docs = self.retriever.get_relevant_documents(query)
            return "\n---\n".join([doc.page_content for doc in docs]) if docs else "No relevant documents found."
        except Exception as e:
            return f"Error retrieving documents: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async run the retriever tool."""
        self._init_retriever_lazy()
        if self.retriever is None:
            return "Retriever not initialized"
        try:
            if hasattr(self.retriever, 'aget_relevant_documents'):
                docs = await self.retriever.aget_relevant_documents(query)
            else:
                docs = self.retriever.get_relevant_documents(query)
            return "\n---\n".join([doc.page_content for doc in docs]) if docs else "No relevant documents found."
        except Exception as e:
            return f"Error retrieving documents: {str(e)}"


retriever_tool = RetrieverTool()
tools = [retriever_tool]