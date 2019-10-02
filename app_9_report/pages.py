from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AdminReport(Page):
    def is_displayed(self):
        return False


class app_9_report_summary(Page):
    def vars_for_template(self):
        self.player.push_vars_to_report_summary()


#class the_end(Page):
#    form_model = 'player'
#    form_fields = ['e_mail']
#
##    def vars_for_template(self):
##        self.player.report_vars_for_database()
#
#    def is_displayed(self):
#        return True


page_sequence = [
    app_9_report_summary,
    #the_end,
]
