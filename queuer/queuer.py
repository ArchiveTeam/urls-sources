import os
import random
import re
import string
import threading
import time
import typing
import urllib.parse

from queuer.hidden import queue_items
from queuer.urls import UrlsList, URL_DATA_TYPE

RANDOM_CHARS = string.hexdigits

__all__ = ('Lists', 'Queuer')


class Lists(threading.Thread):
    def __init__(self, directory: str = '.', interval: int = 10):
        super().__init__()
        self._directory = directory
        self._lists = {}
        self.interval = interval

    def run(self):
        while True:
            self.refresh()
            for filename in os.listdir(self._directory):
                if not re.search(r'^[0-9]+_.+\.txt$', filename):
                    continue
                filepath = os.path.join(self._directory, filename)
                self.add(filepath)
            time.sleep(self.interval)

    def add(self, filepath: str):
        if filepath not in self._lists:
            self._lists[filepath] = UrlsList(filepath)
            return True
        return False

    def refresh(self):
        for filepath, urls_list in self._lists.items():
            self._lists[filepath] = urls_list.refresh()

    def to_queue(self) -> typing.List[URL_DATA_TYPE]:
        data = []
        for urls_list in self._lists.values():
            x = urls_list.to_queue()
            print(len(x))
            data.extend(x)
        return data

    @property
    def directory(self) -> str:
        return self._directory


class Queuer(threading.Thread):
    def __init__(self, lists: Lists, interval: int = 10):
        super().__init__()
        self._lists = lists
        self.interval = interval

    def run(self):
        while True:
            items = []
            for url_data in self.lists.to_queue():
                if 'random' in url_data:
                    url_data['random'] = ''.join(random.choices(RANDOM_CHARS, k=8))
                items.append('custom:'+urllib.parse.urlencode(
                    url_data,
                    quote_via=urllib.parse.quote
                ))
            queue_items(items)
            time.sleep(self.interval)

    @property
    def lists(self):
        return self._lists

