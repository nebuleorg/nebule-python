"""
Nebule Link Interface

This module defines the interface for link operations in the nebule library.
It is equivalent to 500_link_interface.php in the PHP version.
"""

from abc import ABC, abstractmethod


class LinkInterface(ABC):
    """
    Abstract base class for link operations.
    
    Classes implementing this interface provide functionality for managing
    links between nebule objects and entities.
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
    def link_new(self, source, target, type_link, data=''):
        """
        Create a new link.
        
        Args:
            source (str): Source node identifier
            target (str): Target node identifier
            type_link (str): Type of link
            data (str): Optional link data
            
        Returns:
            str: New link identifier or empty string on failure
        """
        pass
    
    @abstractmethod
    def link_check(self, lid):
        """
        Check if a link exists and is valid.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            bool: True if link is valid
        """
        pass
    
    @abstractmethod
    def link_read(self, lid):
        """
        Read a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            dict: Link data or empty dict on failure
        """
        pass
    
    @abstractmethod
    def link_delete(self, lid):
        """
        Delete a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            bool: True if deletion was successful
        """
        pass
    
    @abstractmethod
    def link_parse(self, link_data):
        """
        Parse a link data string.
        
        Args:
            link_data (str): Raw link data
            
        Returns:
            dict: Parsed link information
        """
        pass
    
    @abstractmethod
    def link_get_source(self, lid):
        """
        Get the source node of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: Source node identifier
        """
        pass
    
    @abstractmethod
    def link_get_target(self, lid):
        """
        Get the target node of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: Target node identifier
        """
        pass
    
    @abstractmethod
    def link_get_type(self, lid):
        """
        Get the type of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: Link type
        """
        pass
