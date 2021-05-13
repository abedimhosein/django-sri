import base64
import hashlib
from functools import lru_cache
from pathlib import Path

from sri.algorithm import Algorithm
from sri.utils import get_cache

HASHERS = {
    Algorithm.SHA256: hashlib.sha256,
    Algorithm.SHA384: hashlib.sha384,
    Algorithm.SHA512: hashlib.sha512,
}


def calculate_hash(path: Path, algorithm: Algorithm) -> str:
    cache = get_cache()
    cache_key = get_cache_key(path, algorithm)
    file_hash = cache.get(cache_key)
    if file_hash is None:
        # Cache miss, do the calculation
        content = path.read_bytes()
        digest = HASHERS[algorithm](content).digest()
        file_hash = base64.b64encode(digest).decode()
        cache.set(cache_key, file_hash)
    return file_hash


@lru_cache()
def get_cache_key(path: Path, algorithm: Algorithm) -> str:
    hasher = HASHERS[algorithm]
    return hasher(str(path).encode()).hexdigest()
