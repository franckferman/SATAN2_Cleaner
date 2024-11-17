#!/usr/bin/env python3
# disk_manager.py

"""
SATAN2 Cleaner - Disk Manager Module

Description:
Provides disk management functionalities for listing, selecting, formatting, secure erasing,
and encrypting disks. It includes operations such as disk selection by letter or number,
quick formatting, secure erasing with multiple passes, and a "nuke" operation for irrecoverable erasure.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

import subprocess
import json
import re
import secrets
import string
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, ChaCha20
from .exceptions import (
    DiskNotFoundError, InvalidDiskFormatError, InvalidEraseMethodError, UnsupportedAlgorithmError
)
from .utilities import is_windows
from .encryption import encrypt_disk_with_password, derive_key

class DiskManager:
    def __init__(self):
        if not is_windows():
            raise OSError("This script only works on Windows.")

    def get_disks(self):
        """
        Retrieve the list of available disks.

        Returns:
            list: A list of dictionaries containing disk information such as 'Number', 'FriendlyName', and 'Size'.
        """
        cmd = 'Get-Disk | Select-Object Number,FriendlyName,Size | ConvertTo-Json -Compress'
        result = subprocess.run(['powershell', '-NoProfile', '-Command', cmd],
                                capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise RuntimeError("Error retrieving disks.")
        disks = json.loads(result.stdout)
        if isinstance(disks, dict):
            disks = [disks]
        return disks

    def select_disk_by_letter(self, disk_letter):
        """
        Select a disk by its drive letter.

        Parameters:
            disk_letter (str): The drive letter (e.g., 'D:\\').

        Returns:
            dict: A dictionary containing information about the selected disk.

        Raises:
            InvalidDiskFormatError: If the drive letter format is invalid.
            DiskNotFoundError: If no disk is found for the specified letter.
        """
        if not re.match(r'^[A-Za-z](:\\)?$', disk_letter):
            raise InvalidDiskFormatError("Invalid format. Valid example: 'D:\\'.")
        drive_letter = disk_letter.strip(':\\').upper()
        cmd = f"""
        $partition = Get-Partition -DriveLetter '{drive_letter}'
        if ($partition) {{
            $disk = $partition | Get-Disk | Select-Object Number,FriendlyName,Size
            $disk | ConvertTo-Json -Compress
        }} else {{
            Write-Output 'null'
        }}
        """
        result = subprocess.run(['powershell', '-NoProfile', '-Command', cmd],
                                capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() == 'null':
            raise DiskNotFoundError(f"No disk found for {drive_letter}.")
        return json.loads(result.stdout)

    def select_disk_by_number(self, number):
        """
        Select a disk by its number.

        Parameters:
            number (int): The disk number.

        Returns:
            dict: A dictionary containing information about the selected disk.

        Raises:
            DiskNotFoundError: If no disk is found for the specified number.
        """
        cmd = f'Get-Disk -Number {number} | Select-Object Number,FriendlyName,Size | ConvertTo-Json -Compress'
        result = subprocess.run(['powershell', '-NoProfile', '-Command', cmd],
                                capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            raise DiskNotFoundError(f"Disk number {number} not found.")
        return json.loads(result.stdout)

    def quick_format_disk(self, disk_info):
        """
        Perform a quick format of the specified disk.

        Parameters:
            disk_info (dict): A dictionary containing disk information.
        """
        disk_number = disk_info['Number']
        friendly_name = disk_info['FriendlyName']
        size_gb = disk_info['Size'] / 1e+9

        confirmation = input(f"⚠️ Confirm formatting disk {disk_number} ({friendly_name}, {size_gb:.2f} GB)? (y/n): ")
        if confirmation.lower() != 'y':
            print("Formatting canceled.")
            return

        script = f"""
        $diskNumber = {disk_number}
        $disk = Get-Disk -Number $diskNumber
        if ($disk) {{
            Set-Disk -Number $diskNumber -IsReadOnly $false -IsOffline $false
            Clear-Disk -Number $diskNumber -RemoveData -Confirm:$false
            Initialize-Disk -Number $diskNumber -PartitionStyle MBR
            $partition = New-Partition -DiskNumber $diskNumber -UseMaximumSize -AssignDriveLetter
            Format-Volume -Partition $partition -FileSystem NTFS -NewFileSystemLabel "NewVolume" -Confirm:$false -Force
            Write-Output "Success"
        }} else {{
            Write-Output "DiskNotFound"
        }}
        """
        print("Formatting in progress...")
        result = subprocess.run(['powershell', '-NoProfile', '-Command', script],
                                capture_output=True, text=True)
        if "Success" in result.stdout:
            print(f"Disk {disk_number} formatted successfully.")
        else:
            print("Error during formatting:", result.stderr)

    def secure_erase_disk(self, disk_info, passes=1, algorithm='AES', method='securepass'):
        """
        Securely erase the specified disk and encrypt it.

        Parameters:
            disk_info (dict): A dictionary containing disk information.
            passes (int): Number of passes for erasing.
            algorithm (str): The encryption algorithm to use ('AES' or 'ChaCha20').
            method (str): The method for erasing ('dod3pass', 'dod7pass', 'securepass', 'quickformat').

        Raises:
            InvalidEraseMethodError: If the specified erase method is not supported.
            UnsupportedAlgorithmError: If the specified algorithm is not supported.
        """
        disk_number = disk_info['Number']
        friendly_name = disk_info['FriendlyName']
        size_bytes = disk_info['Size']
        size_gb = size_bytes / 1e+9

        if method not in ['dod3pass', 'dod7pass', 'securepass', 'quickformat']:
            raise InvalidEraseMethodError(f"Unsupported method: {method}")

        if algorithm not in ['AES', 'CHACHA20']:
            raise UnsupportedAlgorithmError(f"Unsupported algorithm: {algorithm}")

        if method == 'dod3pass':
            passes = 3
            patterns = [0xFF, 0x00, 0xFF]
        elif method == 'dod7pass':
            passes = 7
            patterns = [0xFF, 0x00, 0xAA, 0x55, 0xFF, 0x00, 0xFF]
        elif method == 'securepass':
            patterns = None  # Use encryption
        elif method == 'quickformat':
            self.quick_format_disk(disk_info)
            print("Encrypting after quick format.")
            encrypt_disk_with_password(disk_info, algorithm=algorithm)
            return

        confirmation = input(f"⚠️ Confirm erasing disk {disk_number} ({friendly_name}, {size_gb:.2f} GB) with method {method}? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation canceled.")
            return

        print(f"Erasing in progress using method {method}...")

        for pass_num in range(1, passes + 1):
            print(f"Pass {pass_num}/{passes}...")

            if patterns:
                pattern = patterns[pass_num - 1]
                data_block = bytes([pattern]) * 4096
            else:
                password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                                   for _ in range(64))
                salt = get_random_bytes(16)
                key = derive_key(password, salt)

                if algorithm == 'AES':
                    nonce = get_random_bytes(12)
                    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                    block_size = 16
                elif algorithm == 'CHACHA20':
                    nonce = get_random_bytes(12)
                    cipher = ChaCha20.new(key=key, nonce=nonce)
                    block_size = 64

            disk_path = f"\\\\.\PhysicalDrive{disk_number}"

            try:
                with open(disk_path, 'rb+') as disk:
                    total_bytes = 0
                    while total_bytes < size_bytes:
                        if patterns:
                            disk.write(data_block)
                            total_bytes += len(data_block)
                        else:
                            plaintext = get_random_bytes(block_size)
                            ciphertext = cipher.encrypt(plaintext)
                            disk.write(ciphertext)
                            total_bytes += block_size

                        if total_bytes % (100 * 1024 * 1024) == 0:
                            percent = (total_bytes / size_bytes) * 100
                            print(f"Progress: {percent:.2f}%")

                print(f"Pass {pass_num} completed.")
            except PermissionError:
                print("Error: Insufficient permissions.")
                return
            except Exception as e:
                print(f"Error during pass {pass_num}:", e)
                return

        print("Encrypting after secure erasing.")
        encrypt_disk_with_password(disk_info, algorithm=algorithm)

        print(f"Disk {disk_number} erased and encrypted successfully.")

    def nuke_disk(self, disk_info, algorithm='AES', passes=3):
        """
        Execute a series of actions to make the data on the disk unrecoverable.

        Parameters:
            disk_info (dict): A dictionary containing disk information.
            algorithm (str): The encryption algorithm to use ('AES' or 'ChaCha20').
            passes (int): Number of passes for secure erasing.
        """
        disk_number = disk_info['Number']
        friendly_name = disk_info['FriendlyName']
        size_gb = disk_info['Size'] / 1e+9

        confirmation = input(f"⚠️ Confirm NUKE operation on disk {disk_number} ({friendly_name}, {size_gb:.2f} GB) with {passes} passes? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation canceled.")
            return

        print("Step 1: Quick format.")
        self.quick_format_disk(disk_info)

        print(f"Step 2: Secure erasing ({passes} passes).")
        self.secure_erase_disk(disk_info, passes=passes, algorithm=algorithm)

        print("Step 3: Encrypting the disk.")
        encrypt_disk_with_password(disk_info, algorithm=algorithm)

        print("Step 4: Quick reformat.")
        self.quick_format_disk(disk_info)

        print("Step 5: Re-encrypting the disk.")
        encrypt_disk_with_password(disk_info, algorithm=algorithm)

        print("NUKE operation completed successfully.")
