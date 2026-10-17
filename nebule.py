#!/usr/bin/python3
# ------------------------------------------------------------------------------------------
# Imports
import os
import sys
import argparse
import importlib.util
import traceback
import random
import syslog
import datetime
import binascii
from pathlib import Path

# ------------------------------------------------------------------------------------------
BOOTSTRAP_NAME = 'bootstrap'
BOOTSTRAP_SURNAME = 'nebule/bootstrap'
BOOTSTRAP_AUTHOR = 'Project nebule'
BOOTSTRAP_VERSION = '020250425'
BOOTSTRAP_LICENCE = 'GNU GPL 2010-2025'
BOOTSTRAP_WEBSITE = 'www.nebule.org'
BOOTSTRAP_NODE = '88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256'
BOOTSTRAP_CODING = 'application/x-python'
# ------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
#  /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING /// WARNING ///
# ------------------------------------------------------------------------------------------
#
# [FR] Toute modification de ce code entrainera une modification de son empreinte
#      et entrainera donc automatiquement son invalidation !
# [EN] Any changes to this code will cause a change in its footprint and therefore
#      automatically result in its invalidation!
# [ES] Cualquier cambio en el código causarán un cambio en su presencia y por lo
#      tanto lugar automáticamente a su anulación!
#
# ------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------
# Configuration constants for the nebule library
# ------------------------------------------------------------------------------------------

LIB_LINK_VERSION = '2:0'
LIB_DEFAULT_PUPPETMASTER_EID = '88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256'
LIB_DEFAULT_PUPPETMASTER_LOCATION = 'http://puppetmaster.nebule.org'
LIB_REF_CODE_ALGO = 'sha2.256'

# Local storage configuration
LIB_LOCAL_ENVIRONMENT_FILE = 'c'
LIB_LOCAL_ENTITY_FILE = 'e'
LIB_LOCAL_LINKS_FOLDER = 'l'
LIB_LOCAL_OBJECTS_FOLDER = 'o'
LIB_LOCAL_HISTORY_FILE = 'h'

# Node ID constraints
LIB_NID_MIN_HASH_SIZE = 64
LIB_NID_MIN_NONE_SIZE = 8
LIB_NID_MAX_HASH_SIZE = 8192
LIB_NID_MIN_ALGO_SIZE = 2
LIB_NID_MAX_ALGO_SIZE = 12

# ------------------------------------------------------------------------------------------
# Metrology and logging setup
# ------------------------------------------------------------------------------------------

loggerSessionID = binascii.hexlify(random.randbytes(6)).decode('ascii')
metrologyStartTime = datetime.datetime.now()


def log_init(name):
    """Initialize syslog with a unique session ID."""
    syslog.openlog(f'{name}/{loggerSessionID}', syslog.LOG_NDELAY, syslog.LOG_USER)


def log_reopen(name):
    """Reopen syslog connection."""
    syslog.closelog()
    log_init(name)


def log_add(message, level='msg', function='', uid='00000000'):
    """Add a log entry to syslog."""
    diffdate = datetime.datetime.now() - metrologyStartTime
    syslog.syslog(f'LogT={diffdate} LogL="{level}" LogI="{uid}" LogF="{function}" LogM="{message}"')


def log_add_disp(message, level='msg', function='', uid='00000000'):
    """Add a log entry and display it."""
    log_add(message, level, function, uid)
    print(f'{level}({function}) : {uid} : {message}')


# Initialize logging
log_init(BOOTSTRAP_NAME)
syslog.syslog(f'LogT=0 LogT0={metrologyStartTime} LogL="info" LogI="76941959" LogM="start {BOOTSTRAP_NAME}"')

# ------------------------------------------------------------------------------------------
# Break codes and descriptions for error handling
# ------------------------------------------------------------------------------------------

bootstrapBreak = []

BREAK_DESCRIPTIONS = (
    ('00', 'unknown buggy interrupt reason'),
    ('11', 'user interrupt'),
    ('21', 'library init error'),
    ('22', "library i/o : link's folder error"),
    ('23', "library i/o : link's folder error"),
    ('24', "library i/o : object's folder error"),
    ('25', "library i/o : object's folder error"),
    ('31', 'library load : finding library IID error.'),
    ('32', 'library load : finding library OID error.'),
    ('41', 'library load : find code error'),
    ('42', 'library load : include code error'),
    ('43', 'library load : load error'),
    ('44', 'application : find code error'),
    ('45', 'application : include code error'),
    ('46', 'application : load error'),
    ('51', 'unknown bootstrap hash'),
    ('61', 'no local server entity'),
    ('62', 'local server entity error'),
    ('71', 'need sync puppetmaster'),
    ('81', 'library init : I/O open error'),
    ('82', 'library init : puppetmaster error'),
)


def bootstrap_set_break(errorCode, function):
    """Set a bootstrap break with error code and description."""
    errorDesc = _get_from_array(BREAK_DESCRIPTIONS, errorCode)
    if errorDesc == '':
        errorDesc = _get_from_array(BREAK_DESCRIPTIONS, '00')
    bootstrapBreak.append([errorCode, errorDesc])
    log_add(f'bootstrap break code={errorCode} : {errorDesc}', 'error', function, f'100000{errorCode}')


def _get_from_array(array, name):
    """Utility function to get value from array of tuples."""
    for line in array:
        if line[0] == name:
            return line[1]
    return ''


# ------------------------------------------------------------------------------------------
# MINI NEBULE LIBRARY - Core functionality for objects, links, and entities manipulation
# ------------------------------------------------------------------------------------------

class Nebule:
    """
    Mini librairie nebule pour la manipulation des objets, liens et entités.
    
    Cette classe fournit les fonctionnalités de base pour:
    - Vérifier et manipuler les identifiants de nœuds (NID)
    - Gérer les liens entre objets
    - Charger des objets depuis le système de fichiers
    - Interagir avec les entités
    """
    
    def __init__(self):
        """Initialize the nebule library."""
        self.initialized = False
        self.links_folder = LIB_LOCAL_LINKS_FOLDER
        self.objects_folder = LIB_LOCAL_OBJECTS_FOLDER
        self.entity_file = LIB_LOCAL_ENTITY_FILE
        self.environment_file = LIB_LOCAL_ENVIRONMENT_FILE
        
    def init(self):
        """
        Initialize the nebule library environment.
        
        Returns:
            bool: True if initialization succeeded, False otherwise
        """
        if not self.io_open():
            bootstrap_set_break('81', 'nebule.init')
            return False
        
        self.initialized = True
        log_add('Nebule library initialized', 'info', 'nebule.init', '00000001')
        return True
    
    def io_open(self):
        """
        Check and open I/O folders for links and objects.
        
        Returns:
            bool: True if folders exist or were created, False otherwise
        """
        if not self.io_check_link_folder() or not self.io_check_object_folder():
            return False
        return True
    
    def io_check_link_folder(self):
        """
        Check if links folder exists, create if needed and permitted.
        
        Returns:
            bool: True if folder exists, False otherwise
        """
        if not os.path.isdir(self.links_folder):
            self.io_create_link_folder()
        if not os.path.isdir(self.links_folder):
            bootstrap_set_break('22', 'io_check_link_folder')
            return False
        return True
    
    def io_check_object_folder(self):
        """
        Check if objects folder exists, create if needed and permitted.
        
        Returns:
            bool: True if folder exists, False otherwise
        """
        if not os.path.isdir(self.objects_folder):
            self.io_create_object_folder()
        if not os.path.isdir(self.objects_folder):
            bootstrap_set_break('24', 'io_check_object_folder')
            return False
        return True
    
    def io_create_link_folder(self):
        """
        Create the links folder if permitted.
        
        Returns:
            bool: True if folder exists after creation attempt
        """
        if not os.path.isdir(self.links_folder):
            os.mkdir(self.links_folder)
        return os.path.isdir(self.links_folder)
    
    def io_create_object_folder(self):
        """
        Create the objects folder if permitted.
        
        Returns:
            bool: True if folder exists after creation attempt
        """
        if not os.path.isdir(self.objects_folder):
            os.mkdir(self.objects_folder)
        return os.path.isdir(self.objects_folder)
    
    def io_check_node_have_link(self, nid):
        """
        Check if a node has a link file.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if link file exists
        """
        if nid == '':
            return False
        link_path = os.path.join(self.links_folder, nid)
        return os.path.isfile(link_path)
    
    def io_check_node_have_content(self, nid):
        """
        Check if a node has content in the objects folder.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            bool: True if content file exists
        """
        if nid == '':
            return False
        object_path = os.path.join(self.objects_folder, nid)
        return os.path.isfile(object_path)
    
    def nod_check_nid(self, nid='', permit_null=False, permit_zero=False):
        """
        Check if a node ID (NID) is valid.
        
        Args:
            nid (str): Node identifier to check
            permit_null (bool): Allow empty string
            permit_zero (bool): Allow '0' value
            
        Returns:
            bool: True if NID is valid
        """
        if permit_null and nid == '':
            return True
        if permit_zero and nid == '0':
            return True
        
        parts = nid.split('.')
        if len(parts) != 3:
            log_add(f"invalid parts count nid={nid}", 'warning', 'nod_check_nid', '00000002')
            return False
        
        hash_val = parts[0]
        algo_val = parts[1]
        size_val = parts[2]
        
        # Determine minimum size based on algorithm
        if algo_val == 'none' or algo_val == 'string':
            min_size = LIB_NID_MIN_NONE_SIZE
        else:
            min_size = LIB_NID_MIN_HASH_SIZE
        
        # Validate hash value
        valid_chars = 'abcdef0123456789'
        hash_ok = all(c in valid_chars for c in hash_val)
        
        if (hash_val == ''
                or not min_size < (len(hash_val) * 4) < LIB_NID_MAX_HASH_SIZE
                or not hash_ok):
            log_add(f"invalid hash value {hash_val}", 'warning', 'nod_check_nid', '00000003')
            return False
        
        # Validate algorithm value
        if algo_val == '' or not LIB_NID_MIN_ALGO_SIZE < len(algo_val) < LIB_NID_MAX_ALGO_SIZE:
            log_add(f"invalid algo value {algo_val}", 'warning', 'nod_check_nid', '00000004')
            return False
        
        # Validate size value
        if (size_val == '' or not min_size < int(size_val) < LIB_NID_MAX_HASH_SIZE
                or (len(hash_val) * 4) != int(size_val)):
            log_add(f"invalid size value {size_val}", 'warning', 'nod_check_nid', '00000005')
            return False
        
        return True
    
    def obj_load(self, oid):
        """
        Load an object from the objects folder.
        
        Args:
            oid (str): Object identifier
            
        Returns:
            str: Object content if found, empty string otherwise
        """
        if not self.nod_check_nid(oid):
            log_add(f"invalid oid {oid}", 'warning', 'obj_load', '00000006')
            return ''
        
        object_path = os.path.join(self.objects_folder, oid)
        if not os.path.isfile(object_path):
            log_add(f"object file not found: {object_path}", 'warning', 'obj_load', '00000007')
            return ''
        
        try:
            with open(object_path, 'r') as f:
                return f.read()
        except Exception as e:
            log_add(f"error reading object {oid}: {str(e)}", 'error', 'obj_load', '00000008')
            return ''
    
    def lnk_load(self, nid):
        """
        Load link information for a node.
        
        Args:
            nid (str): Node identifier
            
        Returns:
            str: Link content if found, empty string otherwise
        """
        if not self.nod_check_nid(nid):
            log_add(f"invalid nid {nid}", 'warning', 'lnk_load', '00000009')
            return ''
        
        link_path = os.path.join(self.links_folder, nid)
        if not os.path.isfile(link_path):
            log_add(f"link file not found: {link_path}", 'warning', 'lnk_load', '00000010')
            return ''
        
        try:
            with open(link_path, 'r') as f:
                return f.read()
        except Exception as e:
            log_add(f"error reading link {nid}: {str(e)}", 'error', 'lnk_load', '00000011')
            return ''
    
    def ent_load(self):
        """
        Load entity information from the entity file.
        
        Returns:
            str: Entity content if found, empty string otherwise
        """
        if not os.path.isfile(self.entity_file):
            log_add(f"entity file not found: {self.entity_file}", 'warning', 'ent_load', '00000012')
            return ''
        
        try:
            with open(self.entity_file, 'r') as f:
                return f.read()
        except Exception as e:
            log_add(f"error reading entity file: {str(e)}", 'error', 'ent_load', '00000013')
            return ''
    
    def app_load(self, application_name):
        """
        Load a Python application from the objects folder.
        
        This method searches for application files in the objects folder
        that match the application name pattern.
        
        Args:
            application_name (str): Name of the application to load
            
        Returns:
            module: The loaded Python module, or None if not found
        """
        # Search for application files in the objects folder
        app_files = []
        
        if not os.path.isdir(self.objects_folder):
            log_add(f"objects folder not found: {self.objects_folder}", 'error', 'app_load', '00000014')
            return None
        
        # Look for files that could be the application
        for filename in os.listdir(self.objects_folder):
            filepath = os.path.join(self.objects_folder, filename)
            if os.path.isfile(filepath) and filename.endswith('.py'):
                # Check if this file corresponds to the requested application
                if application_name in filename or filename.startswith(application_name):
                    app_files.append(filepath)
        
        if not app_files:
            log_add(f"no application files found for {application_name}", 'warning', 'app_load', '00000015')
            return None
        
        # Try to load the first matching application file
        app_path = app_files[0]
        module_name = Path(app_path).stem
        
        try:
            # Create a module spec and load it
            spec = importlib.util.spec_from_file_location(module_name, app_path)
            if spec is None:
                log_add(f"cannot create spec for {app_path}", 'error', 'app_load', '00000016')
                return None
            
            module = importlib.util.module_from_spec(spec)
            if module is None:
                log_add(f"cannot create module for {app_path}", 'error', 'app_load', '00000017')
                return None
            
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            log_add(f"application loaded: {module_name}", 'info', 'app_load', '00000018')
            return module
            
        except Exception as e:
            log_add(f"error loading application {app_path}: {str(e)}", 'error', 'app_load', '00000019')
            return None


# ------------------------------------------------------------------------------------------
# APPLICATION LOADING FUNCTIONS
# ------------------------------------------------------------------------------------------

nebulib = Nebule()


def load_library_from_objects():
    """
    Load the nebule library by searching for library objects in the 'o' folder
    and following links from the 'l' folder.
    
    This function simulates the behavior of bootstrap.php which:
    1. Initializes the environment
    2. Searches for and loads the library from objects in folder 'o'
    3. Uses links in folder 'l' to find the correct objects
    
    Returns:
        bool: True if library was loaded successfully
    """
    log_add('Starting library loading from objects', 'info', 'load_library_from_objects', '00000020')
    
    # First, ensure the nebule library itself is initialized
    if not nebulib.init():
        log_add('Failed to initialize nebule library', 'error', 'load_library_from_objects', '00000021')
        return False
    
    # The actual library loading will be done through the --application argument
    # which will specify which Python application to load from the objects folder
    log_add('Library environment initialized', 'info', 'load_library_from_objects', '00000022')
    return True


def load_python_application(application_name):
    """
    Load a Python application from the objects folder.
    
    Args:
        application_name (str): Name of the application to load
        
    Returns:
        bool: True if application was loaded and executed successfully
    """
    log_add(f'Loading Python application: {application_name}', 'info', 'load_python_application', '00000023')
    
    # Load the application module
    app_module = nebulib.app_load(application_name)
    if app_module is None:
        log_add(f'Failed to load application: {application_name}', 'error', 'load_python_application', '00000024')
        return False
    
    # Check if the application has a main function
    if hasattr(app_module, 'main'):
        try:
            app_module.main()
            log_add(f'Application {application_name} executed successfully', 'info', 'load_python_application', '00000025')
            return True
        except Exception as e:
            log_add(f'Error executing application {application_name}: {str(e)}', 'error', 'load_python_application', '00000026')
            traceback.print_exc()
            return False
    else:
        log_add(f'Application {application_name} has no main function', 'warning', 'load_python_application', '00000027')
        return False


# ------------------------------------------------------------------------------------------
# MAIN FUNCTION AND ENTRY POINT
# ------------------------------------------------------------------------------------------


def main():
    """
    Main entry point for nebule.py.
    
    This function:
    1. Parses command line arguments
    2. Initializes the nebule library
    3. Loads and executes the specified Python application
    """
    global nebulib
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Nebule Python Bootstrap - Load and execute Python applications from nebule objects'
    )
    parser.add_argument(
        '--application',
        type=str,
        required=True,
        help='Name of the Python application to load from the objects folder (o)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Enable debug logging if requested
    if args.debug:
        log_add('Debug mode enabled', 'info', 'main', '00000028')
    
    # Initialize the nebule library
    log_add('Initializing nebule library', 'info', 'main', '00000029')
    if not load_library_from_objects():
        log_add('Failed to load library from objects', 'error', 'main', '00000030')
        if len(bootstrapBreak) > 0:
            for break_info in bootstrapBreak:
                print(f"Break: {break_info[0]} - {break_info[1]}")
        sys.exit(1)
    
    # Load and execute the specified application
    log_add(f'Attempting to load application: {args.application}', 'info', 'main', '00000031')
    if not load_python_application(args.application):
        log_add(f'Failed to load application: {args.application}', 'error', 'main', '00000032')
        sys.exit(1)
    
    log_add('Application executed successfully', 'info', 'main', '00000033')


# ------------------------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
