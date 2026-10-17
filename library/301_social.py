"""
Nebule Social Module

This module provides social functionality for the nebule library.
It is equivalent to 301_social.php in the PHP version.
"""

from library.nebule_300_social_interface import SocialInterface


class Social(SocialInterface):
    """
    Main social class for nebule library.
    
    This class provides social context management and permission checking.
    """
    
    # Social context constants
    SOCIAL_CONTEXT_MYSELF = 'myself'
    SOCIAL_CONTEXT_NOTMYSELF = 'notmyself'
    SOCIAL_CONTEXT_SELF = 'self'
    SOCIAL_CONTEXT_NOTSELF = 'notself'
    SOCIAL_CONTEXT_AUTHORITY = 'authority'
    SOCIAL_CONTEXT_ALL = 'all'
    SOCIAL_CONTEXT_NONE = 'none'
    SOCIAL_CONTEXT_ONLIST = 'onlist'
    SOCIAL_CONTEXT_OFFLIST = 'offlist'
    SOCIAL_CONTEXT_REPUTATION = 'reputation'
    SOCIAL_CONTEXT_UNREPUTATION = 'unreputation'
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
        self._context = Social.SOCIAL_CONTEXT_ALL
        self._current_entity = ''
        self._social_library = 'authority'  # Default from configuration
    
    def social_get_context(self):
        """
        Get the current social context.
        
        Returns:
            str: Social context identifier
        """
        return self._context
    
    def social_set_context(self, context):
        """
        Set the current social context.
        
        Args:
            context (str): Social context to set
        """
        self._context = context
    
    def social_check_permission(self, permission, entity=None):
        """
        Check if a permission is granted in the current social context.
        
        Args:
            permission (str): Permission to check
            entity (str): Optional entity to check against
            
        Returns:
            bool: True if permission is granted
        """
        # This is a simplified implementation
        # The full implementation would check against the current entity,
        # social context, and permission configuration
        
        # For now, always return True for this basic implementation
        return True
    
    def social_is_myself(self, entity):
        """
        Check if an entity is the current user.
        
        Args:
            entity (str): Entity to check
            
        Returns:
            bool: True if entity is the current user
        """
        if not entity or not self._current_entity:
            return False
        return entity == self._current_entity
    
    def social_is_authority(self, entity):
        """
        Check if an entity is an authority.
        
        Args:
            entity (str): Entity to check
            
        Returns:
            bool: True if entity is an authority
        """
        # Simplified implementation
        # In the full implementation, this would check against
        # the authorities list
        return False
    
    def set_current_entity(self, entity):
        """
        Set the current entity.
        
        Args:
            entity (str): Entity ID to set as current
        """
        self._current_entity = entity
    
    def get_current_entity(self):
        """
        Get the current entity.
        
        Returns:
            str: Current entity ID
        """
        return self._current_entity
    
    def set_social_library(self, library):
        """
        Set the social library to use.
        
        Args:
            library (str): Social library name
        """
        self._social_library = library
    
    def get_social_library(self):
        """
        Get the current social library.
        
        Returns:
            str: Social library name
        """
        return self._social_library
