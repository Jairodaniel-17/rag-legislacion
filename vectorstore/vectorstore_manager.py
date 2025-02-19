import os
import shutil
from typing import Any, List, Optional
from zipfile import ZipFile

import faiss
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS as FAISS_STORE
from langchain_core.documents import Document

from vectorstore.distance_strategy import DistanceStrategyManager
from vectorstore.document_processor import DocumentProcessor
from vectorstore.embeddings import EmbeddingManager


class VectorStoreManager:
    """Clase para gestionar los vectorstore de FAISS."""

    def __init__(self, path: str, name: str):
        """Inicialización de la clase con configuración específica."""
        self.path = path
        self.name = name
        self.embeddings = EmbeddingManager.get_embeddings()
        self.manager_strategy = DistanceStrategyManager()
        self.strategy = self.manager_strategy.strategy
        self.vectorstore = None

        # Inicialización del índice FAISS
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Inicializa el vectorstore con configuración básica."""
        if self.exist_vectorstore():
            self.vectorstore = self.load_vectorstore()
        else:
            # Crear índice base con dimensión correcta
            dummy_embed = self.embeddings.embed_query(
                "Propiedad de Jairo Daniel Mendoza Torres"
            )
            index = faiss.IndexFlatL2(len(dummy_embed))

            self.vectorstore = FAISS_STORE(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
                distance_strategy=self.strategy,
            )

    def create_vectorstore(self) -> bool:
        """Crea y guarda un nuevo vectorstore desde documentos."""
        if self.exist_vectorstore():
            return False

        documents = DocumentProcessor(self.path).files_to_texts()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_documents(documents)

        # Re-inicializar con documentos
        self.vectorstore.add_documents(texts)
        self._save_vectorstore()
        return True

    def delete_vectorstore(self) -> bool:
        """Elimina el vectorstore especificado."""
        try:
            shutil.rmtree(f"database/{self.name}")
            return True
        except FileNotFoundError:
            return False

    def search_similarity(
        self, query: str, k: Optional[int] = 5, fuente: Optional[str] = None
    ) -> str:
        """Búsqueda de similitud con capacidad de filtrado."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()

        filter_dict = {"source": fuente} if fuente else {}

        results = self.vectorstore.similarity_search(query=query, k=k, filter=filter_dict)

        return str(
            [
                {"content": doc.page_content, "source": doc.metadata.get("source")}
                for doc in results
            ]
        )

    def list_sources(self) -> List[str]:
        """Lista todas las fuentes únicas en el vectorstore."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()

        sources = set()
        for doc in self.vectorstore.docstore._dict.values():
            if hasattr(doc, "metadata"):
                sources.add(doc.metadata.get("source", ""))
        return list(sources)

    def _save_vectorstore(self):
        """Guarda el vectorstore en disco."""
        save_path = os.path.join("database", self.name)
        self.vectorstore.save_local(save_path)

    def load_vectorstore(self) -> FAISS_STORE:
        """Carga el vectorstore desde disco."""
        return FAISS_STORE.load_local(
            folder_path=os.path.join("database", self.name),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
            distance_strategy=self.strategy,
        )

    def add_files_vectorstore(self) -> bool:
        """Añade nuevos documentos al vectorstore."""
        temp_folder = "docs"
        if not os.path.exists(temp_folder):
            return False

        documents = DocumentProcessor(temp_folder).files_to_texts()
        if not documents:
            return False

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_documents(documents)

        self.vectorstore.add_documents(texts)
        self._save_vectorstore()
        return True

    def download_vectorstore(self) -> str:
        """Genera un ZIP del vectorstore."""
        zip_path = "temp/vectorstore.zip"
        with ZipFile(zip_path, "w") as zipf:
            for root, _, files in os.walk(f"database/{self.name}"):
                for file in files:
                    zipf.write(os.path.join(root, file))
        return zip_path

    def exist_vectorstore(self) -> bool:
        """Verifica si el vectorstore existe."""
        return os.path.exists(f"database/{self.name}")

    def extract_texts_by_source(self, source: str) -> List[str]:
        """Extract texts of documents that belong to a specific source."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()

        docstore_dict = self.vectorstore.docstore._dict
        texts = []
        for document in docstore_dict.values():
            source_doc = document.metadata.get("source", None)
            if source_doc == source:
                texts.append(document.page_content)
        return texts

    def save_text_to_file_temp(self, source: str) -> bool:
        """Guarda los textos de una fuente en un archivo temporal."""
        texts = self.extract_texts_by_source(source)
        carpeta = "temp"
        target_source_safe = source.replace("\\", "_").replace("/", "_")
        file_path = os.path.join(carpeta, target_source_safe + ".txt")

        try:
            if os.path.exists(carpeta):
                shutil.rmtree(carpeta)
            os.makedirs(carpeta)

            with open(file_path, "w", encoding="utf-8") as file:
                for text in texts:
                    file.write(text)
                    file.write("\n")
            return True
        except Exception:
            return False

    def add_list_files_vectorstore(self, path_files: str) -> bool:
        """Añade documentos de una lista de archivos al vectorstore."""
        if not os.path.exists(path_files):
            return False

        documents = DocumentProcessor(path_files).files_to_texts()
        if not documents:
            return False

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_documents(documents)
        self.vectorstore = self.load_vectorstore()
        self.vectorstore.add_documents(documents=texts)
        self.vectorstore.save_local(folder_path=os.path.join("database", self.name))
        return True

    async def aadd_documents(self, documents: List[Document]) -> None:
        """Versión asíncrona para añadir documentos al vectorstore."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()
        await self.vectorstore.aadd_documents(documents=documents)
        self._save_vectorstore()

    async def asimilarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Versión asíncrona de similarity_search_with_score."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()
        return await self.vectorstore.asimilarity_search_with_score(query=query, k=k)

    def as_retriever(self, search_type: str = "similarity", **kwargs) -> Any:
        """Convierte el vectorstore en un retriever para búsquedas avanzadas."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()
        return self.vectorstore.as_retriever(search_type=search_type, **kwargs)