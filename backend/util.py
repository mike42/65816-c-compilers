import os
from functools import cache


@cache
def compiler_exists(name: str) -> bool:
    return compiler_binary(name) != None


@cache
def compiler_binary(name: str) -> str | None:
    search_paths = os.getenv("PATH", "/bin:/usr/bin:/usr/local/bin").split(":")
    for item in search_paths:
        full_path = os.path.join(item, name)
        if os.path.exists(full_path):
            return full_path
    return None
