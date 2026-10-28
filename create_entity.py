#!/usr/bin/env python3
"""
Create entity script for nebule.
Version: 020261025

Creates a new entity and generates the bloc links that declare it, without
the web interface and without any external cryptographic command line tool.
All cryptographic operations (key pair generation and link signatures) are
done with the Python 'cryptography' library.

Two mutually exclusive key sources:
- --generate: create a new key pair. The key algorithm type is given with
  --algorithm (only 'rsa' is supported), the key size with --key-size. The
  private key is encrypted with the password when one is given. The keys are
  stored as objects in the o/ folder of the target space.
- --private-key: use an existing private key (PEM, possibly encrypted). The
  public key is derived from it, or read from --public-key when given.

The password is always required: either with --password, or it is asked
interactively by the script when the argument is absent.

The objects (public key, private key, name, location) are created in the o/
folder of the target space when absent. The entity self-declaration links
are written into the l/ folder, exactly as sign_master_entities.py does:

    l>pubE>pemOID>typeRID            public key is a PEM file
    l>privE<pemOID>typeRID           private key is a PEM file
    f>pubE>privE>PkeyRID             private key ownership
    l>pubE>nameOID>nameRID           name (if given)
    l>pubE>localOID>localRID         location (if given)
    l>pubE>rsaOID>algoRID            key algorithm

Those links are signed by the entity itself. The signature is computed on
the BH_BL content with RSA PKCS#1 v1.5 over sha2.256 (or sha2.512 for keys
of 4096 bits and more), matching prep_loop_code_master_php.sh
sign_write_link() and lib_nebule/202_crypto_openssl.php.

In non-verbose mode, the script only prints the generated entity EID.

Usage:
    python3 create_entity.py --generate \
        [--space <space_folder>] \
        [--password <password>] \
        [--algorithm rsa|rsa.<bits>] \
        [--key-size <bits>] \
        [--name <name>] \
        [--location <url>] \
        [--date 0YYYYMMDDHHMMSS] \
        [--verbose]

    python3 create_entity.py \
        --private-key <priv.pem> \
        [--public-key <pub.pem>] \
        [--space <space_folder>] \
        [--password <password>] \
        [--name <name>] \
        [--location <url>] \
        [--algorithm rsa.2048] \
        [--date 0YYYYMMDDHHMMSS] \
        [--verbose]

Options:
    --space                Root folder containing the o/ and l/ folders.
                           The folders are created when absent. Default: '.'
    --generate             Generate a new key pair for the entity.
    --private-key          Path to an existing entity private key (PEM,
                           possibly encrypted). Mutually exclusive with
                           --generate.
    --public-key           Path to the entity public key (PEM). Default:
                           derived from the private key.
    --algorithm            Key algorithm type for --generate: 'rsa' or
                           'rsa.<bits>' (default: 'rsa'). Also sets the
                           algorithm declared in the links when given with
                           a size, e.g. 'rsa.2048'.
    --key-size             Key size in bits for --generate. Default: 2048.
                           Overrides the size of --algorithm when both given.
    --password             Private key password. When absent, the script asks
                           for it interactively.
    --name                 Entity name (optional).
    --location             Entity location URL (optional).
    --date                 Signature date, format 0YYYYMMDDHHMMSS (antidated).
                           Default: current time in the same format.
    --verbose              Show verbose output.
"""

import argparse
import getpass
import hashlib
import os
import re
import sys
from datetime import datetime

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
except ImportError:
    print("Error: The 'cryptography' library is required: pip install cryptography", file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------------------------------
# Constants for nebule
# ------------------------------------------------------------------------------------------

# Reference code algorithm
LIB_REF_CODE_ALGO = 'sha2.256'

# Local storage configuration
LIB_LOCAL_LINKS_FOLDER = 'l'
LIB_LOCAL_OBJECTS_FOLDER = 'o'

# Link version
LIB_LINK_VERSION = '2:0'

# Default key algorithm and size for generation
DEFAULT_KEY_ALGORITHM = 'rsa'
DEFAULT_KEY_SIZE = 2048

# Reference strings whose sha2.256 hash is used as OID/RID in links
# (see prep_loop_code_master_php.sh)
REF_PEM_TYPE = 'application/x-pem-file'
REF_OBJ_TYPE = 'nebule/objet/type'
REF_OBJ_NAME = 'nebule/objet/nom'
REF_OBJ_ENTITY_LOCATION = 'nebule/objet/entite/localisation'
REF_OBJ_ENTITY_PRIVATE = 'nebule/objet/entite/prive'
REF_OBJ_ENTITY_ALGORITHM = 'nebule/objet/entite/algorithme'


# ------------------------------------------------------------------------------------------
# Hash and node ID functions
# ------------------------------------------------------------------------------------------

def compute_content_hash(content, algorithm='sha256'):
    """
    Compute the cryptographic hash of content bytes.

    The content MUST be bytes and is NOT modified before hash computation.

    Args:
        content (bytes): Raw bytes content to hash
        algorithm (str): Hash algorithm to use (default: 'sha256')

    Returns:
        str: Hexadecimal hash digest of the content
    """
    if not isinstance(content, bytes):
        raise TypeError(f"content must be bytes, got {type(content).__name__}")
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(content)
    return hash_obj.hexdigest()


def format_node_id(hash_value, algorithm=LIB_REF_CODE_ALGO):
    """
    Format a node ID (NID) according to nebule naming convention.

    Args:
        hash_value (str): The hash digest (hexadecimal, lowercase)
        algorithm (str): The hash algorithm (e.g. 'sha2.256')

    Returns:
        str: Formatted node ID: <hash>.<algorithm>
    """
    return f"{hash_value}.{algorithm}"


def ref_node_id(reference):
    """
    Compute the node ID of a reference string.

    The reference strings are hashed with sha2.256, exactly as done in
    prep_loop_code_master_php.sh:
        echo -n 'nebule/objet/type' | sha256sum

    Args:
        reference (str): The reference string

    Returns:
        str: Formatted node ID of the reference
    """
    return format_node_id(compute_content_hash(reference.encode('utf-8')))


# ------------------------------------------------------------------------------------------
# Key and signature functions
# ------------------------------------------------------------------------------------------

def load_private_key(content, password):
    """
    Load a private key from PEM content.

    Args:
        content (bytes): Private key PEM content
        password (str): Private key password ('' if not encrypted)

    Returns:
        The private key object

    Raises:
        ValueError: If the key cannot be loaded
    """
    pwd = password.encode('utf-8') if password != '' else None
    try:
        return serialization.load_pem_private_key(content, password=pwd)
    except Exception as e:
        raise ValueError(f"Unable to load private key: {e}")


def generate_key_pair(key_algorithm, key_size):
    """
    Generate a new key pair.

    Args:
        key_algorithm (str): Key algorithm type ('rsa')
        key_size (int): Key size in bits

    Returns:
        The private key object

    Raises:
        ValueError: If the algorithm is unsupported or the size invalid
    """
    if key_algorithm != 'rsa':
        raise ValueError(
            f"Unsupported key algorithm: {key_algorithm} (only 'rsa' is supported)")
    if key_size < 512:
        raise ValueError(f"Invalid key size: {key_size} (minimum is 512 bits)")
    return rsa.generate_private_key(public_exponent=65537, key_size=key_size)


def serialize_private_key_pem(private_key, password):
    """
    Serialize a private key to PEM content, encrypted with the password.

    Args:
        private_key: The private key object
        password (str): Encryption password ('' for no encryption)

    Returns:
        bytes: Private key PEM content
    """
    if password != '':
        encryption = serialization.BestAvailableEncryption(password.encode('utf-8'))
    else:
        encryption = serialization.NoEncryption()
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption,
    )


def derive_public_key_pem(private_key):
    """
    Derive the public key PEM from a private key.

    Matches: openssl rsa -in <key> -pubout
    (SubjectPublicKeyInfo, no trailing newline after bash $() stripping)

    Args:
        private_key: The private key object

    Returns:
        bytes: Public key PEM content
    """
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def get_key_bits(key_object):
    """
    Get the key size in bits.

    Args:
        key_object: The key object (public or private)

    Returns:
        int: Key size in bits
    """
    return key_object.key_size


def get_signature_hash_size(key_object):
    """
    Compute the signature hash size for a key.

    Follows prep_loop_code_master_php.sh: keys of 4096 bits are signed with
    sha2.512 (suffix .sha2.512), smaller keys with sha2.256 (suffix .sha2.256).

    Args:
        key_object: The private key object used to sign

    Returns:
        int: Hash size in bits (512 or 256)
    """
    if get_key_bits(key_object) >= 4096:
        return 512
    return 256


def sign_bh_bl(bh_bl, private_key, hash_size):
    """
    Sign the BH_BL content of a link.

    Matches prep_loop_code_master_php.sh:
        echo -n "${link}" | openssl dgst -hex -sha${size} -sign <key> -passin pass:<password>
    which is RSA PKCS#1 v1.5 over the sha digest.

    Args:
        bh_bl (str): The BH_BL content to sign
        private_key: The private key object
        hash_size (int): Hash size in bits (512 or 256)

    Returns:
        str: The signature (hexadecimal)
    """
    if hash_size == 512:
        hash_algo = hashes.SHA512()
    else:
        hash_algo = hashes.SHA256()
    signature = private_key.sign(
        bh_bl.encode('utf-8'),
        padding.PKCS1v15(),
        hash_algo,
    )
    return signature.hex()


# ------------------------------------------------------------------------------------------
# Link building and writing functions
# ------------------------------------------------------------------------------------------

def create_bh():
    """
    Create Block Header (BH) for a link.

    Returns:
        str: Block Header string
    """
    return f"nebule:link/{LIB_LINK_VERSION}"


def create_bh_bl(date, req_type, nids):
    """
    Create the BH_BL content (unsigned link) for a link.

    Format: BH_BL = nebule:link/2:0_0>CHR/REQ>NID1>NID2>...

    Args:
        date (str): Chronology in format 0YYYYMMDDHHMMSS
        req_type (str): Request type ('l', 'f', ...)
        nids (list): List of node IDs (1 to 4)

    Returns:
        str: The BH_BL content string
    """
    if not nids:
        raise ValueError("At least one NID is required")
    if len(nids) > 4:
        raise ValueError(f"Too many NIDs: {len(nids)} provided, maximum allowed is 4")
    bl = f"0>{date}/{req_type}>{'>'.join(nids)}"
    return f"{create_bh()}_{bl}"


def sign_link(bh_bl, signer_eid, private_key, hash_size):
    """
    Sign an unsigned link and return the complete bloc link BH_BL_BS.

    Matches prep_loop_code_master_php.sh:
        flink="${link}_${eid}>${slink}.sha2.${size}"

    Args:
        bh_bl (str): The BH_BL content to sign
        signer_eid (str): Signer entity ID (NID of its public key)
        private_key: The signer private key object
        hash_size (int): Hash size in bits (512 or 256)

    Returns:
        str: Complete bloc link string BH_BL_BS
    """
    signature = sign_bh_bl(bh_bl, private_key, hash_size)
    return f"{bh_bl}_{signer_eid}>{signature}.sha2.{hash_size}"


def extract_nids_from_bloc_link(bloc_link):
    """
    Extract NID1 to NID4 from the link register of a bloc link.

    Matches prep_loop_code_master_php.sh:
        echo "${link}" | cut -d_ -f2 | cut -d/ -f2 | cut -d '>' -f2..5

    Args:
        bloc_link (str): Complete bloc link string BH_BL_BS

    Returns:
        list: List of non-empty NIDs from the link register
    """
    bl_bs = bloc_link.split('_', 1)
    if len(bl_bs) < 2:
        return []
    bl = bl_bs[1].split('_', 1)[0]
    parts = bl.split('/', 1)
    if len(parts) < 2:
        return []
    rl_parts = parts[1].split('>')
    nids = rl_parts[1:5]
    return [nid for nid in nids if nid != '']


def write_link_file(link_string, nid, links_dir):
    """
    Append a link string to a node's link file if not already present.

    Matches prep_loop_code_master_php.sh sign_write_link().

    Args:
        link_string (str): Complete bloc link string
        nid (str): Node ID for the file
        links_dir (str): Path to the links directory

    Returns:
        bool: True if the link was written, False if it was already present
    """
    link_file = os.path.join(links_dir, nid)
    if os.path.exists(link_file):
        with open(link_file, 'r', encoding='utf-8') as f:
            existing = f.read()
        if link_string in existing:
            return False
    with open(link_file, 'a', encoding='utf-8') as f:
        f.write(link_string + '\n')
    return True


def write_signed_link(bloc_link, links_dir, verbose=False):
    """
    Write a signed bloc link into the l/ folder.

    The link line is appended to the file of each NID referenced by the link
    register (deduplicated), and to the l/h history file.

    Matches prep_loop_code_master_php.sh sign_write_link().

    Args:
        bloc_link (str): Complete bloc link string BH_BL_BS
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        list: The NIDs whose file was written
    """
    written = []
    for nid in extract_nids_from_bloc_link(bloc_link):
        if write_link_file(bloc_link, nid, links_dir):
            written.append(nid)
            if verbose:
                print(f"  + l/{nid}")
    # History file: always appended, no dedup, as in the PHP reference
    history_file = os.path.join(links_dir, 'h')
    with open(history_file, 'a', encoding='utf-8') as f:
        f.write(bloc_link + '\n')
    return written


# ------------------------------------------------------------------------------------------
# Objects creation functions
# ------------------------------------------------------------------------------------------

def canonical_contents(content):
    """
    Return the candidate canonical contents of a key file.

    The PHP prep stores key objects without trailing newline
    (echo -n "${key}" after bash $() stripping). Both the raw content and the
    content stripped of trailing newlines are candidates.

    Args:
        content (bytes): Raw file content

    Returns:
        list: Candidate contents, most canonical first
    """
    stripped = content.rstrip(b'\n')
    if stripped == content:
        return [content]
    return [stripped, content]


def ensure_object(content, objects_dir, label, verbose=False):
    """
    Write an object into the o/ folder if absent, and return its NID.

    The object is named by the sha2.256 hash of its canonical content
    (trailing newlines stripped, as the PHP prep does). When the object is
    already present, its content is verified.

    Args:
        content (bytes): Raw object content
        objects_dir (str): Path to the objects directory
        label (str): Label for verbose output and error messages
        verbose (bool): Show verbose output

    Returns:
        tuple: (nid, canonical_content) of the object

    Raises:
        SystemExit: If the present object content mismatches
    """
    canonical = canonical_contents(content)[0]
    nid = format_node_id(compute_content_hash(canonical))
    object_path = os.path.join(objects_dir, nid)
    if os.path.isfile(object_path):
        with open(object_path, 'rb') as f:
            stored = f.read()
        if canonical_contents(stored)[0] != canonical:
            print(f"Error: Object {label} ({nid}) content mismatch in o/", file=sys.stderr)
            sys.exit(1)
        if verbose:
            print(f"  o/{nid} ({label})")
    else:
        with open(object_path, 'wb') as f:
            f.write(canonical)
        if verbose:
            print(f"  o/{nid} ({label}, created)")
    return nid, canonical


def write_object(content, objects_dir, verbose=False):
    """
    Write a string object into the o/ folder if absent, and return its NID.

    Used for name and location objects, as the PHP prep does:
        echo -n 'puppetmaster' > "${SPACE}/o/${entityNameOID}"

    Args:
        content (str): Object content string
        objects_dir (str): Path to the objects directory
        verbose (bool): Show verbose output

    Returns:
        str: The object NID
    """
    content_bytes = content.encode('utf-8')
    nid = format_node_id(compute_content_hash(content_bytes))
    object_path = os.path.join(objects_dir, nid)
    if not os.path.isfile(object_path):
        with open(object_path, 'wb') as f:
            f.write(content_bytes)
        if verbose:
            print(f"  o/{nid} (created)")
    return nid


# ------------------------------------------------------------------------------------------
# Entity functions
# ------------------------------------------------------------------------------------------

class Entity:
    """An entity with its keys and self-declaration attributes."""

    def __init__(self, pub_content, priv_content, password,
                 name='', location='', algorithm=''):
        self.pub_content = pub_content
        self.priv_content = priv_content
        self.password = password
        self.name = name
        self.location = location
        self.algorithm = algorithm
        self.private_key = None
        self.pub_nid = ''
        self.priv_nid = ''
        self.bits = 0
        self.hash_size = 256

    def load(self, objects_dir, verbose=False):
        """Load keys, create o/ objects when absent and compute NIDs."""
        self.priv_nid, self.priv_content = ensure_object(
            self.priv_content, objects_dir, 'private key', verbose)
        self.pub_nid, self.pub_content = ensure_object(
            self.pub_content, objects_dir, 'public key', verbose)
        self.private_key = load_private_key(self.priv_content, self.password)
        self.bits = get_key_bits(self.private_key)
        self.hash_size = get_signature_hash_size(self.private_key)
        # Default algorithm derived from the key size
        if self.algorithm == '':
            self.algorithm = f"rsa.{self.bits}"

    def get_eid(self):
        """Return the entity ID (NID of its public key)."""
        return self.pub_nid


def parse_algorithm(spec):
    """
    Parse an --algorithm specification.

    Format: '<type>' or '<type>.<size>', e.g. 'rsa' or 'rsa.4096'.

    Args:
        spec (str): The algorithm specification string

    Returns:
        tuple: (type, size) with size None when absent

    Raises:
        ValueError: If the specification is invalid
    """
    parts = spec.split('.')
    if len(parts) == 1:
        return parts[0], None
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0], int(parts[1])
    raise ValueError(f"Invalid algorithm (expected 'rsa' or 'rsa.<size>'): {spec}")


# ------------------------------------------------------------------------------------------
# Link generation functions
# ------------------------------------------------------------------------------------------

def generate_self_declaration_links(entity, date, objects_dir, links_dir, verbose=False):
    """
    Generate and write the self-declaration links of an entity.

    Each entity is responsible and owner of the links that concern it, so
    those links are signed by the entity itself. Matches the links list of
    prep_loop_code_master_php.sh:

        l>pubE>pemOID>typeRID            public key is a PEM file (default)
        l>privE<pemOID>typeRID           private key is a PEM file
        f>pubE>privE>PkeyRID             private key ownership
        l>pubE>nameOID>nameRID           name (if given)
        l>pubE>localOID>localRID         location (if given)
        l>pubE>rsaOID>algoRID            key algorithm

    Args:
        entity (Entity): The entity that self-declares and signs
        date (str): Chronology in format 0YYYYMMDDHHMMSS
        objects_dir (str): Path to the objects directory
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        int: Number of links written
    """
    eid = entity.get_eid()
    pem_oid = ref_node_id(REF_PEM_TYPE)
    type_rid = ref_node_id(REF_OBJ_TYPE)
    name_rid = ref_node_id(REF_OBJ_NAME)
    local_rid = ref_node_id(REF_OBJ_ENTITY_LOCATION)
    private_rid = ref_node_id(REF_OBJ_ENTITY_PRIVATE)
    algo_rid = ref_node_id(REF_OBJ_ENTITY_ALGORITHM)

    unsigned_links = [
        create_bh_bl(date, 'l', [eid, pem_oid, type_rid]),
        create_bh_bl(date, 'l', [entity.priv_nid, pem_oid, type_rid]),
        create_bh_bl(date, 'f', [eid, entity.priv_nid, private_rid]),
    ]
    if entity.name != '':
        name_oid = write_object(entity.name, objects_dir, verbose)
        unsigned_links.append(create_bh_bl(date, 'l', [eid, name_oid, name_rid]))
    if entity.location != '':
        local_oid = write_object(entity.location, objects_dir, verbose)
        unsigned_links.append(create_bh_bl(date, 'l', [eid, local_oid, local_rid]))
    if entity.algorithm != '':
        algo_oid = ref_node_id(entity.algorithm)
        unsigned_links.append(create_bh_bl(date, 'l', [eid, algo_oid, algo_rid]))

    count = 0
    for bh_bl in unsigned_links:
        bloc_link = sign_link(bh_bl, eid, entity.private_key, entity.hash_size)
        write_signed_link(bloc_link, links_dir, verbose)
        count += 1
    return count


# ------------------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Create a nebule entity: generate or load its key pair, '
                    'create its objects and sign its self-declaration links'
    )
    parser.add_argument(
        '--space',
        type=str,
        default='.',
        help="Root folder containing the o/ and l/ folders. The folders are "
             "created when absent. Default: '.'"
    )
    parser.add_argument(
        '--date',
        type=str,
        default='',
        help="Signature date in format 0YYYYMMDDHHMMSS (antidated). Default: current time"
    )
    key_source = parser.add_mutually_exclusive_group(required=True)
    key_source.add_argument(
        '--generate',
        action='store_true',
        help='Generate a new key pair for the entity'
    )
    key_source.add_argument(
        '--private-key',
        type=str,
        default=None,
        help='Path to an existing entity private key (PEM, possibly encrypted)'
    )
    parser.add_argument(
        '--public-key',
        type=str,
        default='',
        help='Path to the entity public key (PEM). Default: derived from the private key'
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default=DEFAULT_KEY_ALGORITHM,
        help="Key algorithm type for --generate: 'rsa' or 'rsa.<size>' "
             f"(default: {DEFAULT_KEY_ALGORITHM})"
    )
    parser.add_argument(
        '--key-size',
        type=int,
        default=0,
        help=f"Key size in bits for --generate. Default: {DEFAULT_KEY_SIZE}"
    )
    parser.add_argument(
        '--password',
        type=str,
        default=None,
        help='Private key password. When absent, the script asks for it interactively'
    )
    parser.add_argument(
        '--name',
        type=str,
        default='',
        help='Entity name (optional)'
    )
    parser.add_argument(
        '--location',
        type=str,
        default='',
        help='Entity location URL (optional)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show verbose output. Default: only print the entity EID'
    )
    return parser.parse_args()


# ------------------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------------------

def validate_date(date):
    """
    Validate a chronology date in format 0YYYYMMDDHHMMSS.

    Args:
        date (str): The date string

    Returns:
        bool: True if the date is valid
    """
    if not re.fullmatch(r'0\d{14}', date):
        return False
    try:
        datetime.strptime(date[1:], '%Y%m%d%H%M%S')
    except ValueError:
        return False
    return True


def resolve_password(argument):
    """
    Resolve the private key password.

    The password is always required: it comes either from the --password
    argument, or from an interactive question of the script.

    Args:
        argument (str): The --password argument value, None when absent

    Returns:
        str: The password (possibly '')
    """
    if argument is not None:
        return argument
    return getpass.getpass('Entity private key password: ')


def build_entity_from_private_key(priv_content, password, pub_content=''):
    """
    Build the raw entity contents (public, private) from a private key.

    The public key is derived from the private key, as the PHP prep does:
        openssl rsa -in <key> -pubout

    Args:
        priv_content (bytes): Private key PEM content
        password (str): Private key password
        pub_content (bytes): Given public key PEM content ('' to derive)

    Returns:
        tuple: (pub_content, priv_content, private_key)

    Raises:
        ValueError: If the key cannot be loaded or does not match
    """
    private_key = load_private_key(priv_content, password)
    derived_pub = derive_public_key_pem(private_key)
    if pub_content != '':
        if canonical_contents(pub_content)[0] != canonical_contents(derived_pub)[0]:
            raise ValueError("The given public key does not match the private key")
        return pub_content, priv_content, private_key
    return derived_pub, priv_content, private_key


def main():
    """Main entry point."""
    args = parse_args()

    # Resolve space folders, created when absent
    space = os.path.abspath(args.space)
    objects_dir = os.path.join(space, LIB_LOCAL_OBJECTS_FOLDER)
    links_dir = os.path.join(space, LIB_LOCAL_LINKS_FOLDER)
    os.makedirs(objects_dir, exist_ok=True)
    os.makedirs(links_dir, exist_ok=True)

    # Resolve signature date (antidated or current)
    if args.date == '':
        date = datetime.now().strftime('0%Y%m%d%H%M%S')
    else:
        date = args.date
    if not validate_date(date):
        print(f"Error: Invalid date (expected 0YYYYMMDDHHMMSS): {date}", file=sys.stderr)
        sys.exit(1)

    # Resolve the algorithm specification
    try:
        key_algorithm, algorithm_size = parse_algorithm(args.algorithm)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    if args.generate and algorithm_size is not None and args.key_size <= 0:
        args.key_size = algorithm_size

    # Resolve the password: always required, from argument or interactive question
    password = resolve_password(args.password)

    # Resolve the key pair: generated or loaded from arguments
    if args.generate:
        key_size = args.key_size if args.key_size > 0 else DEFAULT_KEY_SIZE
        if args.verbose:
            print(f"Generating {key_algorithm}.{key_size} key pair...")
        try:
            private_key = generate_key_pair(key_algorithm, key_size)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        priv_content = serialize_private_key_pem(private_key, password)
        pub_content = derive_public_key_pem(private_key)
        declared_algorithm = (
            f"{key_algorithm}.{algorithm_size}" if algorithm_size is not None else '')
    else:
        if args.verbose:
            print(f"Loading entity from {args.private_key}...")
        with open(args.private_key, 'rb') as f:
            priv_content = f.read()
        pub_content = ''
        if args.public_key != '':
            with open(args.public_key, 'rb') as f:
                pub_content = f.read()
        try:
            pub_content, priv_content, _ = build_entity_from_private_key(
                priv_content, password, pub_content)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        declared_algorithm = (
            f"{key_algorithm}.{algorithm_size}" if algorithm_size is not None else '')

    # Load the entity: create the o/ key objects when absent
    entity = Entity(
        pub_content,
        priv_content,
        password,
        args.name,
        args.location,
        declared_algorithm,
    )
    entity.load(objects_dir, args.verbose)
    eid = entity.get_eid()
    if args.verbose:
        print(f"Entity EID: {eid}")
        print(f"Entity algorithm: {entity.algorithm}")
        print('Generating entity self-declaration links...')
    generate_self_declaration_links(entity, date, objects_dir, links_dir, args.verbose)

    if not args.verbose:
        print(eid)
    return 0


if __name__ == '__main__':
    sys.exit(main())
