#!/usr/bin/env python3
"""
Write links script for nebule.
Version: 020261028

Writes bloc links read from a file into the l/ folder of a space, after
checking them. Each line of the input file is a bloc link, either signed:

    BH_BL_BS   (nebule:link/2:0_0>CHR/REQ>NID1[>NID2...]>_EID>SIG.sha2.SIZE)

or unsigned, in which case the line holds the BH_BL part only:

    BH_BL      (nebule:link/2:0_0>CHR/REQ>NID1[>NID2...])

Empty lines and lines starting with '#' are ignored. The behavior depends
on the arguments:

- Without --entity, only the signed links are written, and only if every
  signature is verified with the public key object of an existing entity
  (present and intact in the o/ folder). Unsigned and unverifiable links
  are skipped.

- With --entity (and its private key password), the unsigned links are
  parsed, signed by the entity, then written. The signed links are verified
  then written, like without --entity.

- With --resign (requires --entity), the links already signed get the
  signature of the entity added into their BS block: the EID and its
  signature are appended to the BS, after the existing signatures. The
  existing signatures are still verified first, and a link already signed
  by the entity does not get a second signature from it.

The signing entity must be present in the space: its public key object is
read from o/, its consistency and its links are verified with the functions
of verify_entity.py, and its private key is looked up from its
self-declaration links and loaded with the password, exactly as
sign_master_entities.py does with the puppetmaster.

Links already present in the l/ folder are not rewritten. Written links go
into the l/ file of each NID referenced by the link register, plus one
line in the l/h history file.

Usage:
    python3 write_links.py <links_file> \
        --space <space_folder> \
        [--entity <eid>] \
        [--password <password>] \
        [--resign] \
        [--verbose]

Options:
    --space     Root folder containing the o/ and l/ folders. Default: '.'
    --entity    Signing entity ID (NID of its public key, present in o/).
                Required to sign the unsigned links and for --resign.
    --password  Password of the entity private key. Required with --entity,
                asked interactively when absent.
    --resign    Add the signature of the entity to the already signed links
                (append of the EID and its signature into the BS block).
    --verbose   Show verbose output.
"""

import argparse
import getpass
import os
import re
import sys

try:
    import verify_entity
except ImportError:
    print("Error: The 'verify_entity.py' script must be present in the same folder", file=sys.stderr)
    sys.exit(1)

try:
    import sign_master_entities
except ImportError:
    print("Error: The 'sign_master_entities.py' script must be present in the same folder", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------------------------------
# Links file reading functions
# ------------------------------------------------------------------------------------------

def read_links_file(links_file):
    """
    Read the bloc links from the input file.

    One bloc link per line, either signed (BH_BL_BS) or unsigned (BH_BL).
    Empty lines and lines starting with '#' are ignored.

    Args:
        links_file (str): Path to the input file

    Returns:
        list: The bloc link strings

    Raises:
        OSError: If the file cannot be read
    """
    links = []
    with open(links_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            links.append(line)
    return links


# ------------------------------------------------------------------------------------------
# Unsigned link parsing functions
# ------------------------------------------------------------------------------------------

def parse_bh_bl(bh_bl):
    """
    Parse and structurally validate the BH_BL content of an unsigned link.

    Same checks as verify_entity.parse_bloc_link(), minus the block
    signature: the input holds the BH_BL part only.

    Args:
        bh_bl (str): The BH_BL content string

    Returns:
        tuple: (parsed_dict, error). parsed_dict is None when invalid.
            Keys of parsed_dict: 'date', 'req', 'nids'.
    """
    parts = bh_bl.split('_')
    if len(parts) != 2:
        return None, 'expected BH_BL without block signature'
    bh, bl = parts
    if bh != f"nebule:link/{sign_master_entities.LIB_LINK_VERSION}":
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
    return {'date': date, 'req': req, 'nids': nids}, ''


# ------------------------------------------------------------------------------------------
# Signature verification functions
# ------------------------------------------------------------------------------------------

def load_signer_public_key(eid, objects_dir, cache):
    """
    Load the public key of a signer entity, with a cache.

    The entity must exist in the space: its public key object must be
    present and intact in the o/ folder.

    Args:
        eid (str): The signer entity ID
        objects_dir (str): Path to the objects directory
        cache (dict): Cache of the already loaded public keys

    Returns:
        tuple: (public_key, error). public_key is None when the entity
            cannot be used, with a non-empty error message.
    """
    if eid in cache:
        return cache[eid], ''
    try:
        _, pub_key = sign_master_entities.load_entity_public_key(eid, objects_dir)
    except ValueError as e:
        return None, str(e)
    cache[eid] = pub_key
    return pub_key, ''


def check_link_signatures(bloc_link, parsed, objects_dir, cache, verbose=False):
    """
    Check every signature of a parsed signed link.

    Each signer entity must exist in the space and its signature on the
    BH_BL content must be verified with its public key object.

    Args:
        bloc_link (str): Complete bloc link string BH_BL_BS
        parsed (dict): The verify_entity.parse_bloc_link() result
        objects_dir (str): Path to the objects directory
        cache (dict): Cache of the already loaded public keys
        verbose (bool): Show verbose output

    Returns:
        list: The problems as error strings, empty when all signatures verify
    """
    bh_bl = '_'.join(bloc_link.split('_')[:2])
    problems = []
    for signer in parsed['signers']:
        pub_key, err = load_signer_public_key(signer['eid'], objects_dir, cache)
        if pub_key is None:
            problems.append(f"signer {signer['eid']} is not an existing entity: {err}")
            continue
        if not verify_entity.verify_signature(bh_bl, signer['sig'], signer['size'], pub_key):
            problems.append(f"invalid signature from {signer['eid']}")
        elif verbose:
            print(f"  signature from {signer['eid']}: verified")
    return problems


def add_signature(bloc_link, entity):
    """
    Add the signature of an entity to the BS block of a signed link.

    The EID and its signature are appended after the existing signatures:
    BH_BL_BS1 becomes BH_BL_BS1_BS2. The existing signatures are kept
    untouched, and the signature is computed on the unchanged BH_BL content.

    Args:
        bloc_link (str): Complete bloc link string BH_BL_BS
        entity (Puppetmaster): The signing entity

    Returns:
        str: The resigned bloc link string
    """
    bh_bl = '_'.join(bloc_link.split('_')[:2])
    signature = sign_master_entities.sign_bh_bl(bh_bl, entity.private_key, entity.hash_size)
    return f"{bloc_link}_{entity.eid}>{signature}.sha2.{entity.hash_size}"


# ------------------------------------------------------------------------------------------
# Argument parsing
# ------------------------------------------------------------------------------------------

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Write bloc links from a file into the l/ folder of a '
                    'nebule space, checking and signing them'
    )
    parser.add_argument(
        'links_file',
        type=str,
        help='File containing the bloc links to write, one per line: '
             'signed (BH_BL_BS) or unsigned (BH_BL)'
    )
    parser.add_argument(
        '--space',
        type=str,
        default='.',
        help="Root folder containing the o/ and l/ folders. Default: '.'"
    )
    parser.add_argument(
        '--entity',
        type=str,
        default=None,
        help='Signing entity ID (NID of its public key, present in o/). '
             'The unsigned links are signed by this entity. '
             'The private key is looked up from its links'
    )
    parser.add_argument(
        '--password',
        type=str,
        default=None,
        help='Password of the entity private key. Required with --entity, '
             'asked interactively when absent'
    )
    parser.add_argument(
        '--resign',
        action='store_true',
        help='Add the signature of the entity to the already signed links, '
             'into their BS block (requires --entity)'
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

def resolve_password(argument):
    """
    Resolve the entity private key password.

    The password is required with --entity: it comes either from the
    --password argument, or from an interactive question of the script.

    Args:
        argument (str): The --password argument value, None when absent

    Returns:
        str: The password (possibly '')
    """
    if argument is not None:
        return argument
    return getpass.getpass('Entity private key password: ')


def main():
    """Main entry point."""
    args = parse_args()

    # Resolve space folders
    space = os.path.abspath(args.space)
    objects_dir = os.path.join(space, sign_master_entities.LIB_LOCAL_OBJECTS_FOLDER)
    links_dir = os.path.join(space, sign_master_entities.LIB_LOCAL_LINKS_FOLDER)
    if not os.path.isdir(objects_dir):
        print(f"Error: Objects folder not found: {objects_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(links_dir):
        print(f"Error: Links folder not found: {links_dir}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(args.links_file):
        print(f"Error: Links file not found: {args.links_file}", file=sys.stderr)
        sys.exit(1)

    # Check argument consistency
    if args.resign and args.entity is None:
        print("Error: --resign requires --entity", file=sys.stderr)
        sys.exit(1)
    if args.password is not None and args.entity is None:
        print("Error: --password requires --entity", file=sys.stderr)
        sys.exit(1)

    # Load and verify the signing entity, then its private key from its links
    entity = None
    if args.entity is not None:
        try:
            sign_master_entities.validate_eid(args.entity)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        password = resolve_password(args.password)
        print(f"Loading signing entity {args.entity}...")
        try:
            entity = sign_master_entities.load_puppetmaster(
                args.entity, password, objects_dir, links_dir, args.verbose)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Entity EID: {entity.eid}")

    # Read the links to write, and the links already present in the space
    links = read_links_file(args.links_file)
    existing_links = set(verify_entity.read_links(links_dir))
    print(f"Links to write: {len(links)} (from {args.links_file})")

    # Process the links
    stats = {
        'written': 0,
        'signed': 0,
        'resigned': 0,
        'duplicates': 0,
        'unsigned': 0,
        'invalid': 0,
        'unverified': 0,
    }
    pub_key_cache = {}
    for raw in links:
        parts_count = len(raw.split('_'))
        if parts_count < 3:
            # Unsigned link: only signed when an entity is given
            if entity is None:
                stats['unsigned'] += 1
                if args.verbose:
                    print(f"  skipped (unsigned, no --entity): {raw}")
                continue
            parsed, err = parse_bh_bl(raw)
            if parsed is None:
                stats['invalid'] += 1
                print(f"Error: invalid unsigned link: {err}", file=sys.stderr)
                continue
            bloc_link = sign_master_entities.sign_link(
                raw, entity.eid, entity.private_key, entity.hash_size)
            stats['signed'] += 1
            if args.verbose:
                print(f"  signed by {entity.eid}: {bloc_link}")
        else:
            # Signed link: every signature must verify with an existing entity
            parsed, err = verify_entity.parse_bloc_link(raw)
            if parsed is None:
                stats['invalid'] += 1
                print(f"Error: invalid link: {err}", file=sys.stderr)
                continue
            problems = check_link_signatures(
                raw, parsed, objects_dir, pub_key_cache, args.verbose)
            if problems:
                stats['unverified'] += 1
                print(f"Error: unverified link ({'; '.join(problems)})", file=sys.stderr)
                continue
            bloc_link = raw
            # Resign: append the entity signature into the BS block
            if args.resign and entity is not None \
                    and all(s['eid'] != entity.eid for s in parsed['signers']):
                bloc_link = add_signature(bloc_link, entity)
                stats['resigned'] += 1
                if args.verbose:
                    print(f"  resigned by {entity.eid}: {bloc_link}")

        # Write the link, unless already present in the space
        if bloc_link in existing_links:
            stats['duplicates'] += 1
            if args.verbose:
                print(f"  skipped (already present): {bloc_link}")
            continue
        sign_master_entities.write_signed_link(bloc_link, links_dir, args.verbose)
        existing_links.add(bloc_link)
        stats['written'] += 1

    # Summary
    print(f"Done: {stats['written']} bloc links written into {links_dir}/ "
          f"({stats['signed']} signed, {stats['resigned']} resigned, "
          f"{stats['duplicates']} already present, {stats['unsigned']} unsigned skipped, "
          f"{stats['invalid']} invalid, {stats['unverified']} unverified)")
    if stats['unsigned'] and entity is None:
        print("Hint: unsigned links need --entity (and --password) to be signed and written")
    return 0


if __name__ == '__main__':
    sys.exit(main())
