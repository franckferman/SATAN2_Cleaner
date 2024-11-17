#!/usr/bin/env python3
# encryption.py

"""
SATAN2 Cleaner - Encryption Module

Description:
Handles encryption of storage devices using randomly generated passwords and supports
multiple encryption algorithms, including AES and ChaCha20.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

import secrets
import string
from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES, ChaCha20
from Crypto.Random import get_random_bytes
from .exceptions import UnsupportedAlgorithmError

def derive_key(password, salt):
    """
    Derive a cryptographic key from a password and salt using the scrypt key derivation function.

    Parameters:
        password (str): The password to derive the key from.
        salt (bytes): The salt to use for key derivation.

    Returns:
        bytes: The derived key.
    """
    N = 2**20  # Cost parameter
    r = 8
    p = 1
    key_len = 32  # 256 bits
    try:
        key = scrypt(password.encode(), salt, key_len, N=N, r=r, p=p)
        return key
    except ValueError as e:
        print("Error deriving key with scrypt:", e)
        raise

def encrypt_disk_with_password(disk_info, algorithm='AES'):
    """
    Encrypt a disk with a randomly generated password.

    Parameters:
        disk_info (dict): A dictionary containing disk details such as 'Number' and 'Size'.
        algorithm (str): The encryption algorithm to use ('AES' or 'ChaCha20').

    Raises:
        UnsupportedAlgorithmError: If the specified algorithm is not supported.
    """
    disk_number = disk_info['Number']
    size_bytes = disk_info['Size']

    # Generate a random 64-character password
    password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                       for _ in range(64))

    # Generate a random salt
    salt = get_random_bytes(16)

    # Derive the key
    key = derive_key(password, salt)

    # Prepare the encryption
    if algorithm == 'AES':
        nonce = get_random_bytes(12)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        block_size = 16
    elif algorithm == 'CHACHA20':
        nonce = get_random_bytes(12)
        cipher = ChaCha20.new(key=key, nonce=nonce)
        block_size = 64
    else:
        raise UnsupportedAlgorithmError(f"Unsupported algorithm: {algorithm}")

    print(f"Encrypting disk using {algorithm}...")

    # Path to the physical disk
    disk_path = f"\\\\.\PhysicalDrive{disk_number}"

    try:
        with open(disk_path, 'rb+') as disk:
            total_bytes = 0
            while total_bytes < size_bytes:
                plaintext = get_random_bytes(block_size)
                ciphertext = cipher.encrypt(plaintext)
                disk.write(ciphertext)
                total_bytes += block_size

                # Display progress
                if total_bytes % (100 * 1024 * 1024) == 0:
                    percent = (total_bytes / size_bytes) * 100
                    print(f"Progress: {percent:.2f}%")

        print("Encryption completed successfully.")
    except PermissionError:
        print("Error: Insufficient permissions. Run the script as an administrator.")
    except Exception as e:
        print("An error occurred during encryption:", e)
