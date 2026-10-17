"""
Nebule Social Not Myself Module
Equivalent to 303_social_notmyself.php
"""
from library.nebule_300_social_interface import SocialInterface


class SocialNotMyself(SocialInterface):
    def __init__(self, nebule_instance):
        self._nebule_instance = nebule_instance
    
    def social_get_context(self):
        return 'notmyself'
    
    def social_set_context(self, context):
        pass
    
    def social_check_permission(self, permission, entity=None):
        # Permissions for entities that are not myself
        if hasattr(self._nebule_instance, 'entities') and self._nebule_instance.entities:
            current_entity = self._nebule_instance.entities.get_current_entity()
            if entity and entity != current_entity:
                return True
        return False
    
    def social_is_myself(self, entity):
        return False
    
    def social_is_authority(self, entity):
        return False
