"""
Nebule IO Network HTTPS Module
Equivalent to 104_io_network_https.php in PHP version
"""

from library.nebule_103_io_network_http import IONetworkHTTP


class IONetworkHTTPS(IONetworkHTTP):
    """
    HTTPS network I/O class for nebule library.
    
    This class provides HTTPS-based implementation of IOInterface.
    It extends IONetworkHTTP with SSL/TLS support.
    """
    
    def __init__(self, nebule_instance):
        super().__init__(nebule_instance)
        self._type = 'https'
        self._location = 'https://localhost'
    
    def get_mode(self):
        return 'RO'  # HTTPS is typically read-only
    
    def get_location(self):
        return self._location
