"""
Nebule Link Interface

This module defines the interface for link operations in the nebule library.
It is equivalent to 500_link_interface.php in the PHP version.

Link field naming convention:
The fields of a link register (RL) are named NID1, NID2, NID3, NID4
(formerly source, target, meta/type, data) as in the PHP implementation.
RL format: REQ>NID1>NID2>NID3>NID4
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
    def link_new(self, nid1, nid2, nid3, nid4='0'):
        """
        Create a new link.
        
        Args:
            nid1 (str): First node identifier (NID1)
            nid2 (str): Second node identifier (NID2)
            nid3 (str): Third node identifier (NID3, can be a type or meta)
            nid4 (str): Fourth node identifier (NID4, optional, '0' if unused)
            
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
    def link_get_nid1(self, lid):
        """
        Get the NID1 field of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: NID1 node identifier
        """
        pass
    
    @abstractmethod
    def link_get_nid2(self, lid):
        """
        Get the NID2 field of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: NID2 node identifier
        """
        pass
    
    @abstractmethod
    def link_get_nid3(self, lid):
        """
        Get the NID3 field of a link.
        
        Args:
            lid (str): Link identifier
            
        Returns:
            str: NID3 node identifier (type or meta)
        """
        pass
