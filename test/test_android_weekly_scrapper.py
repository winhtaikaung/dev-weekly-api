import unittest

from database import generate_meta


class MockResponse(object):

    def __init__(self, html):
        self.str_success_html = html


class TestScrapper(unittest.TestCase):

    def test_page(self):
        print(generate_meta(10, 1, [None] * 100))
        print(generate_meta(10, 10, [None] * 100))
