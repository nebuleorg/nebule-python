"""
Nebule IO Interface

This module defines the interface for I/O operations in the nebule library.
It is equivalent to 100_io_interface.php in the PHP version.
"""

from abc import ABC, abstractmethod


class IOInterface(ABC):
    """
    Abstract base class for I/O operations.
    
    Classes implementing this interface provide low-level access to nebule
    objects and their links. They allow checking for the presence of nebule
    objects and their links, reading them, writing them, and deleting their contents.
    
    Each nebule object is referenced by a string containing the hexadecimal ID
    of the object. You cannot use an object (instance) directly here; you must
    first extract the hexadecimal ID as text.
    """
    
    @abstractmethod
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        pass
    
    # Module management functions
    
    @abstractmethod
    def get_ready(self):
        """
        Get the readiness status.
        
        Returns:
            bool: True if ready, False otherwise
        """
        pass
    
    @abstractmethod
    def get_filter_string(self):
        """
        Get the filter string for this filesystem type.
        
        Returns:
            str: Filter string
        """
        pass
    
    @abstractmethod
    def get_mode(self):
        """
        Get the read/write mode (RO/RW).
        
        Returns:
            str: Mode string
        """
        pass
    
    @abstractmethod
    def get_location(self):
        """
        Get the default location string.
        
        Returns:
            str: Location string
        """
        pass
    
    # Link management functions
    
    @abstractmethod
    def set_files_transcode_key(self, key):
        """
        Initialize the transcode key for hidden link files.
        
        Args:
            key: Transcode key
        """
        pass
    
    @abstractmethod
    def io_link_check_node(self, nid):
        """
        Check if a node has a link.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if link exists
        """
        pass
    
    @abstractmethod
    def io_link_check_node_by_rid(self, rid):
        """
        Check if a node has a link by RID.
        
        Args:
            rid (str): Reference identifier
            
        Returns:
            bool: True if link exists
        """
        pass
    
    @abstractmethod
    def io_link_read(self, nid):
        """
        Read a link.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Link content or empty string
        """
        pass
    
    @abstractmethod
    def io_link_read_by_rid(self, rid):
        """
        Read a link by RID.
        
        Args:
            rid (str): Reference identifier
            
        Returns:
            str: Link content or empty string
        """
        pass
    
    # Object management functions
    
    @abstractmethod
    def io_object_check_node(self, nid):
        """
        Check if a node has an object.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if object exists
        """
        pass
    
    @abstractmethod
    def io_object_read(self, nid):
        """
        Read an object.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Object content or empty string
        """
        pass
    
    @abstractmethod
    def io_object_write(self, nid, content):
        """
        Write an object.
        
        Args:
            nid (str): Node identifier
            content (str): Content to write
            
        Returns:
            bool: True if successful
        """
        pass
    
    @abstractmethod
    def io_object_delete(self, nid):
        """
        Delete an object.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if successful
        """
        pass
