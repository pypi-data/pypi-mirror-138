from typing import Callable

from ..user.author import Author

author_table = dict()


def get_or_new_author(name: str, fn: Callable[[str], Author]):
    if name not in author_table:
        author_table[name] = fn(name)

    return author_table[name]
