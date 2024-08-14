#!/usr/bin/env python3
"""
_hash_password method that takes in password string arguments and returns bytes
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt's hashing function
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
