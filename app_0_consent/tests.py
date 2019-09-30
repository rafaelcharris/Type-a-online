from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random, itertools


class PlayerBot(Bot):
    names = itertools.cycle(['Alberto', 'Bolivar', 'Carlos', 'Danilo'])
    ids = itertools.cycle([33, 44, 55, 66])

    def play_round(self):
        yield (pages.Bienvenido)
        yield (pages.Consent, {'nombre': next(self.names), 'id_number': next(self.ids)})

