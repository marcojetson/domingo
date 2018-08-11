import argparse
import imp
import logging
from os.path import abspath, dirname

from speech_recognition import Recognizer, Microphone, UnknownValueError

from domingo.text_to_speech import say

app_dir = dirname(abspath(__file__))

parser = argparse.ArgumentParser(
    description="a not so smart virtual assistant",
    fromfile_prefix_chars="@",
    add_help=False
)

parser.add_argument(
    "-p",
    "--prefix",
    action="store",
    default="",
    help="prefix for commands, e.g. hey domingo"
)

parser.add_argument(
    "-s",
    "--settings",
    action="store",
    help="settings file for custom normalization and commands"
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbosity level"
)

parser.add_argument(
    "-?",
    "--help",
    action="help",
    help="show this help message and exit"
)

args = parser.parse_args()

loglevels = [logging.WARNING, logging.INFO, logging.DEBUG]
loglevel = loglevels[min(len(loglevels) - 1, args.verbose)]
logging.basicConfig(level=loglevel, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

if args.settings:
    settings = imp.load_source("", args.settings)
else:
    import domingo.defaults as settings

recognizer = Recognizer()
source = Microphone()

logger.info("a moment of silence, please...")
with source: recognizer.adjust_for_ambient_noise(source)
logger.info("minimum energy threshold set to %s" % recognizer.energy_threshold)

while True:
    print("listening...")
    with source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("> %s" % text)

        for normalization in settings.normalizations:
            text = normalization(text)

        if text.find(args.prefix) != 0:
            continue

        text = text[len(args.prefix):].lstrip()

        for command in settings.commands:
            if not command.can_handle(text):
                continue

            logger.info("executing %s" % command)
            result = command.handle(text)

            if result:
                print("< %s" % result)
                say(result)

            break

    except UnknownValueError, RequestError:
        pass
