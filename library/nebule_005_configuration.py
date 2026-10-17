"""
Nebule Configuration Module

This module provides configuration management for the nebule library.
It is equivalent to 005_configuration.php in the PHP version.
"""

from library.nebule_000_init import (
    LIB_CONFIGURATIONS_NAME,
    LIB_CONFIGURATIONS_TYPE,
    LIB_CONFIGURATIONS_DEFAULT,
    LIB_DEFAULT_PUPPETMASTER_EID,
)


class Configuration:
    """
    Configuration class for managing nebule library settings.
    
    This class provides methods for:
    - Getting and setting configuration options
    - Validating configuration values
    - Managing default values
    """
    
    _instance = None
    _config = {}
    _cached_config = {}
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, nebule_instance=None):
        """Initialize configuration with default values."""
        if Configuration._instance is not None:
            return
        
        self._nebule_instance = nebule_instance
        Configuration._config = {}
        Configuration._cached_config = {}
        
        # Load default configurations
        for name, default_value in LIB_CONFIGURATIONS_DEFAULT:
            Configuration._config[name] = default_value
    
    def get_option_as_string(self, name):
        """
        Get a configuration option as a string.
        
        Args:
            name (str): Configuration option name
            
        Returns:
            str: Option value or empty string if not found
        """
        if name == '' or name not in LIB_CONFIGURATIONS_NAME:
            return ''
        return str(self._config.get(name, ''))
    
    def get_option_as_bool(self, name):
        """
        Get a configuration option as a boolean.
        
        Args:
            name (str): Configuration option name
            
        Returns:
            bool: Option value or False if not found
        """
        if name == '' or name not in LIB_CONFIGURATIONS_NAME:
            return False
        value = self._config.get(name, False)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes')
        return bool(value)
    
    def get_option_as_int(self, name):
        """
        Get a configuration option as an integer.
        
        Args:
            name (str): Configuration option name
            
        Returns:
            int: Option value or 0 if not found
        """
        if name == '' or name not in LIB_CONFIGURATIONS_NAME:
            return 0
        value = self._config.get(name, 0)
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    def set_option(self, name, value):
        """
        Set a configuration option.
        
        Args:
            name (str): Configuration option name
            value: Value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        if name == '' or name not in LIB_CONFIGURATIONS_NAME:
            return False
        
        # Get the expected type
        expected_type = None
        for config_name, config_type in LIB_CONFIGURATIONS_TYPE:
            if config_name == name:
                expected_type = config_type
                break
        
        # Validate type
        if expected_type == 'boolean':
            self._config[name] = bool(value)
        elif expected_type == 'integer':
            try:
                self._config[name] = int(value)
            except (ValueError, TypeError):
                return False
        elif expected_type == 'string':
            self._config[name] = str(value)
        else:
            self._config[name] = value
        
        # Clear cache
        self.flush_cache()
        return True
    
    def get_config_type(self, name):
        """
        Get the type of a configuration option.
        
        Args:
            name (str): Configuration option name
            
        Returns:
            str: Type name or empty string
        """
        for config_name, config_type in LIB_CONFIGURATIONS_TYPE:
            if config_name == name:
                return config_type
        return ''
    
    def flush_cache(self):
        """Clear the configuration cache."""
        Configuration._cached_config = {}
    
    def set_permit_options_by_links(self, value):
        """
        Set whether options can be permitted by links.
        
        Args:
            value (bool): True to permit, False otherwise
        """
        # Stub for now
        pass
    
    def get_default_entity(self):
        """
        Get the default entity.
        
        Returns:
            str: Default entity ID
        """
        return self.get_option_as_string('defaultEntity') or LIB_DEFAULT_PUPPETMASTER_EID
    
    def get_puppetmaster(self):
        """
        Get the puppetmaster entity.
        
        Returns:
            str: Puppetmaster entity ID
        """
        return self.get_option_as_string('puppetmaster') or LIB_DEFAULT_PUPPETMASTER_EID
