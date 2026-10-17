"""
Nebule Social Interface

This module defines the interface for social operations in the nebule library.
It is equivalent to 300_social_interface.php in the PHP version.
"""

from abc import ABC, abstractmethod


class SocialInterface(ABC):
    """
    Abstract base class for social operations.
    
    Classes implementing this interface provide social functionality
    for the nebule library, including managing social contexts and permissions.
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
    def social_get_context(self):
        """
        Get the current social context.
        
        Returns:
            str: Social context identifier
        """
        pass
    
    @abstractmethod
    def social_set_context(self, context):
        """
        Set the current social context.
        
        Args:
            context (str): Social context to set
        """
        pass
    
    @abstractmethod
    def social_check_permission(self, permission, entity=None):
        """
        Check if a permission is granted in the current social context.
        
        Args:
            permission (str): Permission to check
            entity (str): Optional entity to check against
            
        Returns:
            bool: True if permission is granted
        """
        pass
    
    @abstractmethod
    def social_is_myself(self, entity):
        """
        Check if an entity is the current user.
        
        Args:
            entity (str): Entity to check
            
        Returns:
            bool: True if entity is the current user
        """
        pass
    
    @abstractmethod
    def social_is_authority(self, entity):
        """
        Check if an entity is an authority.
        
        Args:
            entity (str): Entity to check
            
        Returns:
            bool: True if entity is an authority
        """
        pass
