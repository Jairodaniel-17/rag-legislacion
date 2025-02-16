import os
import warnings

from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings

load_dotenv()
warnings.filterwarnings("ignore")

MODEL_EMBEDDINGS = os.getenv("MODEL_EMBEDDINGS")


class EmbeddingManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EmbeddingManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.__embeddings = OllamaEmbeddings(model=MODEL_EMBEDDINGS)

    @classmethod
    def get_embeddings(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.__embeddings
