from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import time


class PlayerBot(Bot):

    def play_round(self):


        answer_set =   [229, 240, 253, 295, 254, 310, 302, 288, 240, 334, 278, 241, 261, 267, 232, 295, 298, 274, 332,
                        335, 278, 330, 366, 291, 277, 258, 274, 309, 278, 298, 230, 306, 157, 257, 356, 273, 317, 212,
                        140, 182, 290, 255, 379, 350, 444, 213, 295, 327, 238, 237, 230, 211, 402, 361, 281, 258, 199,
                        320, 270, 242]


        answer = answer_set[self.player.round_number - 1]

        if self.player.round_number == 1:
            yield pages.app_1_addition_intro
        if 'Primera etapa' in self.html:
            yield pages.app_1_addition_task, dict(answer = answer)
        if self.player.round_number == Constants.num_rounds:
            yield pages.app_1_addition_announcement
