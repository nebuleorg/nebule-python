"""
Nebule Node Module

This module provides node functionality for the nebule library.
It is equivalent to 401_node.php in the PHP version.
"""

from library.nebule_400_node_interface import NodeInterface
from library.nebule_000_init import (
    LIB_NID_MIN_HASH_SIZE,
    LIB_NID_MIN_NONE_SIZE,
    LIB_NID_MAX_HASH_SIZE,
    LIB_NID_MIN_ALGO_SIZE,
    LIB_NID_MAX_ALGO_SIZE,
)


class Node(NodeInterface):
    """
    Node class for nebule library.
    
    This class provides functionality for managing nebule nodes (objects, entities, etc.).
    """
    
    # Node types
    NODE_TYPE_OBJECT = 'object'
    NODE_TYPE_ENTITY = 'entity'
    NODE_TYPE_GROUP = 'group'
    NODE_TYPE_CONVERSATION = 'conversation'
    NODE_TYPE_LOCATION = 'location'
    NODE_TYPE_CURRENCY = 'currency'
    NODE_TYPE_WALLET = 'wallet'
    NODE_TYPE_TOKEN = 'token'
    NODE_TYPE_TOKENPOOL = 'tokenpool'
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
        self._type = Node.NODE_TYPE_OBJECT
    
    def node_new(self, type_node, data=''):
        """
        Create a new node.
        
        Args:
            type_node (str): Type of node
            data (str): Node data
            
        Returns:
            str: New node identifier or empty string on failure
        """
        # Generate a new NID
        nid = self._generate_nid()
        if not nid:
            return ''
        
        # Store the node
        if hasattr(self._nebule_instance, 'io') and self._nebule_instance.io:
            if self._nebule_instance.io.io_object_write(nid, data):
                return nid
        
        return ''
    
    def node_check(self, nid):
        """
        Check if a node exists and is valid.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if node is valid
        """
        if not self._check_nid(nid):
            return False
        
        if hasattr(self._nebule_instance, 'io') and self._nebule_instance.io:
            return self._nebule_instance.io.io_object_check_node(nid)
        
        return False
    
    def node_read(self, nid):
        """
        Read a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            dict: Node data or empty dict on failure
        """
        if not self._check_nid(nid):
            return {}
        
        if hasattr(self._nebule_instance, 'io') and self._nebule_instance.io:
            content = self._nebule_instance.io.io_object_read(nid)
            if content:
                return {
                    'nid': nid,
                    'content': content,
                    'type': self._guess_type_from_nid(nid)
                }
        
        return {}
    
    def node_write(self, nid, data):
        """
        Write to a node.
        
        Args:
            nid (str): Node identifier
            data (str): Data to write
            
        Returns:
            bool: True if write was successful
        """
        if not self._check_nid(nid):
            return False
        
        if hasattr(self._nebule_instance, 'io') and self._nebule_instance.io:
            return self._nebule_instance.io.io_object_write(nid, data)
        
        return False
    
    def node_delete(self, nid):
        """
        Delete a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if deletion was successful
        """
        if not self._check_nid(nid):
            return False
        
        if hasattr(self._nebule_instance, 'io') and self._nebule_instance.io:
            return self._nebule_instance.io.io_object_delete(nid)
        
        return False
    
    def node_get_type(self, nid):
        """
        Get the type of a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Node type
        """
        return self._guess_type_from_nid(nid)
    
    def _check_nid(self, nid):
        """
        Check if a NID is valid.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if valid
        """
        if not nid:
            return False
        
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
    
    def _generate_nid(self):
        """
        Generate a new node ID.
        
        Returns:
            str: New node ID
        """
        import secrets
        import hashlib
        
        # Generate random bytes
        random_bytes = secrets.token_bytes(32)
        
        # Hash to get hexadecimal representation
        h = hashlib.sha256(random_bytes)
        hash_hex = h.hexdigest()
        
        # Format as NID: hash.algo.size
        nid = f"{hash_hex}.sha2.256"
        return nid
    
    def _guess_type_from_nid(self, nid):
        """
        Guess the node type from its NID.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Guessed node type
        """
        # This is a simplified implementation
        # In the full implementation, this would check the node's content or links
        return Node.NODE_TYPE_OBJECT
