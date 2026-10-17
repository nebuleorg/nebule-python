# Nebule Python Library

## Overview

This directory contains the object-oriented Python library equivalent to the PHP `lib_nebule/` library. It provides the core functionality for the nebule project without any web display logic.

## Files

The library consists of multiple Python files that follow the same numbering scheme as the PHP version:

- **000-014**: Core modules (init, nebule, references, functions, metrology, configuration, etc.)
- **100-104**: I/O interfaces and implementations
- **200-204**: Crypto interfaces and implementations
- **300-312**: Social interfaces and contexts
- **400-409**: Node/Entity/Group and related classes
- **500-503**: Link classes
- **999**: License information

## Assembly

To assemble all library files into a single file for the `o/` directory, use the `prep_library.py` script:

```bash
# Basic usage
python3 prep_library.py --master-entity <entity_id> --master-password <password>

# With clean (removes all files from o/ before assembling)
python3 prep_library.py --master-entity <entity_id> --master-password <password> --clean

# With custom output name
python3 prep_library.py --master-entity <entity_id> --master-password <password> --output my_library.py

# With verbose output
python3 prep_library.py --master-entity <entity_id> --master-password <password> --verbose
```

### Arguments

- `--master-entity` (required): Entity ID of the master entity
- `--master-password` (required): Private key password for the master entity
- `--output` (optional): Output file name in o/ directory (default: nebule_library.py)
- `--clean` (optional): Clean the o/ directory before assembling
- `--verbose` (optional): Show verbose output

### Example

```bash
python3 prep_library.py \
  --master-entity "88848d09edc416e443ce1491753c75d75d7d8790c1253becf9a2191ac369f4ea.sha2.256" \
  --master-password "my_secret_password" \
  --clean
```

This will:
1. Clean the `o/` directory
2. Assemble all library files into `o/nebule_library.py`
3. Add metadata about the master entity
4. Make the file self-contained (removes library-specific imports)

## Usage

After assembly, you can load the library from the `o/` directory:

```python
import o.nebule_library

# Create Nebule instance
neb = o.nebule_library.Nebule()

# Access components
metrology = neb.metrology
config = neb.configuration
io = neb.io
```

Or use nebule.py to load it as an application:

```bash
python3 nebule.py --application nebule_library
```

## Loading with nebule.py

The `nebule.py` script can load and execute applications from the `o/` directory:

```bash
# Load the assembled library
python3 nebule.py --application nebule_library

# Load with debug output
python3 nebule.py --application nebule_library --debug
```

## File Structure

The library files are named to match their PHP counterparts:

```
library/
├── 000_init.py           # Constants and initialization
├── 001_nebule.py          # Main Nebule class
├── 002_references.py      # Reference management
├── 003_functions.py       # Utility functions
├── 004_metrology.py       # Logging and metrics
├── 005_configuration.py  # Configuration management
├── 006_rescue.py          # Rescue mode
├── 007_authorities.py     # Authority management
├── 008_entities.py        # Entity management
├── 009_recovery.py        # Recovery functionality
├── 010_cache.py           # Caching
├── 011_session.py         # Session management
├── 012_tokenize.py        # Tokenization
├── 014_router.py          # Routing
├── 100_io_interface.py    # I/O interface
├── 101_io.py              # Basic I/O
├── 102_io_disk.py         # Disk I/O
├── 103_io_network_http.py # HTTP network I/O
├── 104_io_network_https.py # HTTPS network I/O
├── 200_crypto_interface.py # Crypto interface
├── 201_crypto.py          # Basic crypto
├── 202_crypto_openssl.py  # OpenSSL crypto
├── 204_crypto_sodium.py   # Sodium crypto (PyNaCl)
├── 300_social_interface.py # Social interface
├── 301_social.py          # Main social class
├── 302_social_myself.py   # "myself" context
├── 303_social_notmyself.py # "notmyself" context
├── 304_social_self.py     # "self" context
├── 305_social_notself.py  # "notself" context
├── 306_social_authority.py # "authority" context
├── 307_social_all.py      # "all" context
├── 308_social_none.py     # "none" context
├── 309_social_onlist.py   # "onlist" context
├── 310_social_offlist.py  # "offlist" context
├── 311_social_reputation.py # "reputation" context
├── 312_social_unreputation.py # "unreputation" context
├── 400_node_interface.py  # Node interface
├── 401_node.py            # Node class
├── 402_group.py           # Group class
├── 403_entity.py          # Entity class
├── 404_location.py        # Location class
├── 405_conversation.py   # Conversation class
├── 406_currency.py        # Currency class
├── 407_tokenpool.py       # TokenPool class
├── 408_token.py           # Token class
├── 409_wallet.py          # Wallet class
├── 500_link_interface.py  # Link interface
├── 501_bloclink.py        # BlocLink class
├── 502_link_register.py   # LinkRegister class
├── 503_transaction.py     # Transaction class
└── 999_license.py         # License information
```

## Dependencies

Some modules require additional Python packages:

- **OpenSSL Crypto** (202_crypto_openssl.py): `pip install cryptography`
- **Sodium Crypto** (204_crypto_sodium.py): `pip install pynacl`

The base crypto module (201_crypto.py) uses only standard library (hashlib, hmac, secrets).
