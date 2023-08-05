import io
import signal
import time
import urllib.parse

import requests


class GradeMage:
    TIME_TO_LIVE = 6

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

                start = time.time()

                self.solve(instream, outstream)

                end = time.time()

                elapsed = int((end - start) * 1000)

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
