"""
Nebule IO Module

This module provides basic I/O functionality for the nebule library.
It is equivalent to 101_io.php in the PHP version.
"""

import os
from library.nebule_000_init import (
    LIB_LOCAL_LINKS_FOLDER,
    LIB_LOCAL_OBJECTS_FOLDER,
    LIB_LOCAL_ENVIRONMENT_FILE,
    LIB_LOCAL_ENTITY_FILE,
    LIB_LOCAL_HISTORY_FILE,
)
from library.nebule_100_io_interface import IOInterface


class IO(IOInterface):
    """
    Basic I/O class for nebule library.
    
    This class provides the default implementation of IOInterface,
    using the local filesystem for storage.
    """
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
        self._ready = False
        self._mode = 'RW'  # Read-Write mode
        self._location = 'local'
        self._filter_string = ''
        self._files_transcode_key = ''
        
        # Initialize
        self._initialize()
    
    def _initialize(self):
        """Initialize the I/O system."""
        # Check if folders exist
        links_folder = LIB_LOCAL_LINKS_FOLDER
        objects_folder = LIB_LOCAL_OBJECTS_FOLDER
        
        # Create folders if they don't exist
        if not os.path.isdir(links_folder):
            try:
                os.makedirs(links_folder, exist_ok=True)
            except OSError:
                self._ready = False
                return
        
        if not os.path.isdir(objects_folder):
            try:
                os.makedirs(objects_folder, exist_ok=True)
            except OSError:
                self._ready = False
                return
        
        self._ready = True
    
    # IOInterface implementation
    
    def get_ready(self):
        """Get the readiness status."""
        return self._ready
    
    def get_filter_string(self):
        """Get the filter string."""
        return self._filter_string
    
    def get_mode(self):
        """Get the read/write mode."""
        return self._mode
    
    def get_location(self):
        """Get the default location."""
        return self._location
    
    def set_files_transcode_key(self, key):
        """Set the files transcode key."""
        self._files_transcode_key = key
    
    def io_link_check_node(self, nid):
        """Check if a node has a link."""
        if not self._ready or not nid:
            return False
        link_path = os.path.join(LIB_LOCAL_LINKS_FOLDER, nid)
        return os.path.isfile(link_path)
    
    def io_link_check_node_by_rid(self, rid):
        """Check if a node has a link by RID."""
        # For now, same as by NID
        return self.io_link_check_node(rid)
    
    def io_link_read(self, nid):
        """Read a link."""
        if not self._ready or not nid:
            return ''
        link_path = os.path.join(LIB_LOCAL_LINKS_FOLDER, nid)
        if not os.path.isfile(link_path):
            return ''
        try:
            with open(link_path, 'r') as f:
                return f.read()
        except IOError:
            return ''
    
    def io_link_read_by_rid(self, rid):
        """Read a link by RID."""
        # For now, same as by NID
        return self.io_link_read(rid)
    
    def io_object_check_node(self, nid):
        """Check if a node has an object."""
        if not self._ready or not nid:
            return False
        object_path = os.path.join(LIB_LOCAL_OBJECTS_FOLDER, nid)
        return os.path.isfile(object_path)
    
    def io_object_read(self, nid):
        """Read an object."""
        if not self._ready or not nid:
            return ''
        object_path = os.path.join(LIB_LOCAL_OBJECTS_FOLDER, nid)
        if not os.path.isfile(object_path):
            return ''
        try:
            with open(object_path, 'r') as f:
                return f.read()
        except IOError:
            return ''
    
    def io_object_write(self, nid, content):
        """Write an object."""
        if not self._ready or not nid or not content:
            return False
        object_path = os.path.join(LIB_LOCAL_OBJECTS_FOLDER, nid)
        try:
            with open(object_path, 'w') as f:
                f.write(content)
            return True
        except IOError:
            return False
    
    def io_object_delete(self, nid):
        """Delete an object."""
        if not self._ready or not nid:
            return False
        object_path = os.path.join(LIB_LOCAL_OBJECTS_FOLDER, nid)
        if not os.path.isfile(object_path):
            return False
        try:
            os.remove(object_path)
            return True
        except OSError:
            return False
    
    # Additional utility methods
    
    def io_environment_read(self):
        """Read the environment file."""
        if not os.path.isfile(LIB_LOCAL_ENVIRONMENT_FILE):
            return ''
        try:
            with open(LIB_LOCAL_ENVIRONMENT_FILE, 'r') as f:
                return f.read()
        except IOError:
            return ''
    
    def io_environment_write(self, content):
        """Write the environment file."""
        try:
            with open(LIB_LOCAL_ENVIRONMENT_FILE, 'w') as f:
                f.write(content)
            return True
        except IOError:
            return False
    
    def io_entity_read(self):
        """Read the entity file."""
        if not os.path.isfile(LIB_LOCAL_ENTITY_FILE):
            return ''
        try:
            with open(LIB_LOCAL_ENTITY_FILE, 'r') as f:
                return f.read()
        except IOError:
            return ''
    
    def io_entity_write(self, content):
        """Write the entity file."""
        try:
            with open(LIB_LOCAL_ENTITY_FILE, 'w') as f:
                f.write(content)
            return True
        except IOError:
            return False
    
    def io_history_read(self):
        """Read the history file."""
        if not os.path.isfile(LIB_LOCAL_HISTORY_FILE):
            return ''
        try:
            with open(LIB_LOCAL_HISTORY_FILE, 'r') as f:
                return f.read()
        except IOError:
            return ''
