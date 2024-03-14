import functools
import math
import os
import time
import typing

URL_DATA_TYPE = typing.Dict[str, str]

__all__ = ('UrlsList',)


class UrlsList:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.refresh_time = time.time()
        self.queue_time = self.refresh_time

    def to_queue(self) -> typing.List[URL_DATA_TYPE]:
        current_time = time.time()
        rounded = math.floor(current_time/self.interval) * self.interval
        factor = len(self._urls_data) / self.interval
        start_index = math.floor((self.queue_time-rounded)*factor)
        end_index = math.floor((current_time-rounded)*factor)
        print(factor, start_index, end_index)
        data = []
#        data.extend(self._urls_data)
        if start_index < 0:
            data.extend(self._urls_data[start_index:])
            start_index = 0
        data.extend(self._urls_data[start_index:end_index])
        self.queue_time = current_time
        return data

    @functools.cached_property
    def interval(self) -> int:
        return int(os.path.basename(self.filepath).split('_', 1)[0])

    @functools.cached_property
    def _urls_data(self) -> typing.List[URL_DATA_TYPE]:
        with open(self.filepath, 'r') as f:
            urls = []
            for line in f:
                line = line.strip()
                if len(line) == 0 or line.startswith('#'):
                    continue
                arguments = line.split(';')
                for i, argument in enumerate(arguments):
                    if argument.startswith('url='):
                        arguments = arguments[0:i] + [';'.join(arguments[i:])]
                urls.append(dict((s.split('=', 1) for s in arguments)))
        urls = sorted(urls, key=lambda d: d['url'])
        return urls

    @functools.cached_property
    def _urls(self) -> typing.Set[str]:
        return {data['url'] for data in self._urls_data}

    def lookup(self, url: str) -> bool:
        return url in self._urls

    def lookup_data(self, url: str) -> bool:
        for data in self._urls_data:
            if data['url'] == url:
                return data
        return None

    def refresh(self) -> 'UrlsList':
        if not os.path.isfile(self.filepath):
            return None
        if os.path.getmtime(self.filepath) > self.refresh_time:
            self.refresh_time = time.time()
            return UrlsList(self.filepath)
        return self

