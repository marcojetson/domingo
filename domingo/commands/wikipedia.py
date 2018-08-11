import json
import re
import requests


class LookUp(object):
    pattern = re.compile("^look ?up (?P<term>.+)$")

    def can_handle(self, text):
        return re.search(self.pattern, text)

    def handle(self, text):
        match = re.search(self.pattern, text)
        term = match.group("term")

        try:
            res = requests.get(url="https://en.wikipedia.org/w/api.php", params={
                "format": "json",
                "action": "query",
                "prop": "extracts",
                "exintro": "",
                "explaintext": "",
                "titles": term,
            })

            page = json.loads(res.text)["query"]["pages"].itervalues().next()
            extract = page["extract"]

            if extract:
                return extract.encode("utf-8")

            return "I can't say anything about %s" % term
        except Exception as e:
            print e
            return "I can't find anything for %s" % term
