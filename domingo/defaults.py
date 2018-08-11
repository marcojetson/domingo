from domingo.commands.datetime import Time
from domingo.commands.funny import Joke
from domingo.commands.misc import WhatsUp, Dice, Welcome
from domingo.commands.weather import Rains, Snows
from domingo.commands.wikipedia import LookUp

from domingo.normalizations.english import expand_contractions

normalizations = (
    lambda s: s.lower(),
    expand_contractions,
)

commands = (
    Time(),
    Joke(),
    WhatsUp(),
    Dice(),
    Welcome(),
    Rains("Berlin"),
    Snows("Berlin"),
    LookUp(),
)
