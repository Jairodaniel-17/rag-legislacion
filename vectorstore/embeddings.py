from langchain_community.embeddings import OllamaEmbeddings
import warnings

warnings.filterwarnings("ignore")


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
        self.__embeddings = OllamaEmbeddings(model="nomic-embed-text")

    @classmethod
    def get_embeddings(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance.__embeddings
