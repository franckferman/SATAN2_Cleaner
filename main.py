#!/usr/bin/env python3
# main.py

"""
SATAN2 Cleaner - Main Module

Description:
Handles the command-line interface for securely formatting and erasing storage devices,
including secure erase options, quick formatting, and disk management features.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

import typer
from disk_utils.disk_manager import DiskManager
from disk_utils.exceptions import (
    DiskNotFoundError, InvalidDiskFormatError, UnsupportedAlgorithmError, InvalidEraseMethodError
)
from disk_utils.utilities import print_disk_info

def main(
    disk: str = typer.Option(None, help="Optional disk identifier (e.g., 'D:\\')"),
    format_disk: bool = typer.Option(False, help="Quick format the selected disk to NTFS"),
    secure_erase: bool = typer.Option(False, help="Securely erase the selected disk"),
    erase_method: str = typer.Option('securepass', help="Erase method ('dod3pass', 'dod7pass', 'securepass', 'quickformat')"),
    nuke: bool = typer.Option(False, help="Make the data on the disk unrecoverable"),
    nuke_passes: int = typer.Option(3, help="Number of passes for the NUKE operation (3 or 7)"),
    algorithm: str = typer.Option('AES', help="Encryption algorithm ('AES' or 'ChaCha20')", case_sensitive=False)
):
    """
    Main function to handle disk operations including formatting, secure erasing, and nuking disks.
    
    Parameters:
        disk (str): The identifier of the disk (e.g., 'D:\\').
        format_disk (bool): Whether to quick format the selected disk.
        secure_erase (bool): Whether to securely erase the selected disk.
        erase_method (str): Method to use for secure erasing.
        nuke (bool): Whether to make data on the disk unrecoverable.
        nuke_passes (int): Number of passes for the nuke operation (3 or 7).
        algorithm (str): Encryption algorithm to use ('AES' or 'ChaCha20').
    """
    try:
        algorithm = algorithm.upper()
        if algorithm not in ['AES', 'CHACHA20']:
            raise UnsupportedAlgorithmError(f"Unsupported algorithm: {algorithm}")

        disk_manager = DiskManager()

        if disk:
            selected_disk = disk_manager.select_disk_by_letter(disk)
            print_disk_info(selected_disk)
            confirm = input("Is this the desired disk? (y/n): ")
            if confirm.lower() != 'y':
                print("Selection canceled.")
                raise SystemExit
        else:
            disks = disk_manager.get_disks()
            print("Available disks:")
            for disk_info in disks:
                print_disk_info(disk_info)
            available_numbers = [str(disk['Number']) for disk in disks]
            while True:
                number = input("Select the disk number: ")
                if number in available_numbers:
                    break
                print("Invalid number.")
            selected_disk = disk_manager.select_disk_by_number(number)
            print_disk_info(selected_disk)
            confirm = input("Is this the desired disk? (y/n): ")
            if confirm.lower() != 'y':
                print("Selection canceled.")
                raise SystemExit

        print(f"Selected disk: {selected_disk}")

        if format_disk:
            disk_manager.quick_format_disk(selected_disk)

        if secure_erase:
            disk_manager.secure_erase_disk(selected_disk, method=erase_method, algorithm=algorithm)

        if nuke:
            if nuke_passes not in [3, 7]:
                print("Number of passes must be 3 or 7.")
                raise SystemExit
            disk_manager.nuke_disk(selected_disk, algorithm=algorithm, passes=nuke_passes)

    except (DiskNotFoundError, InvalidDiskFormatError, UnsupportedAlgorithmError, InvalidEraseMethodError) as e:
        print("Error:", e)
    except OSError as e:
        print("Operating system error:", e)

if __name__ == "__main__":
    typer.run(main)