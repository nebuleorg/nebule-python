"""
Nebule Crypto Interface

This module defines the interface for cryptographic operations in the nebule library.
It is equivalent to 200_crypto_interface.php in the PHP version.
"""

from abc import ABC, abstractmethod


class CryptoInterface(ABC):
    """
    Abstract base class for cryptographic operations.
    
    Classes implementing this interface provide cryptographic functionality
    for the nebule library, including hashing, encryption, and signing.
    """
    
    @abstractmethod
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        pass
    
    # Hash operations
    
    @abstractmethod
    def crypto_hash(self, data, algorithm='sha2.256'):
        """
        Hash data using the specified algorithm.
        
        Args:
            data (str/bytes): Data to hash
            algorithm (str): Hash algorithm (default: sha2.256)
            
        Returns:
            str: Hexadecimal hash string
        """
        pass
    
    @abstractmethod
    def crypto_hash_file(self, filepath, algorithm='sha2.256'):
        """
        Hash a file using the specified algorithm.
        
        Args:
            filepath (str): Path to file to hash
            algorithm (str): Hash algorithm
            
        Returns:
            str: Hexadecimal hash string
        """
        pass
    
    @abstractmethod
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
        pass
    
    # Asymmetric encryption (public/private keys)
    
    @abstractmethod
    def crypto_asymmetric_encrypt(self, data, public_key):
        """
        Encrypt data with a public key.
        
        Args:
            data (str): Data to encrypt
            public_key (str): Public key
            
        Returns:
            str: Encrypted data
        """
        pass
    
    @abstractmethod
    def crypto_asymmetric_decrypt(self, data, private_key):
        """
        Decrypt data with a private key.
        
        Args:
            data (str): Data to decrypt
            private_key (str): Private key
            
        Returns:
            str: Decrypted data
        """
        pass
    
    @abstractmethod
    def crypto_asymmetric_sign(self, data, private_key):
        """
        Sign data with a private key.
        
        Args:
            data (str): Data to sign
            private_key (str): Private key
            
        Returns:
            str: Signature
        """
        pass
    
    @abstractmethod
    def crypto_asymmetric_verify(self, data, signature, public_key):
        """
        Verify a signature with a public key.
        
        Args:
            data (str): Original data
            signature (str): Signature to verify
            public_key (str): Public key
            
        Returns:
            bool: True if signature is valid
        """
        pass
    
    # Symmetric encryption
    
    @abstractmethod
    def crypto_symmetric_encrypt(self, data, key, algorithm='aes.256.ctr'):
        """
        Encrypt data with a symmetric key.
        
        Args:
            data (str): Data to encrypt
            key (str): Encryption key
            algorithm (str): Encryption algorithm
            
        Returns:
            str: Encrypted data
        """
        pass
    
    @abstractmethod
    def crypto_symmetric_decrypt(self, data, key, algorithm='aes.256.ctr'):
        """
        Decrypt data with a symmetric key.
        
        Args:
            data (str): Data to decrypt
            key (str): Decryption key
            algorithm (str): Encryption algorithm
            
        Returns:
            str: Decrypted data
        """
        pass
    
    # Key management
    
    @abstractmethod
    def crypto_generate_keypair(self, algorithm='rsa.2048'):
        """
        Generate a public/private key pair.
        
        Args:
            algorithm (str): Key generation algorithm
            
        Returns:
            tuple: (public_key, private_key)
        """
        pass
    
    @abstractmethod
    def crypto_generate_random_key(self, length=32):
        """
        Generate a random symmetric key.
        
        Args:
            length (int): Key length in bytes
            
        Returns:
            str: Random key
        """
        pass
