import os
import unittest


class MockResponse(object):

    def __init__(self, html):
        self.str_success_html = html


class TestScrapper(unittest.TestCase):

    def test_androidweekly_scrapper(self):
        html = str(os.environ["AW_HTML"])

        from scrapper import AndroidWeeklyScrapper
        AndroidWeeklyScrapper().scrap_response("", "http://androidweekly.net/issues/", "105")
        self.assertEqual([], [])
