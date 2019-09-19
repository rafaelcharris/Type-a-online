from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    #otree test session_config_1 4

    def play_round(self):
        if self.player.id_in_group == 1:
            yield(pages.app_1_addition_task, {'answer': 51})
            yield(pages.app_1_addition_task, {'answer': 52})
            yield(pages.app_1_addition_task, {'answer': 53})
            yield(pages.app_1_addition_task, {'answer': 54})
            yield(pages.app_1_addition_task, {'answer': 55})
            yield(pages.app_1_addition_announcement)
        elif self.player.id_in_group == 2:
            yield(pages.app_1_addition_task, {'answer': 51})
            yield(pages.app_1_addition_task, {'answer': 52})
            yield(pages.app_1_addition_task, {'answer': 53})
            yield(pages.app_1_addition_task, {'answer': 54})
            yield(pages.app_1_addition_task, {'answer': 55})
            yield(pages.app_1_addition_announcement)
        if self.player.id_in_group == 3:
            yield(pages.app_1_addition_task, {'answer': 100})
            yield(pages.app_1_addition_task, {'answer': 200})
            yield(pages.app_1_addition_task, {'answer': 53})
            yield(pages.app_1_addition_task, {'answer': 400})
            yield(pages.app_1_addition_task, {'answer': 495})
            yield(pages.app_1_addition_announcement)


