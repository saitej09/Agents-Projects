from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field, ConfigDict
from markitdown import MarkItDown
from chonkie import SemanticChunker, SDPMChunker
from qdrant_client import QdrantClient
import os


class DocumentSearchToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    query: str = Field(..., description="Query to search the document")


class DocumentSearchTool(BaseTool):
    name: str = "Document Search Tool"
    description: str = "Performs search on the document based on the query provided"
    args_schema: Type[BaseModel] = DocumentSearchToolInput

    model_config = ConfigDict(extra="allow")

    def __init__(self, doc_file_path: str, db_file_path: str = ":memory:"):

        super().__init__()
        self.doc_file_path = doc_file_path
        self.db_file_path = db_file_path
        self.client = QdrantClient(self.db_file_path)
        self._create_db()

    def _extract_text(self):
        md = MarkItDown()
        res = md.convert(self.doc_file_path)
        return res.text_content

    def _create_chunks(self, text):
        chunker = SemanticChunker(
            embedding_model="minishlab/potion-base-8M",
            mode="window",
            threshold="auto",  # 0.5,
            chunk_size=512,
            min_sentences=1,
        )
        return chunker.chunk(text)

    def _create_db(self):
        raw_text = self._extract_text()
        chunks = self._create_chunks(raw_text)
        docs = [chunk.text for chunk in chunks]
        metadata = [
            {"source": os.path.basename(self.doc_file_path)} for _ in range(len(chunks))
        ]
        ids = list(range(len(chunks)))
        print("Adding collection Agents ..")
        self.client.add(
            collection_name="agents", documents=docs, ids=ids, metadata=metadata
        )

    def _run(self, query: str) -> str:
        # Implementation goes here
        print(f"collections:  {self.client.get_collections()}")
        relevant_chunks = self.client.query(collection_name="agents", query_text=query)
        docs = [chunk.document for chunk in relevant_chunks]
        separator = "\n___\n"
        return separator.join(docs)
