"""
Nebule Conversation Module
Equivalent to 405_conversation.py in PHP version
"""

from library.nebule_400_node_interface import NodeInterface


class Conversation(NodeInterface):
    """
    Conversation class for nebule library.
    
    This class provides functionality for managing nebule conversations.
    """
    
    def __init__(self, nebule_instance):
        self._nebule_instance = nebule_instance
    
    def node_new(self, type_node, data=''):
        """Create a new conversation."""
        from library.nebule_401_node import Node
        node = Node(self._nebule_instance)
        return node.node_new(type_node, data)
    
    def node_check(self, nid):
        """Check if a conversation exists."""
        from library.nebule_401_node import Node
        node = Node(self._nebule_instance)
        return node.node_check(nid)
    
    def node_read(self, nid):
        """Read a conversation."""
        from library.nebule_401_node import Node
        node = Node(self._nebule_instance)
        result = node.node_read(nid)
        if result:
            result['type'] = 'conversation'
        return result
    
    def node_write(self, nid, data):
        """Write to a conversation."""
        from library.nebule_401_node import Node
        node = Node(self._nebule_instance)
        return node.node_write(nid, data)
    
    def node_delete(self, nid):
        """Delete a conversation."""
        from library.nebule_401_node import Node
        node = Node(self._nebule_instance)
        return node.node_delete(nid)
    
    def node_get_type(self, nid):
        """Get the type - always 'conversation'."""
        return 'conversation'
