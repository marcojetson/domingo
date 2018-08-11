import json
import re
import requests


def mw_search_location(query):
    try:
        res = requests.get(url="https://www.metaweather.com/api/location/search/", params={"query": query})
        return json.loads(res.text)[0]["woeid"]
    except Exception:
        return None


def mw_fetch_forecast(query):
    location_id = mw_search_location(query)

    if not location_id:
        return None

    try:
        res = requests.get(url="https://www.metaweather.com/api/location/%s" % location_id)
        return json.loads(res.text)["consolidated_weather"]

    except Exception as e:
        print e
        return None


def extract_place(pattern, text, current_place):
    match = re.search(pattern, text)
    place = match.group("place")

    if not place or place in ("my place", "my house", "my home", "home", "outside"):
        place = current_place

    return place


class Rains(object):
    pattern = re.compile("^is it raining( ((in|at) (?P<place>.+)|outside))?$")
    weather_state_res_map = {
        "sl": "It's sleeting in %s",
        "h": "It's hailing in %s",
        "hr": "It's raining heavily in %s",
        "lr": "It's raining in %s",
        "s": "It's raining in %s",
    }

    def __init__(self, current_place):
        self.current_place = current_place

    def can_handle(self, text):
        return re.search(self.pattern, text)

    def handle(self, text):
        place = extract_place(self.pattern, text, self.current_place)
        forecast = mw_fetch_forecast(place)

        if not forecast:
            return "I couldn't find the forecast for %s" % place

        return self.weather_state_res_map.get(forecast[0]["weather_state_abbr"], "It's not raining in %s") % place


class Snows(object):
    pattern = re.compile("^is it snowing( ((in|at) (?P<place>.+)|outside))?$")

    def __init__(self, current_place):
        self.current_place = current_place

    def can_handle(self, text):
        return re.search(self.pattern, text)

    def handle(self, text):
        place = extract_place(self.pattern, text, self.current_place)
        forecast = mw_fetch_forecast(place)

        if not forecast:
            return "I couldn't find the forecast for %s" % place

        if forecast[0]["weather_state_abbr"] == "sn":
            return "It's snowing in %s" % place

        return "I don't see any snow in %s" % place
