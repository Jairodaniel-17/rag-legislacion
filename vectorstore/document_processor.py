import os

from langchain_community.document_loaders import (
    DirectoryLoader,
    Docx2txtLoader,
    PyMuPDFLoader,
    TextLoader,
)


class DocumentProcessor:
    def __init__(self, path: str):
        self.path = path

    def files_to_texts(self) -> list:
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
