import unittest

from pip._vendor import requests

from database import generate_meta


class MockResponse(object):

    def __init__(self, html):
        self.str_success_html = html


class TestScrapper(unittest.TestCase):

    def test_page(self):
        print(generate_meta(10, 1, [None] * 100))
        print(generate_meta(10, 10, [None] * 100))
        for issue_number in range(120,302):
            print(issue_number)
            requests.get("http://localhost:5000/scrap/5d4a37c7eaf94348ba74045798172b7f/{0}".format(issue_number))
        print ("done")
