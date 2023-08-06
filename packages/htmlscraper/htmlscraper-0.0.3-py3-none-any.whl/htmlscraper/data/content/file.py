from data.abstraction.abstract_attachment import AbstractAttachment


class File(AbstractAttachment):
    def __init__(self) -> None:
        """
        A file attached to a posting.
        """
        super().__init__()
