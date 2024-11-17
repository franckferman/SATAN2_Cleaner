#!/usr/bin/env python3
# utilities.py

"""
SATAN2 Cleaner - Utilities Module

Description:
Provides utility functions used throughout the SATAN2 Cleaner project, including
operating system checks and disk information display.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

import os

def is_windows():
    """
    Check if the operating system is Windows.

    Returns:
        bool: True if the system is Windows, False otherwise.
    """
    return os.name == 'nt'

def print_disk_info(disk_info):
    """
    Display information about a given disk.

    Parameters:
        disk_info (dict): A dictionary containing disk details such as 'Number', 'FriendlyName', and 'Size'.
    """
    print(f"Number: {disk_info['Number']}, FriendlyName: {disk_info['FriendlyName']}, "
          f"Size: {disk_info['Size'] / 1e+9:.2f} GB")
