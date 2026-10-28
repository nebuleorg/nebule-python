#!/usr/bin/env python3
"""
Sign master entities script for nebule.
Version: 020261028

Signs the bloc links that recognize master entities. Entities are created and
self-declared with create_entity.py: this script neither generates entities
nor objects, it only generates the recognition links signed by the
puppetmaster that declare which entity is master (authority) of what:

    l>RID_TYPE>eid>RID_TYPE            global authority of type TYPE

with TYPE in: security, code, time, directory.

Each entity designated by EID (puppetmaster and masters) must already be
present in the o/ folder of the target space: its public key object is read
from o/, and its consistency and its links are verified with the functions of
verify_entity.py. Only structurally valid links signed by the entity, with a
verified signature, are taken into account. Each entity can also be verified
standalone with:

    python3 verify_entity.py --entity <eid> --space <space>

The puppetmaster private key is not given as a file: it is looked up from the
puppetmaster self-declaration links (private key ownership fork), exactly as
verify_entity.py does, and loaded with the password. The password is always
required: either with --puppetmaster-password, or it is asked interactively
by the script when the argument is absent.

The signature is computed on the BH_BL content (see 502_link_register.php:
"la signature SIG calculée sur le contenu du bloc BH_BL") with RSA PKCS#1 v1.5
over sha2.256 (or sha2.512 for keys of 4096 bits and more), matching
prep_loop_code_master_php.sh sign_write_link() and lib_nebule/202_crypto_openssl.php.

Links are written directly into the l/ folder: one line per NID referenced
by the link register, plus one line in the l/h history file.

Usage:
    python3 sign_master_entities.py \
        --space <space_folder> \
        --puppetmaster <eid> \
        [--puppetmaster-password <password>] \
        [--date 0YYYYMMDDHHMMSS] \
        [--master <eid>,<type>[,<type>...]] \
        [--verbose]

Options:
    --space                  Root folder containing the o/ and l/ folders. Default: '.'
    --date                   Signature date, format 0YYYYMMDDHHMMSS (antidated).
                             Default: current time in the same format.
    --puppetmaster           Puppetmaster entity ID (NID of its public key,
                             present in o/). Required.
    --puppetmaster-password  Password of the puppetmaster private key. When
                             absent, the script asks for it interactively.
    --master                 Master role declaration, repeatable, comma
                             separated parts: <eid>,<type>[,<type>...] where
                             type is one of: security, code, time, directory.
                             The recognition links are signed by the puppetmaster.
    --verbose                Show verbose output.
"""

import argparse
import getpass
import os
import re
import sys
from datetime import datetime

try:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    print("Error: The 'cryptography' library is required: pip install cryptography", file=sys.stderr)
    sys.exit(1)

try:
    import verify_entity
except ImportError:
    print("Error: The 'verify_entity.py' script must be present in the same folder", file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------------------------------
# Constants for nebule
# ------------------------------------------------------------------------------------------

# Local storage configuration
LIB_LOCAL_LINKS_FOLDER = 'l'
LIB_LOCAL_OBJECTS_FOLDER = 'o'

# Link version
LIB_LINK_VERSION = '2:0'

# Node ID format (see AGENTS.md: <hash>.<algo>[.<size>], no underscore)
NID_REGEX = r'[0-9a-f]+\.[0-9a-z]+(?:\.\d+)?'

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


# ------------------------------------------------------------------------------------------
# Key and signature functions
# ------------------------------------------------------------------------------------------

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
# Entity verification functions (reuse of verify_entity.py)
# ------------------------------------------------------------------------------------------

def validate_eid(eid):
    """
    Validate an entity ID (NID of its public key).

    Args:
        eid (str): The entity ID

    Returns:
        str: The entity ID

    Raises:
        ValueError: If the entity ID format is invalid
    """
    if not re.fullmatch(NID_REGEX, eid):
        raise ValueError(f"Invalid entity ID: {eid}")
    return eid


def load_entity_public_key(eid, objects_dir):
    """
    Read and load the entity public key object from the o/ folder.

    The object must be present and intact: its content must hash back to its
    name, as verify_entity.py checks.

    Args:
        eid (str): The entity ID (NID of its public key)
        objects_dir (str): Path to the objects directory

    Returns:
        tuple: (pub_content, pub_key) of the entity

    Raises:
        ValueError: If the object is absent, corrupted or not a public key
    """
    pub_content, pub_err = verify_entity.read_object(objects_dir, eid, 'public key')
    if pub_err != '':
        raise ValueError(pub_err)
    try:
        pub_key = verify_entity.load_public_key(pub_content)
    except ValueError as e:
        raise ValueError(f"entity {eid} public key object is not a valid public key PEM ({e})")
    return pub_content, pub_key


def collect_valid_entity_links(eid, pub_key, links_dir, verbose=False):
    """
    Collect the links signed by the entity, verifying the entity signatures.

    Reuses the parsing and signature verification functions of
    verify_entity.py: only structurally valid links signed by the entity,
    with a verified signature, are taken into account.

    Args:
        eid (str): The entity ID
        pub_key: The entity public key object
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        dict: 'total' (links in the space), 'signed' (links signed by the
            entity), 'valid' (of them, the ones with a verified entity
            signature), 'sigs_total', 'sigs_ok', 'links' (the valid parsed
            links)
    """
    all_links = verify_entity.read_links(links_dir)
    entity_links = []
    for link in all_links:
        parsed, err = verify_entity.parse_bloc_link(link)
        if parsed is None:
            if verbose:
                print(f"  unparseable link: {err}")
            continue
        if any(s['eid'] == eid for s in parsed['signers']):
            entity_links.append((link, parsed))
    valid_links = []
    sigs_total = 0
    sigs_ok = 0
    for link, parsed in entity_links:
        bh_bl = '_'.join(link.split('_')[:2])
        link_ok = True
        for signer in parsed['signers']:
            if signer['eid'] != eid:
                continue
            sigs_total += 1
            if verify_entity.verify_signature(bh_bl, signer['sig'], signer['size'], pub_key):
                sigs_ok += 1
            else:
                link_ok = False
                if verbose:
                    print(f"  invalid entity signature on link "
                          f"{parsed['req']}>{'>'.join(parsed['nids'])}")
        if link_ok:
            valid_links.append(parsed)
    return {
        'total': len(all_links),
        'signed': len(entity_links),
        'valid': len(valid_links),
        'sigs_total': sigs_total,
        'sigs_ok': sigs_ok,
        'links': valid_links,
    }


def check_entity_consistency(eid, stats, verbose=False):
    """
    Check the entity self-declaration consistency from its valid links.

    Follows the verify_entity.py final status, minus the key pair check that
    needs the entity private key password: the public key must be declared as
    a PEM file, the key algorithm must be declared, and all the links signed
    by the entity must have a verified signature.

    Args:
        eid (str): The entity ID
        stats (dict): The result of collect_valid_entity_links()
        verbose (bool): Show verbose output

    Returns:
        tuple: (problems, declarations, algorithm) with problems as a list of
            error strings, declarations as the verify_entity.py
            find_declarations() result, algorithm as the declared key
            algorithm ('' when absent)
    """
    declarations = verify_entity.find_declarations(stats['links'], eid)
    algorithm = ''
    for size in verify_entity.RSA_KEY_SIZES:
        if verify_entity.ref_node_id(f"rsa.{size}") in declarations['algorithm']:
            algorithm = f"rsa.{size}"
            break
    problems = []
    if stats['signed'] == 0:
        problems.append('no link signed by the entity in l/')
    elif stats['valid'] != stats['signed']:
        problems.append(
            f"{stats['signed'] - stats['valid']} link(s) signed by the entity "
            f"have an invalid signature")
    if not declarations['pub_pem']:
        problems.append('public key not declared as a PEM file by a valid signed link')
    if algorithm == '':
        problems.append('key algorithm not declared by a valid signed link')
    if verbose:
        print(f"  links: {stats['total']} in l/, {stats['signed']} signed by the entity, "
              f"{stats['valid']} valid ({stats['sigs_ok']}/{stats['sigs_total']} signatures valid)")
    return problems, declarations, algorithm


def find_private_key(eid, pub_content, password, declarations, objects_dir, verbose=False):
    """
    Look up the entity private key from its self-declaration links.

    The private key ownership fork (f>eid>privNID>priveRID) gives the private
    key objects, which must also be declared as PEM files, exactly as
    verify_entity.py does. The retained key loads with the password and
    derives the entity public key.

    Args:
        eid (str): The entity ID
        pub_content (bytes): The entity public key object content
        password (str): The private key password
        declarations (dict): The verify_entity.py find_declarations() result
        objects_dir (str): Path to the objects directory
        verbose (bool): Show verbose output

    Returns:
        tuple: (private_key, priv_nid) of the found private key

    Raises:
        ValueError: If no private key object matches the entity
    """
    candidates = declarations['fork'] & declarations['priv_pem']
    for candidate in sorted(candidates):
        priv_content, priv_err = verify_entity.read_object(
            objects_dir, candidate, 'private key')
        if priv_err != '':
            if verbose:
                print(f"  private key {candidate}: {priv_err}")
            continue
        try:
            private_key = verify_entity.load_private_key(priv_content, password)
        except ValueError:
            if verbose:
                print(f"  private key {candidate}: does not load with the given password")
            continue
        derived = verify_entity.derive_public_key_pem(private_key)
        if verify_entity.canonical_contents(derived)[0] \
                == verify_entity.canonical_contents(pub_content)[0]:
            return private_key, candidate
        if verbose:
            print(f"  private key {candidate}: does not match the entity public key")
    if not candidates:
        raise ValueError(
            f"entity {eid} private key not declared by valid signed links "
            '(ownership or PEM declaration missing)')
    raise ValueError(
        f"entity {eid} private key not found: no private key object matches "
        'the entity public key with the given password')


def verify_master_entity(eid, objects_dir, links_dir, verbose=False):
    """
    Verify a master entity designated by EID.

    The entity public key object must be present in the o/ folder, and the
    entity consistency and its links are verified with the functions of
    verify_entity.py. The key pair is not checked: the entity private key
    password is not given for master entities.

    Args:
        eid (str): The entity ID
        objects_dir (str): Path to the objects directory
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Raises:
        ValueError: If the entity is absent or inconsistent
    """
    pub_content, pub_key = load_entity_public_key(eid, objects_dir)
    stats = collect_valid_entity_links(eid, pub_key, links_dir, verbose)
    problems, _, _ = check_entity_consistency(eid, stats, verbose)
    if problems:
        raise ValueError(
            f"inconsistent master entity {eid}: {'; '.join(problems)}")


# ------------------------------------------------------------------------------------------
# Puppetmaster functions
# ------------------------------------------------------------------------------------------

class Puppetmaster:
    """The puppetmaster entity: its EID, its public key and its private key."""

    def __init__(self, eid, pub_content, pub_key, private_key, priv_nid):
        self.eid = eid
        self.pub_content = pub_content
        self.pub_key = pub_key
        self.private_key = private_key
        self.priv_nid = priv_nid
        self.bits = get_key_bits(private_key)
        self.hash_size = get_signature_hash_size(private_key)


def load_puppetmaster(eid, password, objects_dir, links_dir, verbose=False):
    """
    Load the puppetmaster entity from its EID.

    The public key object is read from the o/ folder, the entity consistency
    and its links are verified with the functions of verify_entity.py, and
    the private key is looked up from the self-declaration links.

    Args:
        eid (str): The puppetmaster entity ID
        password (str): The private key password
        objects_dir (str): Path to the objects directory
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        Puppetmaster: The puppetmaster entity

    Raises:
        ValueError: If the entity is absent, inconsistent or its private key
            cannot be found
    """
    pub_content, pub_key = load_entity_public_key(eid, objects_dir)
    stats = collect_valid_entity_links(eid, pub_key, links_dir, verbose)
    problems, declarations, algorithm = check_entity_consistency(eid, stats, verbose)
    if problems:
        raise ValueError(
            f'inconsistent puppetmaster entity {eid}: {"; ".join(problems)}')
    private_key, priv_nid = find_private_key(
        eid, pub_content, password, declarations, objects_dir, verbose)
    if verbose:
        print(f"  private key: {priv_nid}")
        print(f"  algorithm: {algorithm}")
    return Puppetmaster(eid, pub_content, pub_key, private_key, priv_nid)


# ------------------------------------------------------------------------------------------
# Link generation functions
# ------------------------------------------------------------------------------------------

def generate_recognition_links(eid, types, puppetmaster, date, links_dir, verbose=False):
    """
    Generate and write the recognition links that declare an entity as master.

    The recognition links are generated and signed by the puppetmaster only.
    Matches prep_loop_code_master_php.sh and lib_nebule/007_authorities.php
    _findEntityByType() filter (req='l', nid1=rid, nid3=rid, entity=nid2):

        l>RID_TYPE>eid>RID_TYPE           global authority of type TYPE

    Args:
        eid (str): The entity recognized as master
        types (list): List of master types (security, code, time, directory)
        puppetmaster (Puppetmaster): The puppetmaster entity that signs
        date (str): Chronology in format 0YYYYMMDDHHMMSS
        links_dir (str): Path to the links directory
        verbose (bool): Show verbose output

    Returns:
        int: Number of links written

    Raises:
        ValueError: If a type is unknown
    """
    unsigned_links = []
    for master_type in types:
        if master_type not in MASTER_GLOBAL_TYPES:
            raise ValueError(
                f"Unknown master type: {master_type} "
                f"(expected one of: {', '.join(MASTER_GLOBAL_TYPES)})"
            )
        rid = MASTER_GLOBAL_TYPES[master_type]
        unsigned_links.append(create_bh_bl(date, 'l', [rid, eid, rid]))

    count = 0
    for bh_bl in unsigned_links:
        bloc_link = sign_link(
            bh_bl, puppetmaster.eid, puppetmaster.private_key, puppetmaster.hash_size)
        write_signed_link(bloc_link, links_dir, verbose)
        count += 1
    return count


# ------------------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Sign the nebule links that recognize master entities, '
                    'with the puppetmaster entity'
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
        '--puppetmaster',
        type=str,
        required=True,
        help='Puppetmaster entity ID (NID of its public key, present in o/). '
             'The private key is looked up from its links'
    )
    parser.add_argument(
        '--puppetmaster-password',
        type=str,
        default=None,
        help='Password of the puppetmaster private key. When absent, the script '
             'asks for it interactively'
    )
    parser.add_argument(
        '--master',
        type=str,
        action='append',
        default=[],
        dest='masters',
        help='Master role: <eid>,<type>[,<type>...] with type in '
             'security, code, time, directory (repeatable, signed by puppetmaster)'
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


def resolve_password(argument):
    """
    Resolve the puppetmaster private key password.

    The password is always required: it comes either from the
    --puppetmaster-password argument, or from an interactive question of the
    script.

    Args:
        argument (str): The --puppetmaster-password argument value, None when
            absent

    Returns:
        str: The password (possibly '')
    """
    if argument is not None:
        return argument
    return getpass.getpass('Puppetmaster private key password: ')


def parse_master_specs(master_specs):
    """
    Parse the --master specifications.

    Each specification is comma separated: the entity EID, then one or more
    master types. Each EID must be present in the o/ folder.

    Args:
        master_specs (list): List of --master specification strings

    Returns:
        list: List of (eid, [types]) tuples

    Raises:
        ValueError: If a specification is invalid
    """
    masters = []
    for spec in master_specs:
        parts = [p.strip() for p in spec.split(',') if p.strip() != '']
        if len(parts) < 2:
            raise ValueError(
                f"Invalid master spec (need entity EID and at least one type): {spec}")
        eid, types = parts[0], parts[1:]
        validate_eid(eid)
        for master_type in types:
            if master_type not in MASTER_GLOBAL_TYPES:
                raise ValueError(
                    f"Unknown master type: {master_type} "
                    f"(expected one of: {', '.join(MASTER_GLOBAL_TYPES)})")
        masters.append((eid, types))
    return masters


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

    # Parse master specifications
    try:
        masters = parse_master_specs(args.masters)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Resolve the puppetmaster password
    password = resolve_password(args.puppetmaster_password)

    # Load and verify the puppetmaster entity, then its private key from its links
    try:
        validate_eid(args.puppetmaster)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Loading puppetmaster entity {args.puppetmaster}...")
    try:
        puppetmaster = load_puppetmaster(
            args.puppetmaster, password, objects_dir, links_dir, args.verbose)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"Puppetmaster EID: {puppetmaster.eid}")

    # Verify the master entities
    if masters:
        print(f"Verifying {len(masters)} master entity(ies)...")
        try:
            for eid, _ in masters:
                verify_master_entity(eid, objects_dir, links_dir, args.verbose)
                print(f"Entity EID: {eid}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Generate recognition links, signed by the puppetmaster
    total = 0
    print('Generating puppetmaster recognition links...')
    for eid, types in masters:
        print(f"  {eid}: master of {', '.join(types)}")
        try:
            total += generate_recognition_links(
                eid, types, puppetmaster, date, links_dir, args.verbose)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Done: {total} bloc links written into {links_dir}/")
    return 0


if __name__ == '__main__':
    sys.exit(main())
