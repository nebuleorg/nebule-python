#!/usr/bin/env python3
"""
Sign master entities script for nebule.
Version: 020261025

Generates and signs the bloc links that declare and recognize master entities:
- Each entity (including the puppetmaster) self-declares its own links:
  PEM public key type, PEM private key type, private key ownership (fork),
  name, location and algorithm. Those links are signed by the entity itself.
- The puppetmaster generates the recognition links that declare which entity
  is master (authority) of what. Those links are signed by the puppetmaster.

The signature is computed on the BH_BL content (see 502_link_register.php:
"la signature SIG calculée sur le contenu du bloc BH_BL") with RSA PKCS#1 v1.5
over sha2.256 (or sha2.512 for keys of 4096 bits and more), matching
prep_loop_code_master_php.sh sign_write_link() and lib_nebule/202_crypto_openssl.php.

Entity key objects (public and private) must already be present in the o/
folder of the target space: they are verified, not created. Name and
location string objects are created in o/ if absent, as the PHP prep does.

Links are written directly into the l/ folder: one line per NID referenced
by the link register, plus one line in the l/h history file.

Usage:
    python3 sign_master_entities.py \
        --space <space_folder> \
        --date 0YYYYMMDDHHMMSS \
        --puppetmaster-key <puppetmaster_private_key.pem> \
        --puppetmaster-password <password> \
        [--puppetmaster-name <name>] \
        [--puppetmaster-location <url>] \
        [--entity pub=<pub.pem>,priv=<priv.pem>,password=<pw>,name=<name>,location=<url>,algorithm=rsa.2048] \
        [--master <pub.pem|eid>,security,code,time,directory,local] \
        [--verbose]

Options:
    --space                  Root folder containing the o/ and l/ folders. Default: '.'
    --date                   Signature date, format 0YYYYMMDDHHMMSS (antidated).
                             Default: current time in the same format.
    --puppetmaster-key       Puppetmaster private key (PEM, possibly encrypted). Required.
    --puppetmaster-password  Puppetmaster private key password. Required.
    --puppetmaster-name      Puppetmaster name (optional).
    --puppetmaster-location  Puppetmaster location URL (optional).
    --entity                 Entity specification, repeatable, comma separated key=value
                             pairs. Only 'pub' is mandatory; 'priv' and 'password' are
                             required for self-declaration links:
                             pub=<pub.pem>,priv=<priv.pem>,password=<pw>,name=<name>,
                             location=<url>,algorithm=rsa.2048
    --master                 Master role declaration, repeatable, comma separated parts:
                             <entity_pub_key_path_or_eid>,<type>[,<type>...]
                             where type is one of: security, code, time, directory, local.
                             The recognition links are signed by the puppetmaster.
    --verbose                Show verbose output.
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
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

# Master (authority) types and their reference RID (from bootstrap.php)
RID_SECURITY_AUTHORITY = 'a4b210d4fb820a5b715509e501e36873eb9e27dca1dd591a98a5fc264fd2238adf4b489d.none.288'
RID_CODE_AUTHORITY = '2b9dd679451eaca14a50e7a65352f959fc3ad55efc572dcd009c526bc01ab3fe304d8e69.none.288'
RID_TIME_AUTHORITY = 'bab7966fd5b483f9556ac34e4fac9f778d0014149f196236064931378785d81cae5e7a6e.none.288'
RID_DIRECTORY_AUTHORITY = '0a4c1e7930a65672379616a2637b84542049b416053ac0d9345300189791f7f8e05f3ed4.none.288'

MASTER_GLOBAL_TYPES = {
    'security': RID_SECURITY_AUTHORITY,
    'code': RID_CODE_AUTHORITY,
    'time': RID_TIME_AUTHORITY,
    'directory': RID_DIRECTORY_AUTHORITY,
}
MASTER_LOCAL_TYPE = 'local'

# Reference strings whose sha2.256 hash is used as OID/RID in links
# (see prep_loop_code_master_php.sh)
REF_PEM_TYPE = 'application/x-pem-file'
REF_OBJ_TYPE = 'nebule/objet/type'
REF_OBJ_NAME = 'nebule/objet/nom'
REF_OBJ_ENTITY_LOCATION = 'nebule/objet/entite/localisation'
REF_OBJ_ENTITY_LOCAL_AUTHORITY = 'nebule/objet/entite/autorite/locale'
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
# Objects verification functions
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


def find_object(content, objects_dir, label, verbose=False):
    """
    Verify that a key object is present in the o/ folder and return its NID.

    The object must be named by the sha2.256 hash of its content, and its
    content must hash back to its name (integrity check).

    Args:
        content (bytes): Raw key file content
        objects_dir (str): Path to the objects directory
        label (str): Label for error messages
        verbose (bool): Show verbose output

    Returns:
        tuple: (nid, canonical_content) of the found object

    Raises:
        SystemExit: If the object is absent or corrupted
    """
    for candidate in canonical_contents(content):
        nid = format_node_id(compute_content_hash(candidate))
        object_path = os.path.join(objects_dir, nid)
        if os.path.isfile(object_path):
            with open(object_path, 'rb') as f:
                stored = f.read()
            if canonical_contents(stored)[0] != candidate:
                print(f"Error: Object {label} ({nid}) content mismatch in o/", file=sys.stderr)
                sys.exit(1)
            if verbose:
                print(f"  o/{nid} ({label})")
            return nid, candidate
    expected = ', '.join(
        format_node_id(compute_content_hash(candidate))
        for candidate in canonical_contents(content)
    )
    print(f"Error: Object for {label} not found in o/ folder: {objects_dir}", file=sys.stderr)
    print(f"       Expected object name(s): {expected}", file=sys.stderr)
    sys.exit(1)


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
        """Load keys, verify o/ objects presence and compute NIDs."""
        self.priv_nid, self.priv_content = find_object(
            self.priv_content, objects_dir, 'private key', verbose)
        self.pub_nid, self.pub_content = find_object(
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


def load_puppetmaster(key_path, password, name, location, objects_dir, verbose=False):
    """
    Load the puppetmaster entity from its private key.

    The public key is derived from the private key, as the PHP prep does:
        openssl rsa -in <key> -pubout

    Args:
        key_path (str): Path to the puppetmaster private key PEM file
        password (str): Private key password
        name (str): Puppetmaster name (may be empty)
        location (str): Puppetmaster location (may be empty)
        objects_dir (str): Path to the objects directory
        verbose (bool): Show verbose output

    Returns:
        Entity: The puppetmaster entity
    """
    with open(key_path, 'rb') as f:
        priv_content = f.read()
    private_key = load_private_key(priv_content, password)
    pub_content = derive_public_key_pem(private_key)
    entity = Entity(pub_content, priv_content, password, name, location)
    entity.load(objects_dir, verbose)
    return entity


def parse_entity_spec(spec):
    """
    Parse an --entity specification.

    Format: comma separated key=value pairs. Only 'pub' is positional-mandatory;
    'priv' and 'password' are required for the self-declaration links.

    Args:
        spec (str): The entity specification string

    Returns:
        dict: The entity attributes

    Raises:
        ValueError: If the specification is invalid
    """
    attributes = {
        'pub': '',
        'priv': '',
        'password': '',
        'name': '',
        'location': '',
        'algorithm': '',
    }
    for part in spec.split(','):
        part = part.strip()
        if part == '':
            continue
        if '=' not in part:
            raise ValueError(f"Invalid entity attribute (expected key=value): {part}")
        key, value = part.split('=', 1)
        if key not in attributes:
            raise ValueError(f"Unknown entity attribute: {key}")
        attributes[key] = value
    if attributes['pub'] == '':
        raise ValueError(f"Missing mandatory 'pub' attribute in entity spec: {spec}")
    if attributes['priv'] == '':
        raise ValueError(f"Missing mandatory 'priv' attribute in entity spec: {spec}")
    return attributes


def load_entities(entity_specs, objects_dir, verbose=False):
    """
    Load all entities from their specifications.

    Args:
        entity_specs (list): List of --entity specification strings
        objects_dir (str): Path to the objects directory
        verbose (bool): Show verbose output

    Returns:
        list: List of loaded Entity objects
    """
    entities = []
    for spec in entity_specs:
        attributes = parse_entity_spec(spec)
        with open(attributes['pub'], 'rb') as f:
            pub_content = f.read()
        with open(attributes['priv'], 'rb') as f:
            priv_content = f.read()
        entity = Entity(
            pub_content,
            priv_content,
            attributes['password'],
            attributes['name'],
            attributes['location'],
            attributes['algorithm'],
        )
        entity.load(objects_dir, verbose)
        entities.append(entity)
    return entities


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


def generate_recognition_links(entity, types, puppetmaster, date, links_dir, verbose=False):
    """
    Generate and write the recognition links that declare an entity as master.

    The recognition links are generated and signed by the puppetmaster only.
    Matches prep_loop_code_master_php.sh and lib_nebule/007_authorities.php
    _findEntityByType() filter (req='l', nid1=rid, nid3=rid, entity=nid2):

        l>RID_TYPE>eid>RID_TYPE           global authority of type TYPE

    and the local authority link:

        f>lauthOID>eid>                   local authority

    Args:
        entity (Entity): The entity recognized as master
        types (list): List of master types (security, code, time, directory, local)
        puppetmaster (Entity): The puppetmaster entity that signs
        date (str): Chronology in format 0YYYYMMDDHHMMSS
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        int: Number of links written

    Raises:
        ValueError: If a type is unknown
    """
    eid = entity.get_eid()
    lauth_oid = ref_node_id(REF_OBJ_ENTITY_LOCAL_AUTHORITY)

    unsigned_links = []
    for master_type in types:
        if master_type == MASTER_LOCAL_TYPE:
            unsigned_links.append(create_bh_bl(date, 'f', [lauth_oid, eid]))
        elif master_type in MASTER_GLOBAL_TYPES:
            rid = MASTER_GLOBAL_TYPES[master_type]
            unsigned_links.append(create_bh_bl(date, 'l', [rid, eid, rid]))
        else:
            raise ValueError(
                f"Unknown master type: {master_type} "
                f"(expected one of: {', '.join(list(MASTER_GLOBAL_TYPES) + [MASTER_LOCAL_TYPE])})"
            )

    count = 0
    for bh_bl in unsigned_links:
        bloc_link = sign_link(
            bh_bl, puppetmaster.get_eid(), puppetmaster.private_key, puppetmaster.hash_size)
        write_signed_link(bloc_link, links_dir, verbose)
        count += 1
    return count


# ------------------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate and sign nebule master entity declaration and recognition links'
    )
    parser.add_argument(
        '--space',
        type=str,
        default='.',
        help="Root folder containing the o/ and l/ folders. Default: '.'"
    )
    parser.add_argument(
        '--date',
        type=str,
        default='',
        help="Signature date in format 0YYYYMMDDHHMMSS (antidated). Default: current time"
    )
    parser.add_argument(
        '--puppetmaster-key',
        type=str,
        required=True,
        help='Path to the puppetmaster private key (PEM)'
    )
    parser.add_argument(
        '--puppetmaster-password',
        type=str,
        required=True,
        help='Password of the puppetmaster private key'
    )
    parser.add_argument(
        '--puppetmaster-name',
        type=str,
        default='',
        help='Puppetmaster name (optional)'
    )
    parser.add_argument(
        '--puppetmaster-location',
        type=str,
        default='',
        help='Puppetmaster location URL (optional)'
    )
    parser.add_argument(
        '--entity',
        type=str,
        action='append',
        default=[],
        dest='entities',
        help='Entity spec: pub=<pub.pem>,priv=<priv.pem>,password=<pw>,'
             'name=<name>,location=<url>,algorithm=rsa.2048 (repeatable)'
    )
    parser.add_argument(
        '--master',
        type=str,
        action='append',
        default=[],
        dest='masters',
        help='Master role: <pub_key_path_or_eid>,<type>[,<type>...] with type in '
             'security, code, time, directory, local (repeatable, signed by puppetmaster)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show verbose output'
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


def resolve_master_entities(master_specs, entities_by_pub_path, entities_by_eid):
    """
    Resolve --master specifications to (entity, types) pairs.

    The first comma separated part is either the public key file path of a
    declared entity, or a known entity EID. The following parts are the
    master types.

    Args:
        master_specs (list): List of --master specification strings
        entities_by_pub_path (dict): Entities indexed by public key file path
        entities_by_eid (dict): Entities indexed by EID (including puppetmaster)

    Returns:
        list: List of (Entity, [types]) tuples

    Raises:
        ValueError: If a specification is invalid or unresolvable
    """
    resolved = []
    for spec in master_specs:
        parts = [p.strip() for p in spec.split(',')]
        if len(parts) < 2:
            raise ValueError(f"Invalid master spec (need entity and at least one type): {spec}")
        entity_ref, types = parts[0], parts[1:]
        if entity_ref in entities_by_eid:
            entity = entities_by_eid[entity_ref]
        else:
            key_path = os.path.abspath(entity_ref)
            if key_path not in entities_by_pub_path:
                raise ValueError(
                    f"Master spec entity not found: {entity_ref} "
                    f"(not a known entity public key path nor EID)"
                )
            entity = entities_by_pub_path[key_path]
        resolved.append((entity, types))
    return resolved


def main():
    """Main entry point."""
    args = parse_args()

    # Resolve space folders
    space = os.path.abspath(args.space)
    objects_dir = os.path.join(space, LIB_LOCAL_OBJECTS_FOLDER)
    links_dir = os.path.join(space, LIB_LOCAL_LINKS_FOLDER)
    if not os.path.isdir(objects_dir):
        print(f"Error: Objects folder not found: {objects_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(links_dir):
        print(f"Error: Links folder not found: {links_dir}", file=sys.stderr)
        sys.exit(1)

    # Resolve signature date (antidated or current)
    if args.date == '':
        date = datetime.now().strftime('0%Y%m%d%H%M%S')
    else:
        date = args.date
    if not validate_date(date):
        print(f"Error: Invalid date (expected 0YYYYMMDDHHMMSS): {date}", file=sys.stderr)
        sys.exit(1)
    print(f"Signature date: {date}")

    # Load puppetmaster
    print(f"Loading puppetmaster from {args.puppetmaster_key}...")
    try:
        puppetmaster = load_puppetmaster(
            args.puppetmaster_key,
            args.puppetmaster_password,
            args.puppetmaster_name,
            args.puppetmaster_location,
            objects_dir,
            args.verbose,
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Puppetmaster EID: {puppetmaster.get_eid()}")

    # Load entities
    print(f"Loading {len(args.entities)} entity(ies)...")
    try:
        entities = load_entities(args.entities, objects_dir, args.verbose)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    for entity in entities:
        print(f"Entity EID: {entity.get_eid()}")

    # Index entities for master specs resolution
    entities_by_pub_path = {}
    entities_by_eid = {puppetmaster.get_eid(): puppetmaster}
    for attributes, entity in zip(args.entities, entities):
        entities_by_pub_path[os.path.abspath(parse_entity_spec(attributes)['pub'])] = entity
        entities_by_eid[entity.get_eid()] = entity

    # Resolve master specifications
    try:
        masters = resolve_master_entities(args.masters, entities_by_pub_path, entities_by_eid)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate self-declaration links, signed by each entity
    total = 0
    print('Generating entity self-declaration links...')
    total += generate_self_declaration_links(puppetmaster, date, objects_dir, links_dir, args.verbose)
    for entity in entities:
        total += generate_self_declaration_links(entity, date, objects_dir, links_dir, args.verbose)

    # Generate recognition links, signed by the puppetmaster
    print('Generating puppetmaster recognition links...')
    for entity, types in masters:
        print(f"  {entity.get_eid()}: master of {', '.join(types)}")
        total += generate_recognition_links(
            entity, types, puppetmaster, date, links_dir, args.verbose)

    print(f"Done: {total} bloc links written into {links_dir}/")
    return 0


if __name__ == '__main__':
    sys.exit(main())
