from ..abstraction.abstract_attachment import AbstractAttachment


class Content(AbstractAttachment):
    def __init__(self, content: str) -> None:
        """
        Text version of the content of the posting. This is the most common type of 'attachment'
        for a posting.
        """
        super().__init__()
        self._content = content

    def content(self):
        return self._content

    def __repr__(self):
        return "(content={})".format(self._content)
