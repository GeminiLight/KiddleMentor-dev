from langchain_core.embeddings import Embeddings
from typing import Optional


class EmbedderFactory:
    @staticmethod
    def create(
        model: str = "sentence-transformers/all-MiniLM-L6-v2",
        model_provider: Optional[str] = "huggingface",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        ) -> Embeddings:
        """Create an embedding model instance based on the specified model name.

        Args:
            model: Model name/identifier
            model_provider: Provider name (huggingface, openai, azure, cohere, ollama, together)
            api_key: Optional API key for providers that require authentication
            api_base: Optional API base URL for custom endpoints

        Returns:
            Embeddings: An instance of the appropriate embeddings class
        """
        if ':' in model:
            model_provider, model = model.split(':', 1)
        else:
            model_provider = model_provider or "huggingface"

        kwargs = {}
        if api_key:
            kwargs['api_key'] = api_key
        if api_base:
            kwargs['base_url'] = api_base

        match model_provider.lower():
            case "huggingface":
                from langchain_huggingface import HuggingFaceEmbeddings
                return HuggingFaceEmbeddings(model_name=model)
            case "openai":
                from langchain_openai import OpenAIEmbeddings
                return OpenAIEmbeddings(model=model, **kwargs)
            case "azure":
                from langchain_openai import AzureOpenAIEmbeddings
                return AzureOpenAIEmbeddings(model=model, **kwargs)
            case "cohere":
                from langchain_cohere import CohereEmbeddings
                return CohereEmbeddings(model=model, **kwargs)
            case "ollama":
                from langchain_ollama import OllamaEmbeddings
                base_url = api_base or "http://localhost:11434"
                return OllamaEmbeddings(model=model, base_url=base_url)
            case "together":
                from langchain_together import TogetherEmbeddings
                return TogetherEmbeddings(model=model, **kwargs)
            case _:
                raise ValueError(f"Unsupported model provider: {model_provider}")


if __name__ == "__main__":
    # Example usage
    embedder = EmbedderFactory.create(
        model="sentence-transformers/all-mpnet-base-v2", 
        model_provider="huggingface")
    text = "Hello, world!"
    embedding = embedder.embed_query(text)
    print(f"Embedding for '{text}': {embedding}")
