"""
Nebule IO Disk Module

This module provides disk-based I/O functionality for the nebule library.
It is equivalent to 102_io_disk.php in the PHP version.
"""

from library.nebule_100_io_interface import IOInterface


class IODisk(IOInterface):
    """
    Disk I/O class for nebule library.
    
    This class provides disk-based implementation of IOInterface.
    It extends the basic IO class with disk-specific functionality.
    """
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        # Call parent constructor
        super().__init__(nebule_instance)
        self._type = 'disk'
    
    def get_ready(self):
        """Get the readiness status."""
        # For now, use parent implementation
        return super().get_ready()
    
    def get_filter_string(self):
        """Get the filter string for disk filesystem."""
        return 'disk'
    
    def get_mode(self):
        """Get the read/write mode."""
        return 'RW'
    
    def get_location(self):
        """Get the default location."""
        return 'disk'
    
    def set_files_transcode_key(self, key):
        """Set the files transcode key."""
        # For now, use parent implementation
        super().set_files_transcode_key(key)
