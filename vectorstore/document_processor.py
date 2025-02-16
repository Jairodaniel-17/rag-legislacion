import os

from langchain_community.document_loaders import (
    DirectoryLoader,
    Docx2txtLoader,
    PyMuPDFLoader,
    TextLoader,
)


class DocumentProcessor:
    """Document Processor class to process files in a directory."""

    def __init__(self, path: str):
        """Document Processor class to process files in a directory."""
        self.path = path

    def files_to_texts(self) -> list:
        """Convert files in a directory to text."""
        loaders_config = {
            "*.pdf": PyMuPDFLoader,
            "*.txt": (TextLoader, {"encoding": "utf-8"}),
            "*.docx": Docx2txtLoader,
            "*.doc": Docx2txtLoader,
        }

        loaders = [
            DirectoryLoader(
                path=self.path,
                glob=glob,
                loader_cls=loader if isinstance(loader, type) else loader[0],
                loader_kwargs=loader[1] if isinstance(loader, tuple) else None,
            )
            for glob, loader in loaders_config.items()
            if any(fname.endswith(glob[1:]) for fname in os.listdir(self.path))
        ]

        documents = []
        for loader in loaders:
            documents.extend(loader.load())

        return documents
