import math

from enum import Enum

from pyquery import PyQuery as pq
from pip._vendor import requests


class Lang(Enum):
    EN = 0
    MM = 1
    TH = 2


class ReadingTime:
    def __init__(self, wpm=275):
        self.wpm = wpm

    def _word_count(self, text=None):
        if not text:
            return 0
        else:
            return len(str(text).split())

    def _word_per_sec(self):
        return self.wpm / 60

    def _total_reading_time_second(self, text=None):
        return self._word_count(text) / self._word_per_sec()

    def _total_reading_time_minute(self, text=None):
        return math.floor(self._total_reading_time_second(text) / 60)

    def _lang(self, lang=None):
        option = {
            Lang.EN: {"less_sec": "less than {reading_time} sec read", "sec": "{reading_time} sec read",
                      "min": "{reading_time} min read"},
            Lang.MM: {"less_sec": "ဖတ်ချိန် စက္ကန့်ဝက်", "sec": "ဖတ်ချိန် {reading_time} စက္ကန့် ",
                      "min": "ဖတ်ချိန် {reading_time}  မိနစ်"},
            Lang.TH: {"less_sec": "น้อยกว่า {reading_time} วินาทีอ่าน", "sec": "อ่าน {reading_time} วินาที ",
                      "min": "อ่าน {reading_time}  นาที"}
        }
        return option[lang]

    def _extract_text(self, url):
            response = requests.get(url)
            html=response.text
            texts = pq(html)('body p').text()
            return texts

    def estimate(self, text=None, format=True, lang=Lang.EN):

        if format is True:
            if self._total_reading_time_second(text) < 60:
                if self._total_reading_time_second(text) < 10:
                    return self._lang(lang)["less_sec"].format(reading_time=self._total_reading_time_second(text))
                else:
                    return self._lang(lang)["sec"].format(reading_time=self._total_reading_time_second(text))
            else:
                return self._lang(lang)["min"].format(reading_time=self._total_reading_time_minute(text))
        else:
            if self._total_reading_time_second(text) < 60:
                return self._total_reading_time_second(text)
            else:
                return self._total_reading_time_minute(text)

    def estimate_url(self, url=None, format=True, lang=Lang.EN):
        texts = self._extract_text(url)
        return self.estimate(texts, format, lang)
