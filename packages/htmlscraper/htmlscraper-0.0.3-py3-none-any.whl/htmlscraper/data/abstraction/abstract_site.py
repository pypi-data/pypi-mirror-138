class AbstractSite:
    def __init__(self) -> None:
        """
        A abstract class representing a site, which is a collection of pages.
        """
        self.users = dict()
