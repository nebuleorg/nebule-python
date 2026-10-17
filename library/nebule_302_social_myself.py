"""
Nebule Social Myself Module

This module represents the "myself" social context for the nebule library.
It is equivalent to 302_social_myself.php in the PHP version.
"""

from library.nebule_300_social_interface import SocialInterface


class SocialMyself(SocialInterface):
    """
    Social class for "myself" context.
    
    This class represents social operations where the context is the current user themselves.
    """
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
    
    def social_get_context(self):
        """Get the social context - always 'myself'."""
        return 'myself'
    
    def social_set_context(self, context):
        """Set context - not applicable for myself."""
        pass
    
    def social_check_permission(self, permission, entity=None):
        """
        Check permission in myself context.
        
        In the myself context, permissions are checked against the current entity.
        
        Args:
            permission (str): Permission to check
            entity (str): Entity to check against
            
        Returns:
            bool: True if permission is granted
        """
        # In myself context, only the current entity has permissions
        if hasattr(self._nebule_instance, 'entities') and self._nebule_instance.entities:
            current_entity = self._nebule_instance.entities.get_current_entity()
            if entity and entity == current_entity:
                return True
        return False
    
    def social_is_myself(self, entity):
        """Check if entity is myself - always True if entity matches current."""
        if hasattr(self._nebule_instance, 'entities') and self._nebule_instance.entities:
            current_entity = self._nebule_instance.entities.get_current_entity()
            return entity == current_entity
        return False
    
    def social_is_authority(self, entity):
        """Check if entity is an authority - not in myself context."""
        return False
