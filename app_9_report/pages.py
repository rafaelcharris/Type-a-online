from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AdminReport(Page):
    def is_displayed(self):
        return False


class the_end(Page):
    form_model = 'player'
    form_fields = ['e_mail']

#    def vars_for_template(self):
#        self.player.report_vars_for_database()

    def is_displayed(self):
        return True


page_sequence = [
    the_end,
]
