import json
import re
import requests


class Joke(object):
    pattern = re.compile("^tell( me )?(a|another|some) joke$")

    def can_handle(self, text):
        return re.search(self.pattern, text)

    def handle(self, _):
        try:
            res = requests.get(url="https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke")
            return "%(setup)s... %(punchline)s" % json.loads(res.text)
        except Exception:
            return "I can't remember any right now"
