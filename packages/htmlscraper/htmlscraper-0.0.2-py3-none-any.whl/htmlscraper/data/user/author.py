from ..abstraction.user import User


class Author(User):
    def __init__(self, str_id: str) -> None:
        super().__init__(str_id)
