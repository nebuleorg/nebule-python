"""
Nebule Social Onlist Module
Equivalent to 309_social_onlist.py in PHP version
"""
from library.nebule_300_social_interface import SocialInterface


class SocialOnlist(SocialInterface):
    def __init__(self, nebule_instance):
        self._nebule_instance = nebule_instance
    
    def social_get_context(self):
        return 'onlist'
    
    def social_set_context(self, context):
        pass
    
    def social_check_permission(self, permission, entity=None):
        # Stub implementation
        return True
    
    def social_is_myself(self, entity):
        return False
    
    def social_is_authority(self, entity):
        return False
