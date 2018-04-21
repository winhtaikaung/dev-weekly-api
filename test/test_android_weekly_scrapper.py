import unittest

from pip._vendor import requests

from readingtime import ReadingTime


class MockResponse(object):

    def __init__(self, html):
        self.str_success_html = html


class TestScrapper(unittest.TestCase):

    def test_page(self):
        # print(generate_meta(10, 1, [None] * 100))
        # print(generate_meta(10, 10, [None] * 100))
        for issue_number in range(120, 305):
            print(issue_number)
            requests.get("http://localhost:5000/scrap/db87092d90714c66ba3f32471e4c5ddf/{0}".format(issue_number))
        print("done")


class TestReaingTime(unittest.TestCase):
    def test_zero_reading_time(self):
        readingTime = ReadingTime()
        assert readingTime.estimate("", False) == 0

    def test_url_reading_time(self):
        readingTime = ReadingTime()
        print(readingTime.estimate_url(
            "https://medium.com/yangonpy/https-medium-com-yangonrb-use-ruby-to-mass-download-an-instagram-user-public-images-6b41556df50c",
            True))
