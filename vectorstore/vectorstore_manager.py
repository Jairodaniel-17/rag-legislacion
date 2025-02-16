import os
import shutil
from typing import List, Optional
from zipfile import ZipFile

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from vectorstore.document_processor import DocumentProcessor
from vectorstore.embeddings import EmbeddingManager


class VectorStoreManager:
    """Clase para gestionar el vectorstore.

    Esta clase maneja la creación, eliminación y búsqueda de documentos similares.

    Métodos:
    - __init__(path: str, name: str, embeddings: Embeddings):
        Inicializa la clase con la ruta del directorio, el nombre del vectorstore
        y el modelo de embeddings.
    - create_vectorstore() -> bool:
        Crea un vectorstore a partir de los documentos en la ruta especificada
        y lo guarda localmente.
    - delete_vectorstore() -> bool:
        Elimina el vectorstore especificado.
    - search_similarity(query: str, fuente: Optional[str] = None) -> str:
        Busca documentos similares en el vectorstore basado en una query
        y una fuente opcional.
    - list_sources() -> List[str]:
        Lista todas las fuentes de los documentos en el vectorstore.
    - extract_texts_by_source(source: str) -> List[str]:
        Extrae los textos de los documentos que pertenecen a una fuente específica.
    - save_text_to_file_temp(source: str) -> bool:
        Guarda los textos de una fuente específica en un archivo temporal.
    - load_vectorstore() -> FAISS:
        Carga el vectorstore desde el almacenamiento local.
    - add_files_vectorstore() -> Optional[FAISS]:
        Añade nuevos documentos al vectorstore y lo guarda localmente.
    - download_vectorstore() -> str:
        Genera un archivo zip del vectorstore y devuelve la ruta del archivo.
    """

    def __init__(self, path: str, name: str):
        """Inicializa el gestor del vectorstore.

        Clase para gestionar el vectorstore, incluyendo la creación,
        eliminación y búsqueda de documentos similares.

        Parámetros:
        - path: str - ruta del directorio que contiene los documentos (usualmente es
        "database" que es el directorio donde se almacenan las bases de datos).
        - name: str - nombre que será el identificador del vectorstore, se
        usa para guardar y cargar el vectorstore.
        """
        self.path = path
        self.name = name
        self.embeddings = EmbeddingManager.get_embeddings()
        self.vectorstore = None

    def create_vectorstore(self) -> bool:
        """Create and save a vector store from documents in the specified path.

        The process includes:
        - Converting files to text documents
        - Splitting texts into chunks with overlap
        - Creating FAISS vector store with embeddings
        - Saving vector store to local database directory

        Retorna True si el vectorstore fue creado y guardado exitosamente.
        """
        documents = DocumentProcessor(self.path).files_to_texts()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(
            documents=texts, embedding=self.embeddings
        )
        base_de_datos_dir = os.path.join("database", self.name)
        self.vectorstore.save_local(folder_path=base_de_datos_dir)
        return True

    def delete_vectorstore(self) -> bool:
        """Delete the specified vector store."""
        try:
            shutil.rmtree(f"database/{self.name}")
        except FileNotFoundError:
            return False
        return True

    def search_similarity(self, query: str, fuente: Optional[str] = None) -> str:
        """Busqueda de similitd en documentos del vectorstore basado en la query.

        Modo de uso:
        debe ingresar la query y la fuente (opcional) para buscar documentos
        similares en el vectorstore.

        Nota: debe estar definido el vectorstore para poder realizar la búsqueda.

        Parámetros:
        query: str - texto de la query.
        fuente: str - fuente de los documentos a buscar, pero es opcional.

        Retorna:
        str - documentos similares.
        """
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()

        if fuente:
            filtro = {"source": fuente}
            retriever = self.vectorstore.similarity_search(
                query=query, k=5, filter=filtro
            )
        else:
            retriever = self.vectorstore.similarity_search(query=query, k=5)
        busqueda = [
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", None),
            }
            for doc in retriever
        ]

        return str(busqueda)

    def list_sources(self) -> List[str]:
        """List all sources of the documents in the vectorstore."""
        if not self.vectorstore:
            self.vectorstore = self.load_vectorstore()

        docstore_dict = self.vectorstore.docstore._dict
        source_metadata = {}
        for doc_id, document in docstore_dict.items():
            source = document.metadata.get("source", None)
            source_metadata[doc_id] = source

        return list(set(source_metadata.values()))

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
        """Save texts of a specific source to a temporary file."""
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

    def load_vectorstore(self) -> FAISS:
        """Load the vectorstore from local storage."""
        return FAISS.load_local(
            folder_path=os.path.join("database", self.name),
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def add_list_files_vectorstore(self, path_files: str) -> bool:
        """Add files to the vectorstore and save it locally."""
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

    def add_files_vectorstore(self) -> Optional[FAISS]:
        """Add new documents to the vectorstore and save it locally."""
        temp_folder = "docs"
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            return None

        documents = DocumentProcessor(temp_folder).files_to_texts()
        if not documents:
            return None

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_documents(documents)
        self.vectorstore = self.load_vectorstore()
        self.vectorstore.add_documents(documents=texts)
        self.vectorstore.save_local(folder_path=os.path.join("database", self.name))
        return self.vectorstore

    def download_vectorstore(self):
        """Generate a zip file of the vectorstore and return the file path."""
        with ZipFile("temp/vectorstore.zip", "w") as zip:
            for root, _dirs, files in os.walk(f"database/{self.name}"):
                for file in files:
                    zip.write(os.path.join(root, file))
        return "temp/vectorstore.zip"

    def exist_vectorstore(self) -> bool:
        """Check if the vectorstore exists in the local storage."""
        return os.path.exists(f"database/{self.name}")
