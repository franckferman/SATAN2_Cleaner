#!/usr/bin/env python3
# __init__.py

"""
SATAN2 Cleaner - Disk Utilities Package

Description:
Initializes the disk utilities package for SATAN2 Cleaner. This package includes modules for
disk management, encryption, and utility functions to support secure formatting and erasure of disks.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

from .disk_manager import DiskManager
from .exceptions import (
    DiskNotFoundError, InvalidDiskFormatError, UnsupportedAlgorithmError, InvalidEraseMethodError
)
from .utilities import is_windows, print_disk_info
from .encryption import encrypt_disk_with_password, derive_key
