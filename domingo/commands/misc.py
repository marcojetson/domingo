import random


class WhatsUp(object):
    def can_handle(self, text):
        return text == "what is up"

    def handle(self, _):
        return "the sky"


class Dice(object):
    def can_handle(self, text):
        return text == "roll a dice"

    def handle(self, _):
        return "you rolled a %s" % random.randint(1, 6)


class Welcome(object):
    res = (
        "you are welcome",
        "just doing my job",
        "it's my pleasure",
        "no problem",
    )

    def can_handle(self, text):
        return text in ("thanks", "thank you", "many thanks", "thanks a lot", "thank you very much")

    def handle(self, _):
        return random.choice(self.res)
