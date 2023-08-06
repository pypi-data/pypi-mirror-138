from abc import abstractmethod, ABCMeta

from bs4 import BeautifulSoup
from requests import Session

from ..user.author import Author


class PostingVisitor(metaclass=ABCMeta):
    def __init__(self) -> None:
        """
        Abstract visitor class for visiting a posting.
        The 'visitor' must override the visit_content method to extract
        the information needed from the html response.

        Strictly speaking, this isn't exactly following the visitor pattern,
        yet it still provides the flexibility of having different visitors for parsing
        different types of postings.
        """
        pass

    def visit_content(self, soup: BeautifulSoup) -> None:
        return None


class AbstractPosting:
    def __init__(self, session: Session, url: str, post_id: int, title: str, author: Author,
                 html_content: BeautifulSoup) -> None:
        """
        Posting of the page.
        :param session: requests.Session
        :param url: url of the posting
        :param post_id: id of the posting
        :param title: title of the posting
        :param author: author of the posting
        :param html_content: BeautifulSoup of the posting
        """
        self._session = session
        self._url = url
        self._post_id = post_id
        self._title = title
        self._author = author
        self._html_content = html_content

    def url(self) -> str:
        return self._url

    def post_id(self) -> int:
        return self._post_id

    def title(self) -> str:
        return self._title

    def author(self) -> Author:
        return self._author

    @abstractmethod
    def accept(self, visitor: PostingVisitor) -> None:
        """
        abstract method to follow the visitor pattern.
        """
        pass

    def __repr__(self):
        return "Posting(id={}, title={}, author={})".format(self._post_id, self._title, self._author)
