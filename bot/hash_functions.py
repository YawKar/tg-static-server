import hashlib
from base64 import b85encode


def mk_base85_hash(relative_path: str) -> str:
    return b85encode(
        hashlib.sha256(relative_path.encode(), usedforsecurity=False).digest()
    ).decode()


def compare_by_hash(path1: str, path2: str) -> bool:
    """
    returns: whether given paths are equal with respect to base85_hash
    """
    return mk_base85_hash(path1) == mk_base85_hash(path2)
