from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Yuzhu Zhang'

doc = """
Design the experiment interface for an improved dictator game
"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 6
    endowment = c(100)
    # endowment_amount = 100


class Subsession(BaseSubsession):

    #create_session will be excuted n times depends on num_rounds
    def creating_session(self):
        paying_round = random.randint(1, Constants.num_rounds)
        self.session.vars['paying_round'] = paying_round
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(min = 0, max = Constants.endowment)
    threat = models.CurrencyField(min = 0, max = Constants.endowment)
    negotiate = models.CurrencyField(min = 0, max = Constants.endowment)
    offer = models.CurrencyField(min = 0)
    actual_offer = models.CurrencyField(min = 0)

    offer_accepted = models.BooleanField() # or booleanfeild

    received_amount = models.CurrencyField()


    def set_payoffs(self):
        p1 = self.get_player_by_role("Dictator")
        p2 = self.get_player_by_role("Receiver")
        self.received_amount = Constants.endowment - self.sent_amount
        if self.offer_accepted == True:
            bonus = self.actual_offer if self.actual_offer != None else 0
            p1.payoff = self.received_amount + bonus
            p2.payoff = self.sent_amount - bonus
        else:
            p1.payoff = 0
            p2.payoff = 0
        # p1.finalpayoff = p1.finalpayoff + p1.payoff
        # p2.finalpayoff = p2.finalpayoff + p2.payoff



class Player(BasePlayer):
    # accpeted = models.BooleanField()
    # self.finalpayoff = c(0)
    
    def role(self):
        if self.id_in_group % 2 == 1:
            return "Dictator"
        else:
            return "Receiver"
