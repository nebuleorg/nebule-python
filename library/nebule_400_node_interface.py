"""
Nebule Node Interface

This module defines the interface for node operations in the nebule library.
It is equivalent to 400_node_interface.php in the PHP version (which doesn't exist, 
but we create it for consistency with the entity/link pattern).
"""

from abc import ABC, abstractmethod


class NodeInterface(ABC):
    """
    Abstract base class for node operations.
    
    Classes implementing this interface provide functionality for managing
    nebule nodes (objects, entities, groups, etc.).
    """
    
    @abstractmethod
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        pass
    
    @abstractmethod
    def node_new(self, type_node, data=''):
        """
        Create a new node.
        
        Args:
            type_node (str): Type of node
            data (str): Node data
            
        Returns:
            str: New node identifier or empty string on failure
        """
        pass
    
    @abstractmethod
    def node_check(self, nid):
        """
        Check if a node exists and is valid.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if node is valid
        """
        pass
    
    @abstractmethod
    def node_read(self, nid):
        """
        Read a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            dict: Node data or empty dict on failure
        """
        pass
    
    @abstractmethod
    def node_write(self, nid, data):
        """
        Write to a node.
        
        Args:
            nid (str): Node identifier
            data (str): Data to write
            
        Returns:
            bool: True if write was successful
        """
        pass
    
    @abstractmethod
    def node_delete(self, nid):
        """
        Delete a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if deletion was successful
        """
        pass
    
    @abstractmethod
    def node_get_type(self, nid):
        """
        Get the type of a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Node type
        """
        pass
