#!/usr/bin/env python3
"""
Verify entity script for nebule.

Verifies an entity, typically the result of create_entity.py: checks the
key pair and the entity self-declaration links found in the l/ folder of
the target space, together with their signatures.

The private key is looked up from the links: the ownership fork link
(f>eid>privNID>priveRID) gives the private key object, which must also be
declared as a PEM file. Only structurally valid links signed by the entity,
with a verified signature, are taken into account.

The key pair is valid when the public and private key objects are present
and intact in the o/ folder, and the public key derived from the private
key (loaded with the password) matches the entity public key object. The
password is always required: either with --password, or it is asked
interactively by the script.

The displayed attributes (algorithm, name, location) are shown only when
declared by a link signed by the entity. The final status does not depend
on the optional attributes (name, location).

Usage:
    python3 verify_entity.py \
        --entity <eid|public_key_path> \
        [--space <space_folder>] \
        [--password <password>] \
        [--verbose]

Options:
    --entity                Entity ID (NID of its public key), or path to a
                            public key file (PEM or o/ object). Required.
    --space                 Root folder containing the o/ and l/ folders.
                            Default: '.'
    --password              Private key password. When absent, the script asks
                            for it interactively.
    --verbose               Show verbose output.

Exit status: 0 when the entity is valid, 1 otherwise.
"""

import argparse
import getpass
import hashlib
import os
import re
import sys

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

# Candidate RSA key sizes used to decode the algorithm reference
RSA_KEY_SIZES = (512, 1024, 1536, 2048, 3072, 4096, 8192)

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

    Args:
        reference (str): The reference string

    Returns:
        str: Formatted node ID of the reference
    """
    return format_node_id(compute_content_hash(reference.encode('utf-8')))


def canonical_contents(content):
    """
    Return the candidate canonical contents of an object file.

    The PHP prep stores key objects without trailing newline. Both the raw
    content and the content stripped of trailing newlines are candidates.

    Args:
        content (bytes): Raw file content

    Returns:
        list: Candidate contents, most canonical first
    """
    stripped = content.rstrip(b'\n')
    if stripped == content:
        return [content]
    return [stripped, content]


# ------------------------------------------------------------------------------------------
# Key functions
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
        raise ValueError(f"unable to load private key: {e}")


def load_public_key(content):
    """
    Load a public key from PEM content.

    Args:
        content (bytes): Public key PEM content

    Returns:
        The public key object

    Raises:
        ValueError: If the key cannot be loaded
    """
    try:
        return serialization.load_pem_public_key(content)
    except Exception as e:
        raise ValueError(f"unable to load public key: {e}")


def derive_public_key_pem(private_key):
    """
    Derive the public key PEM from a private key.

    Args:
        private_key: The private key object

    Returns:
        bytes: Public key PEM content
    """
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def verify_signature(bh_bl, signature_hex, hash_size, public_key):
    """
    Verify a BH_BL signature (RSA PKCS#1 v1.5 over sha2.256 or sha2.512).

    Args:
        bh_bl (str): The signed BH_BL content
        signature_hex (str): The signature (hexadecimal)
        hash_size (str): Hash size in bits ('256' or '512')
        public_key: The signer public key object

    Returns:
        bool: True if the signature is valid
    """
    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return False
    hash_algo = hashes.SHA512() if hash_size == '512' else hashes.SHA256()
    try:
        public_key.verify(signature, bh_bl.encode('utf-8'), padding.PKCS1v15(), hash_algo)
    except Exception:
        return False
    return True


# ------------------------------------------------------------------------------------------
# Link parsing functions
# ------------------------------------------------------------------------------------------

def parse_bloc_link(bloc_link):
    """
    Parse and structurally validate a bloc link BH_BL_BS.

    Format: nebule:link/2:0_0>CHR/REQ>NID1[>NID2...]>_EID>SIG.sha2.SIZE

    Args:
        bloc_link (str): Complete bloc link string

    Returns:
        tuple: (parsed_dict, error). parsed_dict is None when invalid.
            Keys of parsed_dict: 'date', 'req', 'nids', 'signers' with
            signers as a list of {'eid', 'sig', 'size'}.
    """
    parts = bloc_link.split('_')
    if len(parts) < 3:
        return None, 'missing BH_BL or BL_BS separator'
    bh, bl = parts[0], parts[1]
    bs_blocks = parts[2:]
    if bh != f"nebule:link/{LIB_LINK_VERSION}":
        return None, f'unsupported block header: {bh}'
    bl_parts = bl.split('/', 1)
    if len(bl_parts) != 2:
        return None, 'missing chronology/register separator'
    rc, rl = bl_parts
    rc_parts = rc.split('>')
    if len(rc_parts) != 2 or rc_parts[0] != '0':
        return None, f'invalid chronology register: {rc}'
    date = rc_parts[1]
    if not re.fullmatch(r'0\d{14}', date):
        return None, f'invalid chronology: {date}'
    rl_parts = rl.split('>')
    req = rl_parts[0]
    nids = rl_parts[1:]
    if not nids:
        return None, 'empty link register'
    if len(nids) > 4:
        return None, f'too many NIDs: {len(nids)}'
    for nid in nids:
        if not re.fullmatch(r'[0-9a-f]+\.[0-9a-z]+(?:\.\d+)?', nid):
            return None, f'invalid NID: {nid}'
    signers = []
    for bs in bs_blocks:
        bs_parts = bs.split('>')
        if len(bs_parts) != 2:
            return None, f'invalid block signature: {bs}'
        sig_parts = bs_parts[1].split('.')
        if len(sig_parts) != 3 or sig_parts[1] != 'sha2' \
                or sig_parts[2] not in ('256', '512'):
            return None, f'invalid signature suffix: {bs_parts[1]}'
        signers.append({'eid': bs_parts[0], 'sig': sig_parts[0], 'size': sig_parts[2]})
    return {'date': date, 'req': req, 'nids': nids, 'signers': signers}, ''


def read_links(links_dir):
    """
    Read all bloc links from the l/ folder (all node files and history).

    Duplicate link strings are removed, order is preserved.

    Args:
        links_dir (str): Path to the links directory

    Returns:
        list: Unique bloc link strings
    """
    links = []
    for name in os.listdir(links_dir):
        path = os.path.join(links_dir, name)
        if not os.path.isfile(path):
            continue
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            for line in f:
                line = line.strip()
                if line != '':
                    links.append(line)
    return list(dict.fromkeys(links))


# ------------------------------------------------------------------------------------------
# Objects functions
# ------------------------------------------------------------------------------------------

def read_object(objects_dir, nid, label):
    """
    Read an object from the o/ folder and check its integrity.

    The object must be present and its content must hash back to its name.

    Args:
        objects_dir (str): Path to the objects directory
        nid (str): Node ID (object name) to read
        label (str): Label for error messages

    Returns:
        tuple: (canonical_content, error). Content is None when absent or
            corrupted, with a non-empty error message.
    """
    object_path = os.path.join(objects_dir, nid)
    if not os.path.isfile(object_path):
        return None, f'{label} object absent: o/{nid}'
    with open(object_path, 'rb') as f:
        content = f.read()
    for candidate in canonical_contents(content):
        if format_node_id(compute_content_hash(candidate)) == nid:
            return candidate, ''
    return None, f'{label} object corrupted: o/{nid}'


# ------------------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Verify a nebule entity: check its key pair and its '
                    'self-declaration links, with their signatures'
    )
    parser.add_argument(
        '--entity',
        type=str,
        required=True,
        help='Entity ID (NID of its public key), or path to a public key file'
    )
    parser.add_argument(
        '--space',
        type=str,
        default='.',
        help="Root folder containing the o/ and l/ folders. Default: '.'"
    )
    parser.add_argument(
        '--password',
        type=str,
        default=None,
        help='Private key password. When absent, the script asks for it interactively'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show verbose output'
    )
    return parser.parse_args()


# ------------------------------------------------------------------------------------------
# Entity resolution functions
# ------------------------------------------------------------------------------------------

def resolve_entity_id(entity_arg, objects_dir):
    """
    Resolve the entity ID from the --entity argument.

    The argument is either a NID, or a path to a public key file (PEM file
    or o/ object): the EID is then the sha2.256 NID of its content.

    Args:
        entity_arg (str): The --entity argument value
        objects_dir (str): Path to the objects directory

    Returns:
        str: The entity ID

    Raises:
        SystemExit: If the argument is neither a NID nor a readable file
    """
    if os.path.isfile(entity_arg):
        with open(entity_arg, 'rb') as f:
            content = f.read()
        candidates = canonical_contents(content)
        for candidate in candidates:
            nid = format_node_id(compute_content_hash(candidate))
            if os.path.isfile(os.path.join(objects_dir, nid)):
                return nid
        return format_node_id(compute_content_hash(candidates[0]))
    if not re.fullmatch(r'[0-9a-f]+\.[0-9a-z]+(?:\.\d+)?', entity_arg):
        print(f"Error: Invalid entity ID: {entity_arg}", file=sys.stderr)
        sys.exit(1)
    return entity_arg


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


def find_declarations(valid_links, eid):
    """
    Extract the entity declarations from its valid signed links.

    Args:
        valid_links (list): List of parsed links signed by the entity
        eid (str): The entity ID

    Returns:
        dict: 'pub_pem' (bool), 'priv_pem' (set of private key NIDs
            declared as PEM), 'fork' (set of owned private key NIDs),
            'algorithm' (set of algorithm OIDs), 'name' (set of name OIDs),
            'location' (set of location OIDs)
    """
    pem_oid = ref_node_id(REF_PEM_TYPE)
    type_rid = ref_node_id(REF_OBJ_TYPE)
    name_rid = ref_node_id(REF_OBJ_NAME)
    local_rid = ref_node_id(REF_OBJ_ENTITY_LOCATION)
    private_rid = ref_node_id(REF_OBJ_ENTITY_PRIVATE)
    algo_rid = ref_node_id(REF_OBJ_ENTITY_ALGORITHM)

    declarations = {
        'pub_pem': False,
        'priv_pem': set(),
        'fork': set(),
        'algorithm': set(),
        'name': set(),
        'location': set(),
    }
    for parsed in valid_links:
        req = parsed['req']
        nids = parsed['nids']
        if req == 'l' and nids == [eid, pem_oid, type_rid]:
            declarations['pub_pem'] = True
        elif req == 'l' and len(nids) == 3 \
                and nids[0] != eid and nids[1] == pem_oid and nids[2] == type_rid:
            declarations['priv_pem'].add(nids[0])
        elif req == 'f' and len(nids) == 3 \
                and nids[0] == eid and nids[2] == private_rid:
            declarations['fork'].add(nids[1])
        elif req == 'l' and len(nids) == 3 \
                and nids[0] == eid and nids[2] == algo_rid:
            declarations['algorithm'].add(nids[1])
        elif req == 'l' and len(nids) == 3 \
                and nids[0] == eid and nids[2] == name_rid:
            declarations['name'].add(nids[1])
        elif req == 'l' and len(nids) == 3 \
                and nids[0] == eid and nids[2] == local_rid:
            declarations['location'].add(nids[1])
    return declarations


# ------------------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------------------

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

    # Resolve the entity and the password
    eid = resolve_entity_id(args.entity, objects_dir)
    password = resolve_password(args.password)
    print(f"Entity: {eid}")

    # Public key object: presence, integrity, loadability
    pub_content, pub_err = read_object(objects_dir, eid, 'public key')
    pub_key = None
    if pub_err != '':
        print(f"Public key: {pub_err}")
    else:
        try:
            pub_key = load_public_key(pub_content)
        except ValueError as e:
            print(f"Public key: not a valid public key PEM ({e})")
        else:
            print("Public key: ok")

    # Read and parse all links of the space
    all_links = read_links(links_dir)
    entity_links = []
    unparsed = 0
    for link in all_links:
        parsed, err = parse_bloc_link(link)
        if parsed is None:
            unparsed += 1
            if args.verbose:
                print(f"  unparseable link: {err}")
            continue
        if any(s['eid'] == eid for s in parsed['signers']):
            entity_links.append((link, parsed))
    if args.verbose:
        print(f"Links found in {links_dir}/: {len(all_links)} "
              f"({unparsed} unparseable), {len(entity_links)} signed by the entity")

    # Verify the structure and the signatures of the entity-signed links
    valid_links = []
    sigs_total = 0
    sigs_ok = 0
    for link, parsed in entity_links:
        bh_bl = '_'.join(link.split('_')[:2])
        link_ok = True
        for signer in parsed['signers']:
            sigs_total += 1
            signer_content, signer_err = read_object(
                objects_dir, signer['eid'], 'signer public key')
            if signer_err != '':
                link_ok = False
                if args.verbose:
                    print(f"  {parsed['req']}>{'>'.join(parsed['nids'])}: "
                          f"signature by {signer['eid']}: {signer_err}")
                continue
            try:
                signer_key = load_public_key(signer_content)
            except ValueError:
                link_ok = False
                if args.verbose:
                    print(f"  {parsed['req']}>{'>'.join(parsed['nids'])}: "
                          f"signer {signer['eid']} is not a public key")
                continue
            if verify_signature(bh_bl, signer['sig'], signer['size'], signer_key):
                sigs_ok += 1
            else:
                link_ok = False
                if args.verbose:
                    print(f"  {parsed['req']}>{'>'.join(parsed['nids'])}: "
                          f"invalid signature by {signer['eid']}")
        if link_ok:
            valid_links.append(parsed)

    links_count = len(entity_links)
    if links_count == 0:
        print("Links: none signed by the entity")
    else:
        print(f"Links: {len(valid_links)}/{links_count} valid")
        print(f"Signatures: {sigs_ok}/{sigs_total} valid")

    # Extract the entity declarations from its valid signed links
    declarations = find_declarations(valid_links, eid)

    # Look up the private key from the links, then check the key pair
    priv_candidates = declarations['fork'] & declarations['priv_pem']
    priv_nid = ''
    keypair_ok = False
    keypair_reason = ''
    if pub_key is None:
        keypair_reason = 'entity public key object unusable'
    elif not priv_candidates:
        keypair_reason = ('private key not declared by valid signed links '
                          '(ownership or PEM declaration missing)')
    else:
        for candidate in sorted(priv_candidates):
            priv_content, priv_err = read_object(objects_dir, candidate, 'private key')
            if priv_err != '':
                keypair_reason = priv_err
                continue
            priv_nid = candidate
            try:
                private_key = load_private_key(priv_content, password)
            except ValueError:
                keypair_reason = 'private key does not load with the given password'
                continue
            derived = derive_public_key_pem(private_key)
            if canonical_contents(derived)[0] == canonical_contents(pub_content)[0]:
                keypair_ok = True
                keypair_reason = ''
                break
            keypair_reason = ('the public key derived from the private key '
                              'does not match the entity public key')
    if priv_nid != '':
        print(f"Private key: {priv_nid}")
    if keypair_ok:
        print("Key pair: valid")
    else:
        print(f"Key pair: invalid - {keypair_reason}")

    # Decode the declared algorithm reference
    algorithm = ''
    for size in RSA_KEY_SIZES:
        if ref_node_id(f"rsa.{size}") in declarations['algorithm']:
            algorithm = f"rsa.{size}"
            break

    # Display the attributes, only when declared by a link signed by the entity
    print("Attributes:")
    attributes_shown = 0
    if algorithm != '':
        print(f"  algorithm: {algorithm}")
        attributes_shown += 1
    for label, oids in (('name', sorted(declarations['name'])),
                       ('location', sorted(declarations['location']))):
        for oid in oids:
            content, obj_err = read_object(objects_dir, oid, label)
            if obj_err != '':
                print(f"  {label}: {obj_err}")
            else:
                print(f"  {label}: {content.decode('utf-8', errors='replace')}")
            attributes_shown += 1
    if attributes_shown == 0:
        print("  (none)")

    # Final status: independent of the optional attributes (name, location)
    entity_valid = (
        pub_key is not None
        and keypair_ok
        and declarations['pub_pem']
        and algorithm != ''
        and links_count > 0
        and len(valid_links) == links_count
    )
    print(f"Final status: entity {'VALID' if entity_valid else 'INVALID'}")
    return 0 if entity_valid else 1


if __name__ == '__main__':
    sys.exit(main())
