from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):

    def vars_for_template(self):
        return {
            'treatment': self.player.participant.vars['treatment'],
        }

    def is_displayed(self):
        return self.subsession.round_number == 1


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']

    def vars_for_template(self):
        return {
            'treatment':  self.player.participant.vars['treatment'],
        }

    def before_next_page(self):
        self.player.set_payoff()


class Results(Page):
    pass


page_sequence = [Introduction, Bid, Results]
