"""
Nebule Metrology Module

This module provides metrology and logging functionality for the nebule library.
It is equivalent to 004_metrology.php in the PHP version.
"""

import syslog
import datetime
import traceback
from library.nebule_000_init import NEBULE_NAME


class Metrology:
    """
    Metrology class for logging and performance measurement.
    
    This class provides methods for:
    - Logging messages with different levels
    - Measuring time intervals
    - Managing session-specific logging
    """
    
    LOG_LEVEL_DEBUG = 'debug'
    LOG_LEVEL_INFO = 'info'
    LOG_LEVEL_MSG = 'msg'
    LOG_LEVEL_WARNING = 'warning'
    LOG_LEVEL_ERROR = 'error'
    LOG_LEVEL_CRITICAL = 'critical'
    
    _instance = None
    _session_id = ''
    _start_time = None
    _logs = []
    _timers = {}
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance."""
        if cls._instance is None:
            cls._instance = super(Metrology, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize metrology with session ID and start time."""
        # Only initialize once
        if Metrology._start_time is not None:
            return
        
        import random
        import binascii
        
        Metrology._session_id = binascii.hexlify(random.randbytes(6)).decode('ascii')
        Metrology._start_time = datetime.datetime.now()
        Metrology._logs = []
        Metrology._timers = {}
        
        # Initialize syslog
        self.log_init(NEBULE_NAME)
    
    @classmethod
    def log_init(cls, name):
        """Initialize syslog with session ID."""
        syslog.openlog(f'{name}/{cls._session_id}', syslog.LOG_NDELAY, syslog.LOG_USER)
    
    @classmethod
    def log_reopen(cls, name):
        """Reopen syslog connection."""
        syslog.closelog()
        cls.log_init(name)
    
    @classmethod
    def add_log(cls, message, level=LOG_LEVEL_MSG, function='', uid='00000000'):
        """
        Add a log entry.
        
        Args:
            message (str): The log message
            level (str): Log level (debug, info, msg, warning, error, critical)
            function (str): Function name where log originated
            uid (str): Unique identifier for the log entry
        """
        diffdate = datetime.datetime.now() - cls._start_time
        log_entry = {
            'timestamp': datetime.datetime.now(),
            'diffdate': diffdate,
            'level': level,
            'function': function,
            'uid': uid,
            'message': message
        }
        cls._logs.append(log_entry)
        
        # Log to syslog
        syslog.syslog(
            f'LogT={diffdate} LogL="{level}" LogI="{uid}" LogF="{function}" LogM="{message}"'
        )
    
    @classmethod
    def add_log_disp(cls, message, level=LOG_LEVEL_MSG, function='', uid='00000000'):
        """Add a log entry and display it."""
        cls.add_log(message, level, function, uid)
        print(f'{level}({function}) : {uid} : {message}')
    
    @classmethod
    def set_metrology_timer(cls, name):
        """Set a named timer."""
        cls._timers[name] = datetime.datetime.now()
    
    @classmethod
    def get_metrology_timer(cls, name):
        """Get elapsed time for a named timer."""
        if name not in cls._timers:
            return 0
        return (datetime.datetime.now() - cls._timers[name]).total_seconds()
    
    @classmethod
    def get_metrology(cls, name):
        """Get a metrology value."""
        # For now, return timer value or 0
        return cls.get_metrology_timer(name)
    
    @classmethod
    def increment_metrology(cls, name):
        """Increment a metrology counter."""
        # For now, just a stub
        pass
    
    @classmethod
    def get_start_time(cls):
        """Get the metrology start time."""
        return cls._start_time
    
    @classmethod
    def get_session_id(cls):
        """Get the current session ID."""
        return cls._session_id
    
    @classmethod
    def get_logs(cls):
        """Get all logged entries."""
        return cls._logs
    
    @classmethod
    def flush_logs(cls):
        """Clear all logged entries."""
        cls._logs = []
