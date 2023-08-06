class User:
    def __init__(self, str_id: str) -> None:
        self._str_id = str_id

    def str_id(self):
        return self._str_id

    def set_str_id(self, str_id):
        self._str_id = str_id

    def __repr__(self):
        return 'User(str_id={})'.format(self._str_id)
