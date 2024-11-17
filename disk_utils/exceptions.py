#!/usr/bin/env python3
# exceptions.py

"""
SATAN2 Cleaner - Exceptions Module

Description:
Defines custom exceptions used in the SATAN2 Cleaner project for handling
errors related to disk operations, invalid formats, unsupported algorithms, and more.

Created By  : Franck FERMAN
Created Date: 17/11/2024
Version     : 1.0.0
"""

class DiskNotFoundError(Exception):
    """
    Raised when the specified disk cannot be found.
    """
    pass

class InvalidDiskFormatError(Exception):
    """
    Raised when the disk format is invalid or unsupported.
    """
    pass

class UnsupportedAlgorithmError(Exception):
    """
    Raised when the encryption algorithm is not supported.
    """
    pass

class InvalidEraseMethodError(Exception):
    """
    Raised when the specified erase method is invalid or unrecognized.
    """
    pass
