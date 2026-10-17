"""
Nebule Social Notself Module
Equivalent to 305_social_notself.py in PHP version
"""
from library.nebule_300_social_interface import SocialInterface


class SocialNotself(SocialInterface):
    def __init__(self, nebule_instance):
        self._nebule_instance = nebule_instance
    
    def social_get_context(self):
        return 'notself'
    
    def social_set_context(self, context):
        pass
    
    def social_check_permission(self, permission, entity=None):
        # Stub implementation
        return True
    
    def social_is_myself(self, entity):
        return False
    
    def social_is_authority(self, entity):
        return False
