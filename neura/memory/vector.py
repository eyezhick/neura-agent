"""Vector memory implementation using ChromaDB."""

from typing import Any, Dict, List, Optional, Union

import chromadb
from chromadb.config import Settings
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import Chroma
from pydantic import BaseModel, Field

from neura.memory.base import BaseMemory


class VectorMemoryConfig(BaseModel):
    """Configuration for vector memory."""
    
    collection_name: str = Field(default="neura_memory")
    persist_directory: str = Field(default="./data/chroma")
    embedding_model: str = Field(default="text-embedding-3-small")
    distance_metric: str = Field(default="cosine")
    metadata_hnsw_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "M": 16,
            "ef_construction": 100,
            "ef_search": 100
        }
    )


class VectorMemory(BaseMemory):
    """Vector-based memory implementation using ChromaDB."""
    
    def __init__(
        self,
        config: Optional[VectorMemoryConfig] = None,
        embedding_function: Optional[OpenAIEmbeddings] = None
    ):
        """Initialize vector memory.
        
        Args:
            config: Memory configuration
            embedding_function: Custom embedding function
        """
        self.config = config or VectorMemoryConfig()
        self.embedding_function = embedding_function or OpenAIEmbeddings(
            model=self.config.embedding_model
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.Client(Settings(
            persist_directory=self.config.persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=self.config.collection_name,
            metadata={"hnsw:space": self.config.distance_metric}
        )
        
        # Initialize vector store
        self.vectorstore = Chroma(
            client=self.client,
            collection_name=self.config.collection_name,
            embedding_function=self.embedding_function
        )
    
    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> str:
        """Add a memory to the vector store.
        
        Args:
            content: The content to store
            metadata: Optional metadata
            **kwargs: Additional arguments
            
        Returns:
            The ID of the added memory
        """
        doc = Document(
            page_content=content,
            metadata=metadata or {}
        )
        
        ids = self.vectorstore.add_documents([doc])
        return ids[0]
    
    def get_memory(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> List[Document]:
        """Retrieve memories similar to the query.
        
        Args:
            query: The search query
            k: Number of results to return
            filter: Optional metadata filter
            **kwargs: Additional arguments
            
        Returns:
            List of relevant documents
        """
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filter,
            **kwargs
        )
    
    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """Update an existing memory.
        
        Args:
            memory_id: The ID of the memory to update
            content: New content
            metadata: New metadata
            **kwargs: Additional arguments
        """
        if content:
            self.collection.update(
                ids=[memory_id],
                documents=[content],
                metadatas=[metadata or {}]
            )
        elif metadata:
            self.collection.update(
                ids=[memory_id],
                metadatas=[metadata]
            )
    
    def delete_memory(
        self,
        memory_id: str,
        **kwargs: Any
    ) -> None:
        """Delete a memory.
        
        Args:
            memory_id: The ID of the memory to delete
            **kwargs: Additional arguments
        """
        self.collection.delete(ids=[memory_id])
    
    def clear(self) -> None:
        """Clear all memories."""
        self.collection.delete(where={})
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dictionary containing memory statistics
        """
        return {
            "count": self.collection.count(),
            "dimensions": self.collection.metadata.get("dimension", 0),
            "distance_metric": self.config.distance_metric
        } 