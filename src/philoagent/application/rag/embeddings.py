from langchain_huggingface import HuggingFaceEmbeddings

EmbeddingModel = HuggingFaceEmbeddings


def get_embedding_model(
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2",
    device: str = "cpu",
) -> EmbeddingModel:
    return get_huggingface_embedding_model(model_id, device)


def get_huggingface_embedding_model(
    model_id: str,
    device: str,
) -> EmbeddingModel:
    return HuggingFaceEmbeddings(model_name=model_id, model_kwargs={"device": device})

