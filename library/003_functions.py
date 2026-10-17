"""
Nebule Functions Module

This module provides utility functions for the nebule library.
It is equivalent to 003_functions.php in the PHP version.
"""

import re
from library.nebule_000_init import (
    LIB_NID_MIN_HASH_SIZE,
    LIB_NID_MIN_NONE_SIZE,
    LIB_NID_MAX_HASH_SIZE,
    LIB_NID_MIN_ALGO_SIZE,
    LIB_NID_MAX_ALGO_SIZE,
)


class Functions:
    """
    Functions class providing utility methods for the nebule library.
    
    This class provides methods for:
    - Node ID validation and manipulation
    - String and data processing
    - Various utility functions
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Functions, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, nebule_instance=None):
        """Initialize with reference to nebule instance."""
        if Functions._instance is not None:
            return
        
        self._nebule_instance = nebule_instance
        self._environment_library = None
    
    def set_environment_library(self, lib):
        """Set the environment library reference."""
        self._environment_library = lib
    
    def check_nid(self, nid='', permit_null=False, permit_zero=False):
        """
        Check if a node ID (NID) is valid.
        
        Args:
            nid (str): Node identifier to check
            permit_null (bool): Allow empty string
            permit_zero (bool): Allow '0' value
            
        Returns:
            bool: True if NID is valid
        """
        if permit_null and nid == '':
            return True
        if permit_zero and nid == '0':
            return True
        
        parts = nid.split('.')
        if len(parts) != 3:
            return False
        
        hash_val = parts[0]
        algo_val = parts[1]
        size_val = parts[2]
        
        # Determine minimum size based on algorithm
        if algo_val == 'none' or algo_val == 'string':
            min_size = LIB_NID_MIN_NONE_SIZE
        else:
            min_size = LIB_NID_MIN_HASH_SIZE
        
        # Validate hash value
        valid_chars = 'abcdef0123456789'
        hash_ok = all(c in valid_chars for c in hash_val)
        
        if (hash_val == ''
                or not min_size < (len(hash_val) * 4) < LIB_NID_MAX_HASH_SIZE
                or not hash_ok):
            return False
        
        # Validate algorithm value
        if algo_val == '' or not LIB_NID_MIN_ALGO_SIZE < len(algo_val) < LIB_NID_MAX_ALGO_SIZE:
            return False
        
        # Validate size value
        try:
            size_int = int(size_val)
        except ValueError:
            return False
            
        if (size_val == '' or not min_size < size_int < LIB_NID_MAX_HASH_SIZE
                or (len(hash_val) * 4) != size_int):
            return False
        
        return True
    
    def get_nid_hash(self, nid):
        """
        Extract the hash part from a node ID.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Hash part or empty string
        """
        if not self.check_nid(nid):
            return ''
        return nid.split('.')[0]
    
    def get_nid_algo(self, nid):
        """
        Extract the algorithm part from a node ID.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Algorithm part or empty string
        """
        if not self.check_nid(nid):
            return ''
        return nid.split('.')[1]
    
    def get_nid_size(self, nid):
        """
        Extract the size part from a node ID.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Size part or empty string
        """
        if not self.check_nid(nid):
            return ''
        return nid.split('.')[2]
    
    def clean_nid(self, nid):
        """
        Clean a node ID by removing extra characters.
        
        Args:
            nid (str): Node identifier to clean
            
        Returns:
            str: Cleaned node ID
        """
        # Remove whitespace and special characters
        nid = re.sub(r'[^a-zA-Z0-9\.]+', '', nid)
        return nid
    
    def get_from_array(self, array, name):
        """
        Get value from an array of tuples by name.
        
        Args:
            array: Array of tuples (name, value)
            name: Name to search for
            
        Returns:
            Value if found, empty string otherwise
        """
        for item in array:
            if isinstance(item, tuple) and len(item) >= 2:
                if item[0] == name:
                    return item[1]
        return ''
    
    def is_hex(self, string):
        """
        Check if a string contains only hexadecimal characters.
        
        Args:
            string (str): String to check
            
        Returns:
            bool: True if hexadecimal
        """
        valid_chars = '0123456789abcdefABCDEF'
        return all(c in valid_chars for c in string)
    
    def generate_random_hex(self, length=16):
        """
        Generate a random hexadecimal string.
        
        Args:
            length (int): Length of string to generate
            
        Returns:
            str: Random hexadecimal string
        """
        import random
        chars = '0123456789abcdef'
        return ''.join(random.choice(chars) for _ in range(length))
