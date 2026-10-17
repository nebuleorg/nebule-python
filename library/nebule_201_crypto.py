"""
Nebule Crypto Module

This module provides cryptographic functionality using OpenSSL for the nebule library.
It is equivalent to 201_crypto.php in the PHP version.
"""

import hashlib
import hmac
import secrets
from library.nebule_000_init import (
    LIB_REF_CODE_ALGO,
)
from library.nebule_200_crypto_interface import CryptoInterface


class Crypto(CryptoInterface):
    """
    Main crypto class for nebule library.
    
    This class provides the default implementation of CryptoInterface,
    using hashlib and other standard Python libraries for cryptography.
    """
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
        self._hash_algorithm = LIB_REF_CODE_ALGO
    
    def crypto_hash(self, data, algorithm='sha2.256'):
        """
        Hash data using the specified algorithm.
        
        Args:
            data (str/bytes): Data to hash
            algorithm (str): Hash algorithm (default: sha2.256)
            
        Returns:
            str: Hexadecimal hash string
        """
        if not data:
            return ''
        
        # Convert string to bytes if needed
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Map algorithm names to hashlib names
        algo_map = {
            'sha2.224': 'sha224',
            'sha2.256': 'sha256',
            'sha2.384': 'sha384',
            'sha2.512': 'sha512',
            'sha3.224': 'sha3_224',
            'sha3.256': 'sha3_256',
            'sha3.384': 'sha3_384',
            'sha3.512': 'sha3_512',
        }
        
        # Use mapped algorithm or default to sha256
        hash_algo = algo_map.get(algorithm, 'sha256')
        
        try:
            hash_obj = hashlib.new(hash_algo)
            hash_obj.update(data)
            return hash_obj.hexdigest()
        except ValueError:
            # Fallback to sha256 if algorithm not supported
            hash_obj = hashlib.sha256()
            hash_obj.update(data)
            return hash_obj.hexdigest()
    
    def crypto_hash_file(self, filepath, algorithm='sha2.256'):
        """
        Hash a file using the specified algorithm.
        
        Args:
            filepath (str): Path to file to hash
            algorithm (str): Hash algorithm
            
        Returns:
            str: Hexadecimal hash string
        """
        if not filepath or not os.path.isfile(filepath):
            return ''
        
        import os
        
        # Map algorithm names
        algo_map = {
            'sha2.224': 'sha224',
            'sha2.256': 'sha256',
            'sha2.384': 'sha384',
            'sha2.512': 'sha512',
        }
        hash_algo = algo_map.get(algorithm, 'sha256')
        
        try:
            hash_obj = hashlib.new(hash_algo)
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except (ValueError, IOError):
            return ''
    
    def crypto_hash_verify(self, data, expected_hash, algorithm='sha2.256'):
        """
        Verify data against expected hash.
        
        Args:
            data (str/bytes): Data to verify
            expected_hash (str): Expected hash value
            algorithm (str): Hash algorithm
            
        Returns:
            bool: True if hash matches
        """
        computed_hash = self.crypto_hash(data, algorithm)
        return computed_hash == expected_hash.lower()
    
    def crypto_asymmetric_encrypt(self, data, public_key):
        """
        Encrypt data with a public key.
        
        Args:
            data (str): Data to encrypt
            public_key (str): Public key in PEM format
            
        Returns:
            str: Encrypted data (base64 encoded)
        """
        # This requires the cryptography library
        # For now, return empty string (stub)
        return ''
    
    def crypto_asymmetric_decrypt(self, data, private_key):
        """
        Decrypt data with a private key.
        
        Args:
            data (str): Data to decrypt (base64 encoded)
            private_key (str): Private key in PEM format
            
        Returns:
            str: Decrypted data
        """
        # Stub for now
        return ''
    
    def crypto_asymmetric_sign(self, data, private_key):
        """
        Sign data with a private key.
        
        Args:
            data (str): Data to sign
            private_key (str): Private key in PEM format
            
        Returns:
            str: Signature (base64 encoded)
        """
        # Stub for now
        return ''
    
    def crypto_asymmetric_verify(self, data, signature, public_key):
        """
        Verify a signature with a public key.
        
        Args:
            data (str): Original data
            signature (str): Signature to verify (base64 encoded)
            public_key (str): Public key in PEM format
            
        Returns:
            bool: True if signature is valid
        """
        # Stub for now
        return False
    
    def crypto_symmetric_encrypt(self, data, key, algorithm='aes.256.ctr'):
        """
        Encrypt data with a symmetric key.
        
        Args:
            data (str): Data to encrypt
            key (str): Encryption key
            algorithm (str): Encryption algorithm
            
        Returns:
            str: Encrypted data (base64 encoded)
        """
        # Stub for now
        return ''
    
    def crypto_symmetric_decrypt(self, data, key, algorithm='aes.256.ctr'):
        """
        Decrypt data with a symmetric key.
        
        Args:
            data (str): Data to decrypt (base64 encoded)
            key (str): Decryption key
            algorithm (str): Encryption algorithm
            
        Returns:
            str: Decrypted data
        """
        # Stub for now
        return ''
    
    def crypto_generate_keypair(self, algorithm='rsa.2048'):
        """
        Generate a public/private key pair.
        
        Args:
            algorithm (str): Key generation algorithm
            
        Returns:
            tuple: (public_key, private_key) in PEM format
        """
        # Stub for now - would use cryptography library
        return ('', '')
    
    def crypto_generate_random_key(self, length=32):
        """
        Generate a random symmetric key.
        
        Args:
            length (int): Key length in bytes
            
        Returns:
            str: Random key (hex encoded)
        """
        return secrets.token_hex(length)
    
    def crypto_hmac(self, data, key, algorithm='sha2.256'):
        """
        Generate HMAC for data with a key.
        
        Args:
            data (str): Data to sign
            key (str): Secret key
            algorithm (str): Hash algorithm
            
        Returns:
            str: HMAC (hex encoded)
        """
        if not data or not key:
            return ''
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(key, str):
            key = key.encode('utf-8')
        
        # Map algorithm
        algo_map = {
            'sha2.224': 'sha224',
            'sha2.256': 'sha256',
            'sha2.384': 'sha384',
            'sha2.512': 'sha512',
        }
        hash_algo = algo_map.get(algorithm, 'sha256')
        
        h = hmac.new(key, data, hash_algo)
        return h.hexdigest()
