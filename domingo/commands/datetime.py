import time


class Time(object):
    def can_handle(self, text):
        return text in ("what time is it", "what is the time")

    def handle(self, _):
        return "it's %s" % time.strftime("%H:%M")
