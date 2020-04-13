from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants, levenshtein, distance_and_ok
from django.conf import settings
import time

class intro(Page):

    def is_displayed(self):
        return self.player.round_number == 1

    def before_next_page(self):
        self.participant.vars['expiry'] = time.time() + self.session.config['time_limit']

class Transcribe(Page):
    form_model = 'player'
    form_fields = ['transcribed_text']

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.participant.vars['expiry'] - time.time() > 0

    def vars_for_template(self):
        return dict(
            reference_text=Constants.reference_texts[self.round_number - 1],
            debug=settings.DEBUG,
            required_accuracy = 100 * (1 - Constants.allowed_error_rate)
        )

class Results(Page):

    def is_displayed(self):
        self.player.set_payoff()
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        table_rows = []
        for prev_player in self.player.in_all_rounds():
            row = dict(
                round_number=prev_player.round_number,
                reference_text_length=len(Constants.reference_texts[prev_player.round_number - 1]),
                transcribed_text_length= len(prev_player.transcribed_text) if prev_player.transcribed_text is not None else 0, #Intentar arreglar error
                distance=prev_player.levenshtein_distance,
                payoff = prev_player.payoff
            )
            table_rows.append(row)

        return dict(table_rows=table_rows,
                    final_payment = self.participant.payoff)

class Announcement(Page):

    def is_displayed(self):
        self.player.set_final_payoff()
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        #En esta pagina payoff es el pago que tendría si no hubiera shock
        return dict(
            final_payoff = self.player.final_payoff,
            payoff = self.participant.payoff
        )

    def before_next_page(self):
        self.player.report_addition()

page_sequence = [
    intro,
    Transcribe,
    Results,
    Announcement]
