"""
Nebule Core Library

This is the main nebule library class.
It is equivalent to 001_nebule.php in the PHP version.

This class serves as the central point for the nebule library, coordinating
all the different components and providing the main API.
"""

from library.nebule_000_init import (
    NEBULE_NAME,
    NEBULE_SURNAME,
    NEBULE_VERSION,
    NEBULE_AUTHOR,
    NEBULE_LICENCE,
    NEBULE_WEBSITE,
    NEBULE_CODING,
    NEBULE_FUNCTION_VERSION,
)
from library.nebule_004_metrology import Metrology
from library.nebule_005_configuration import Configuration
from library.nebule_003_functions import Functions


class Nebule:
    """
    Main nebule library class.
    
    This is the core class that initializes and coordinates all nebule library
    components. It provides access to all library functionality.
    
    Attributes:
        _nebule_instance: Self-reference for singleton pattern
        _metrology_instance: Metrology instance
        _configuration_instance: Configuration instance
        _functions: Functions instance
        ... (other instances will be added as needed)
    """
    
    # Session saved variables (for serialization)
    SESSION_SAVED_VARS = [
        '_authorities_instance',
        '_recovery_instance',
        '_cache_instance',
        '_session_instance',
        '_tokenize_instance',
        '_crypto_instance',
    ]
    
    _instance = None
    _loading_status = False
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance."""
        if cls._instance is None:
            cls._instance = super(Nebule, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the nebule library.
        
        This constructor:
        - Sets up the singleton instance
        - Initializes logging
        - Initializes all library components
        """
        global nebule_instance
        
        # Only initialize once
        if hasattr(self, '_initialized') and self._initialized:
            return
        
        # Set singleton instance
        Nebule._instance = self
        Nebule._nebule_instance = self
        nebule_instance = self
        self._initialized = False
        
        # Initialize metrology first (it's needed for logging)
        # This will create the Metrology singleton
        self._metrology_instance = Metrology()
        
        # Reopen metrology log
        Metrology.log_reopen(NEBULE_NAME)
        Metrology.add_log(
            'Loading nebule library',
            Metrology.LOG_LEVEL_INFO,
            '__init__',
            '1452ed72'
        )
        
        # Initialize other components
        self._initialisation()
        
        # Set loading status
        Nebule._loading_status = True
    
    def __str__(self):
        """String representation of the nebule instance."""
        return NEBULE_NAME
    
    def __sleep__(self):
        """Prepare for serialization."""
        return self.SESSION_SAVED_VARS
    
    def __wakeup__(self):
        """Restore after deserialization."""
        global nebule_instance
        Nebule._nebule_instance = self
        nebule_instance = self
        Metrology.add_log(
            'Reloading nebule library',
            Metrology.LOG_LEVEL_INFO,
            '__wakeup__',
            '2d9358d5'
        )
        self._initialisation()
    
    def _initialisation(self):
        """
        Initialize all library components.
        
        This method is called during __init__ and __wakeup__ to set up
        all the library instances.
        """
        # Metrology is already initialized in __init__
        self._metrology_instance.add_log(
            'first step init nebule instance',
            Metrology.LOG_LEVEL_DEBUG,
            '_initialisation',
            '64154189'
        )
        
        # Initialize functions
        self._functions = Functions(self)
        self._functions.set_environment_library(self)
        
        # Initialize configuration
        self._init_configuration()
        
        # Other initializations (stubs for now)
        self._init_rescue()
        self._init_session()
        self._init_crypto()
        self._init_io()
        self._init_cache()
        self._init_social()
        self._init_authorities()
        self._init_recovery()
        self._init_entities()
        self._init_tokenize()
        self._init_router()
        
        # Set environment instances
        self._set_environment_instances()
        
        # Initialize all instances
        self._init_all_instances()
        
        # Apply configuration
        if hasattr(self, '_configuration_instance') and self._configuration_instance:
            self._configuration_instance.set_permit_options_by_links(True)
            self._configuration_instance.flush_cache()
        
        # Additional initialization steps
        self._get_subordination_entity()
        self._check_writeable_io()
        self._find_current_objet()
        self._find_current_entity()
        
        # Mark as initialized
        self._initialized = True
    
    def _init_configuration(self):
        """Initialize configuration instance."""
        self._configuration_instance = Configuration(self)
    
    def _init_rescue(self):
        """Initialize rescue instance."""
        # Stub - will be implemented in 006_rescue.py
        self._rescue_instance = None
    
    def _init_session(self):
        """Initialize session instance."""
        # Stub - will be implemented in 011_session.py
        self._session_instance = None
    
    def _init_crypto(self):
        """Initialize crypto instance."""
        # Stub - will be implemented in crypto modules
        self._crypto_instance = None
    
    def _init_io(self):
        """Initialize I/O instance."""
        # Stub - will be implemented in IO modules
        self._io_instance = None
    
    def _init_cache(self):
        """Initialize cache instance."""
        # Stub - will be implemented in 010_cache.py
        self._cache_instance = None
    
    def _init_social(self):
        """Initialize social instance."""
        # Stub - will be implemented in social modules
        self._social_instance = None
    
    def _init_authorities(self):
        """Initialize authorities instance."""
        # Stub - will be implemented in 007_authorities.py
        self._authorities_instance = None
    
    def _init_recovery(self):
        """Initialize recovery instance."""
        # Stub - will be implemented in 009_recovery.py
        self._recovery_instance = None
    
    def _init_entities(self):
        """Initialize entities instance."""
        # Stub - will be implemented in 008_entities.py
        self._entities_instance = None
    
    def _init_tokenize(self):
        """Initialize tokenize instance."""
        # Stub - will be implemented in 012_tokenize.py
        self._tokenize_instance = None
    
    def _init_router(self):
        """Initialize router instance."""
        # Stub - will be implemented in 014_router.py
        self._router_instance = None
    
    def _set_environment_instances(self):
        """Set environment instances."""
        # Stub for now
        pass
    
    def _init_all_instances(self):
        """Initialize all instances."""
        # Stub for now
        pass
    
    def _get_subordination_entity(self):
        """Get subordination entity."""
        # Stub for now
        pass
    
    def _check_writeable_io(self):
        """Check if I/O is writeable."""
        # Stub for now
        pass
    
    def _find_current_objet(self):
        """Find the current object."""
        # Stub for now
        pass
    
    def _find_current_entity(self):
        """Find the current entity."""
        # Stub for now
        pass
    
    # Public accessors for instances
    
    @property
    def metrology(self):
        """Get the metrology instance."""
        return self._metrology_instance
    
    @property
    def configuration(self):
        """Get the configuration instance."""
        return self._configuration_instance
    
    @property
    def functions(self):
        """Get the functions instance."""
        return self._functions
    
    @property
    def io(self):
        """Get the I/O instance."""
        return self._io_instance
    
    @property
    def crypto(self):
        """Get the crypto instance."""
        return self._crypto_instance
    
    @property
    def cache(self):
        """Get the cache instance."""
        return self._cache_instance
    
    @property
    def authorities(self):
        """Get the authorities instance."""
        return self._authorities_instance
    
    @property
    def entities(self):
        """Get the entities instance."""
        return self._entities_instance
    
    @property
    def session(self):
        """Get the session instance."""
        return self._session_instance
