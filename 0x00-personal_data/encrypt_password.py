#!/usr/bin/env python3
"""
function that expects one string argument name password and returns
a salted, hashed password, which is a byte string
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
