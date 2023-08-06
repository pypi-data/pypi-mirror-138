import imp
import unittest
import requests

from typing import List, Tuple

from htmlscraper.data.simple_html.simple_html_page import SimpleHTMLPageCollector
from htmlscraper.data.user.author import Author


class TestSimpleHtmlPage(unittest.TestCase):

    def test_generator(self):
        def posting_to_info(soup) -> List[Tuple[str, int, str, Author]]:
            ol = soup.find('ol')
            li = ol.find_all('li')

            postings = []
            for link in li:
                a = link.find('a')
                title = a.text
                ref = a['href']
                postings.append(
                    ('http://www.columbia.edu/~fdc/sample.html{}'.format(ref),
                     0,
                     title,
                     Author('some author')))

            return postings

        def next_page_url(soup) -> str:
            return None

        session = requests.Session()
        with SimpleHTMLPageCollector(
                session=session,
                url="http://www.columbia.edu/~fdc/sample.html",
                page_to_posting_info_fn=posting_to_info,
                next_page_url_fn=next_page_url,
                workers=1,
                timeout=2) as collector:

            for posting in collector.posting_generator():
                print(posting)


if __name__ == '__main__':
    unittest.main()
