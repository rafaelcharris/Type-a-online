from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.player.metarole == True:
            yield pages.app_2_trust_send, dict(sent_amount = 2)
            yield pages.app_2_trust_sendback, dict(sent_back_amount_if1 = True, sent_back_amount_if2 = True)
        if self.player.metarole == False:
            yield pages.app_2_trust_sendback, dict(sent_back_amount_if1 = True, sent_back_amount_if2 = True)
            yield pages.app_2_trust_send, dict(sent_amount = 2)
#        yield pages.app_2_trust_beliefs, dict(sender_belief_if1 = True,
#                                              sender_belief_if2 = True,
#                                              sender_belief_shock = 2,
#                                              receiver_belief = 2,
#                                              receiver_belief_shock = 2)
#        yield pages.app_2_trust_main_results

