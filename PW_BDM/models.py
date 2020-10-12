from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
)


class Constants(BaseConstants):
    name_in_url = 'Valuation_Lottery'
    players_per_group = None
    num_rounds = 2
    endowment = 15
    min_allowable_bid = 0
    max_allowable_bid = 15
    h_pay = 15
    l_pay = 0

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            import random
            p.random_draw = random.randrange(1, 100)

            item_value = random.uniform(
                Constants.min_allowable_bid, Constants.max_allowable_bid
            )
            p.item_value = round(item_value, 2)


            if self.round_number == 1:
                for p in self.get_players():
                    p.participant.vars['paying_round'] = random.randint(1, Constants.num_rounds)
                    p.paying_round = p.participant.vars['paying_round']
                    p.participant.vars['treatment'] = random.choice(['positive', 'negative', 'neutral'])
                    p.treatment = p.participant.vars['treatment']


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    paying_round = models.IntegerField(
        doc="""Which round counts as paying round """
    )

    treatment = models.StringField(
        doc="""Which demand treatment does the participant belong to """
    )

    item_value = models.CurrencyField(
        doc="""random value of the item to be auctioned, random for treatment"""
    )
    random_draw = models.FloatField(
        doc="""To determine the outcome of the lottery"""
    )

    bid_amount = models.CurrencyField(
        min=Constants.min_allowable_bid,
        max=Constants.max_allowable_bid,
        doc="""Amount bidded by the player""",
        label="Bid price"
    )

    def set_round1_payoff(self):
        import random

        if self.in_round(1).bid_amount >= self.in_round(1).item_value:
            if self.random_draw <= 10:
                self.payoff = Constants.endowment - self.in_round(1).item_value + Constants.h_pay

            else:
                self.payoff = Constants.endowment - self.in_round(1).item_value + Constants.l_pay

        else:
            self.payoff = Constants.endowment

    def set_round2_payoff(self):
        import random

        if self.in_round(2).bid_amount >= self.in_round(2).item_value:
            if self.random_draw <= 90:
                self.payoff = Constants.endowment - self.in_round(2).item_value + Constants.h_pay

            else:
                self.payoff = Constants.endowment - self.in_round(2).item_value + Constants.l_pay

        else:
            self.payoff = Constants.endowment

