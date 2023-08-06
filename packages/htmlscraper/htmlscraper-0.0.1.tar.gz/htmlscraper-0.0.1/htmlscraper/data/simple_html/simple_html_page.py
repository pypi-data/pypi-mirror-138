import multiprocessing
import time
from abc import ABCMeta
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from threading import Thread
from typing import Callable, List, Generator, Tuple

from bs4 import BeautifulSoup
from requests import Session

from ..abstraction.abstract_page import AbstractPage
from ..abstraction.abstract_posting import AbstractPosting
from ..simple_html.simple_html_posting import SimpleHTMLPosting
from ..user.author import Author


class SimpleHTMLPage(AbstractPage, metaclass=ABCMeta):
    def __init__(self, session: Session, url: str) -> None:
        super().__init__(url, session)


class SimpleHTMLPageCollector(SimpleHTMLPage):
    def __init__(self, session: Session, url,
                 page_to_posting_info_fn: Callable[[BeautifulSoup], List[Tuple[str, int, str, Author]]],
                 next_page_url_fn: Callable[[BeautifulSoup], str],
                 workers=1,
                 timeout=2) -> None:
        """
        SimpleHTMLPageCollector is a class that can be used to collect the postings
        from the given url. To make the interal threads work properly, you must use it with the
        context manager. Ex) with SimpleHTMLPageCollector(...) as page:

        :param session: the requests session to use
        :param url: the url to collect postings from
        :param page_to_posting_info_fn: a function to convert the BeautifulSoup object into list of 'postings'.
        'postings' are tuples of (posting_url, posting_id, title, author).
        :param next_page_url_fn: a function to extract the url of the next page from the BeautifulSoup object.
        returns None if there is no next page.
        :param workers: the number of workers to use to read the postings.
        :param timeout: the timeout to use for the requests.get() call.
        """

        super().__init__(session, url)

        self._page_to_posting_info_fn = page_to_posting_info_fn
        self._next_page_url_fn = next_page_url_fn
        self._workers = workers
        self._timeout = timeout

        self._getPageThread = Thread(target=self.__read_page_content)

        self._postingHtmlQueue = Queue(multiprocessing.cpu_count() * 4)
        self._workerThread = Thread(target=self.__search_postings)
        self._workerRunning = False

        self._html = None

    def __read_page_content(self):
        for _ in range(1000):
            try:
                response = self._session.get(self._url, timeout=self._timeout)
                self._html = BeautifulSoup(response.content, 'html5lib')
                return
            except Exception as ex:
                print(ex)
                continue

        assert True, "Cannot read the page {} after trying for 1000 times. Something is wrong with the page itself?"

    def __search_postings(self):
        try:
            self._workerRunning = True
            print("search task running on", self._url)

            print("post search waiting for page parsing")
            self._getPageThread.join()
            assert self._html

            posting_info_list = self._page_to_posting_info_fn(self._html)

            with ThreadPoolExecutor(max_workers=self._workers) as pool:
                for posting_url, posting_id, title, author in posting_info_list:
                    pool.submit(self.__read_post, self._session,
                                posting_url, posting_id, title, author)
        finally:
            self._workerRunning = False
            print("search task stopped for", self._url)

    def __read_post(self, session: Session, url, post_id, title, author):
        response = session.get(url, timeout=self._timeout)
        html = BeautifulSoup(response.content, 'html5lib')
        self._postingHtmlQueue.put((url, post_id, title, author, html))

    def posting_generator(self) -> Generator[AbstractPosting, None, None]:
        """
        Get generator to generate the posts in this page.

        Notice that it takes a 'snapshot' at the moment when it has visited
        the page, so the postings may be outdated, yet there will be no
        duplicated postings 'within' the generator.

        This is intended to be used only 'once' and any generator after the first
        return value will produce nothing. Re-read the page in order to use the generator again.
        However, as explained above, the new page may generate the postings different
        than the last generator

        :return: the generator
        """

        print("generator waiting for page parsing")
        self._getPageThread.join()
        assert self._html

        while self._workerRunning or not self._postingHtmlQueue.empty():
            try:
                url, post_id, title, author, html = self._postingHtmlQueue.get(
                    timeout=1)

                yield SimpleHTMLPosting(self._session, url, post_id, title, author, html)
            except Empty:
                continue

    def next_page(self):
        """
        Get the new SimpleHTMLPage object for the next page.

        :return: the new SimpleHTMLPageCollector object. None if there is no next page.
        """

        self._getPageThread.join()
        assert self._html

        next_url = self._next_page_url_fn(self._html)
        if next_url is not None:
            return SimpleHTMLPageCollector(self._session,
                                           next_url,
                                           self._page_to_posting_info_fn,
                                           self._next_page_url_fn,
                                           workers=self._workers,
                                           timeout=self._timeout)
        else:
            return None

    def __enter__(self):
        self._getPageThread.start()
        self._workerThread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._workerThread.join()
