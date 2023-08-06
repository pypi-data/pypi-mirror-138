from ..abstraction.abstract_attachment import AbstractAttachment
from ..user.author import Author


class Comment(AbstractAttachment):
    def __init__(self, unique_id: int, author: Author, time: str, content: str) -> None:
        """
        A comment on a post.
        """
        super().__init__()
        self._unique_id = unique_id
        self._author = author
        self._time = time
        self._content = content

    def unique_id(self):
        return self._unique_id

    def author(self):
        return self._author

    def time(self):
        return self._time

    def content(self):
        return self._content

    def __repr__(self):
        return "(Author={}, time={}, content={})".format(self._author, self._time, self._content)
