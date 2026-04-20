from app.core.config import get_settings
import ollama

settings = get_settings()


async def generate_embedding(text: str) -> list[float]:
    """
    Generate embeddings for the given text using Ollama embedding model.
    
    Args:
        text: The input text to generate embeddings for
        
    Returns:
        A list of floats representing the embedding vector
    """
    response = ollama.embeddings(
        model=settings.EMBEDDING_MODEL,
        prompt=text
    )
    return response["embedding"]

