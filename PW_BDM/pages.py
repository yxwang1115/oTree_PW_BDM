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
        if self.subsession.round_number == 2:
            if self.player.paying_round == 1:
                self.player.set_round1_payoff()
            else:
                self.player.set_round2_payoff()


class Results(Page):
    def vars_for_template(self):
        return {
            'pay_round': self.player.participant.vars['paying_round'],
            'item1': self.player.in_round(1).item_value,
            'item2': self.player.in_round(2).item_value,
            'bid1': self.player.in_round(1).bid_amount,
            'bid2': self.player.in_round(2).bid_amount,
        }

    def is_displayed(self):
        return self.subsession.round_number == 2


page_sequence = [Introduction, Bid, Results]
