"""
Nebule Crypto OpenSSL Module

This module provides cryptographic functionality using OpenSSL bindings for the nebule library.
It is equivalent to 202_crypto_openssl.php in the PHP version.

Note: This implementation requires the cryptography library to be installed:
    pip install cryptography
"""

from library.nebule_200_crypto_interface import CryptoInterface


class CryptoOpenSSL(CryptoInterface):
    """
    OpenSSL-based crypto class for nebule library.
    
    This class provides OpenSSL-specific cryptographic operations.
    It requires the cryptography library to be installed.
    """
    
    def __init__(self, nebule_instance):
        """
        Constructor.
        
        Args:
            nebule_instance: Reference to the main nebule instance
        """
        self._nebule_instance = nebule_instance
        self._initialized = False
        
        try:
            # Try to import cryptography
            import cryptography
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding, rsa
            from cryptography.hazmat.backends import default_backend
            
            self._cryptography_available = True
            self._backend = default_backend()
            self._initialized = True
        except ImportError:
            self._cryptography_available = False
            self._initialized = False
    
    def is_initialized(self):
        """Check if OpenSSL crypto is available."""
        return self._initialized
    
    def crypto_hash(self, data, algorithm='sha2.256'):
        """
        Hash data using OpenSSL.
        
        Args:
            data (str/bytes): Data to hash
            algorithm (str): Hash algorithm
            
        Returns:
            str: Hexadecimal hash string
        """
        if not self._initialized:
            return ''
        
        import hashlib
        
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Map algorithm names
        algo_map = {
            'sha2.224': 'sha224',
            'sha2.256': 'sha256',
            'sha2.384': 'sha384',
            'sha2.512': 'sha512',
        }
        
        try:
            hash_obj = hashlib.new(algo_map.get(algorithm, 'sha256'))
            hash_obj.update(data)
            return hash_obj.hexdigest()
        except ValueError:
            return ''
    
    def crypto_hash_file(self, filepath, algorithm='sha2.256'):
        """
        Hash a file using OpenSSL.
        
        Args:
            filepath (str): Path to file to hash
            algorithm (str): Hash algorithm
            
        Returns:
            str: Hexadecimal hash string
        """
        if not self._initialized:
            return ''
        
        import hashlib
        import os
        
        if not os.path.isfile(filepath):
            return ''
        
        algo_map = {
            'sha2.224': 'sha224',
            'sha2.256': 'sha256',
            'sha2.384': 'sha384',
            'sha2.512': 'sha512',
        }
        
        try:
            hash_obj = hashlib.new(algo_map.get(algorithm, 'sha256'))
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
        Encrypt data with a public key using RSA.
        
        Args:
            data (str): Data to encrypt
            public_key (str): Public key in PEM format
            
        Returns:
            str: Encrypted data (base64 encoded)
        """
        if not self._cryptography_available:
            return ''
        
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            import base64
            
            # Load public key
            pub_key = serialization.load_pem_public_key(
                public_key.encode('utf-8'),
                backend=self._backend
            )
            
            # Encrypt
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            ciphertext = pub_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return base64.b64encode(ciphertext).decode('ascii')
        except Exception:
            return ''
    
    def crypto_asymmetric_decrypt(self, data, private_key):
        """
        Decrypt data with a private key using RSA.
        
        Args:
            data (str): Data to decrypt (base64 encoded)
            private_key (str): Private key in PEM format
            
        Returns:
            str: Decrypted data
        """
        if not self._cryptography_available:
            return ''
        
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            import base64
            
            # Load private key
            priv_key = serialization.load_pem_private_key(
                private_key.encode('utf-8'),
                password=None,
                backend=self._backend
            )
            
            # Decrypt
            ciphertext = base64.b64decode(data)
            plaintext = priv_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            return plaintext.decode('utf-8')
        except Exception:
            return ''
    
    def crypto_asymmetric_sign(self, data, private_key):
        """
        Sign data with a private key using RSA.
        
        Args:
            data (str): Data to sign
            private_key (str): Private key in PEM format
            
        Returns:
            str: Signature (base64 encoded)
        """
        if not self._cryptography_available:
            return ''
        
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            import base64
            
            # Load private key
            priv_key = serialization.load_pem_private_key(
                private_key.encode('utf-8'),
                password=None,
                backend=self._backend
            )
            
            # Sign
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            signature = priv_key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return base64.b64encode(signature).decode('ascii')
        except Exception:
            return ''
    
    def crypto_asymmetric_verify(self, data, signature, public_key):
        """
        Verify a signature with a public key using RSA.
        
        Args:
            data (str): Original data
            signature (str): Signature to verify (base64 encoded)
            public_key (str): Public key in PEM format
            
        Returns:
            bool: True if signature is valid
        """
        if not self._cryptography_available:
            return False
        
        try:
            from cryptography.hazmat.primitives import hashes, serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            import base64
            
            # Load public key
            pub_key = serialization.load_pem_public_key(
                public_key.encode('utf-8'),
                backend=self._backend
            )
            
            # Verify
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            sig = base64.b64decode(signature)
            
            pub_key.verify(
                sig,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return True
        except Exception:
            return False
    
    def crypto_generate_keypair(self, algorithm='rsa.2048'):
        """
        Generate a public/private key pair.
        
        Args:
            algorithm (str): Key generation algorithm
            
        Returns:
            tuple: (public_key, private_key) in PEM format
        """
        if not self._cryptography_available:
            return ('', '')
        
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import serialization
            
            # Parse algorithm
            if algorithm.startswith('rsa.'):
                try:
                    key_size = int(algorithm.split('.')[1])
                except ValueError:
                    key_size = 2048
            else:
                key_size = 2048
            
            # Generate key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=self._backend
            )
            
            # Serialize
            priv_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            pub_pem = private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            return (pub_pem.decode('utf-8'), priv_pem.decode('utf-8'))
        except Exception:
            return ('', '')
    
    def crypto_generate_random_key(self, length=32):
        """
        Generate a random symmetric key.
        
        Args:
            length (int): Key length in bytes
            
        Returns:
            str: Random key (hex encoded)
        """
        import secrets
        return secrets.token_hex(length)
