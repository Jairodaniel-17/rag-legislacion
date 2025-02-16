import os
import warnings

from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
warnings.filterwarnings("ignore")

MODEL_EMBEDDINGS = os.getenv("MODEL_EMBEDDINGS")
FLAG_EMBEDDINGS_OLLAMA = int(os.getenv("FLAG_EMBEDDINGS_OLLAMA"))

class EmbeddingManager:
    """Embedding Manager class to manage embeddings."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create a new instance of the EmbeddingManager class."""
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the EmbeddingManager class."""
        if self.__initialized:
            return
        self.__initialized = True
        if FLAG_EMBEDDINGS_OLLAMA == 1:
            self.__embeddings = OllamaEmbeddings(model=MODEL_EMBEDDINGS)
        else:
            self.__embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_EMBEDDINGS,
            encode_kwargs={"normalize_embeddings": True},
            model_kwargs={"device": "cuda"},
        )
    @classmethod
    def get_embeddings(cls):
        """Get the embeddings."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.__embeddings
