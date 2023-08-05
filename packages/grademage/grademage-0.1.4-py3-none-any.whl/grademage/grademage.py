import datetime
import io
import signal
import urllib.parse

import requests


class GradeMage:
    TIME_TO_LIVE = 4

    def handler(self, sig, frame):
        raise TimeoutError()

    def solve(self, instream, outstream):
        raise NotImplementedError("Please implement code logic")

    def measure(self, url: str, item: str):
        x = urllib.parse.urljoin(url, item + ".in")
        y = urllib.parse.urljoin(url, item + ".out")

        source = requests.get(x).content.decode("utf-8")
        target = requests.get(y).content.decode("utf-8")

        with io.StringIO(source) as instream, io.StringIO() as outstream:
            try:
                signal.signal(signal.SIGALRM, self.handler)
                signal.alarm(self.TIME_TO_LIVE)

                start = datetime.datetime.now()

                self.solve(instream, outstream)

                end = datetime.datetime.now()

                elapsed = int((end - start).total_seconds() * 1000)  # milliseconds

                correct = target.strip() == outstream.getvalue().strip()
            except:
                correct = False
                elapsed = -1
            finally:
                signal.alarm(0)

        return correct, elapsed

    def grade(self, url: str, items: list):
        """
        `url` is the path of test data while items are the file names (without .in or .out)
        """
        result = []
        for item in items:
            metric = self.measure(url, item)
            result.append(metric)

        return result
