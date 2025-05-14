"""Base memory interface for NEURA."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class Memory(Protocol):
    """Protocol defining the interface for all memory implementations."""
    
    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> str:
        """Add a memory.
        
        Args:
            content: The content to store
            metadata: Optional metadata
            **kwargs: Additional arguments
            
        Returns:
            The ID of the added memory
        """
        ...
    
    def get_memory(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> List[Any]:
        """Retrieve memories.
        
        Args:
            query: The search query
            k: Number of results to return
            filter: Optional metadata filter
            **kwargs: Additional arguments
            
        Returns:
            List of relevant memories
        """
        ...
    
    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """Update a memory.
        
        Args:
            memory_id: The ID of the memory to update
            content: New content
            metadata: New metadata
            **kwargs: Additional arguments
        """
        ...
    
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
        ...
    
    def clear(self) -> None:
        """Clear all memories."""
        ...
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dictionary containing memory statistics
        """
        ...


class BaseMemory(ABC):
    """Base implementation of the Memory protocol."""
    
    @abstractmethod
    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> str:
        """Add a memory.
        
        Args:
            content: The content to store
            metadata: Optional metadata
            **kwargs: Additional arguments
            
        Returns:
            The ID of the added memory
        """
        pass
    
    @abstractmethod
    def get_memory(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> List[Any]:
        """Retrieve memories.
        
        Args:
            query: The search query
            k: Number of results to return
            filter: Optional metadata filter
            **kwargs: Additional arguments
            
        Returns:
            List of relevant memories
        """
        pass
    
    @abstractmethod
    def update_memory(
        self,
        memory_id: str,
        content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> None:
        """Update a memory.
        
        Args:
            memory_id: The ID of the memory to update
            content: New content
            metadata: New metadata
            **kwargs: Additional arguments
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all memories."""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics.
        
        Returns:
            Dictionary containing memory statistics
        """
        pass 