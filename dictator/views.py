from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        pass

class WaitForP1(WaitPage):
    pass

class WaitForP2(WaitPage):
    pass



class Results(Page):
    pass

class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'total_payoff': sum([p.payoff for p in self.player.in_all_rounds()]),
        }

class Send(Page):

    #include error page

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 1 and (self.round_number % 6 == 1 or self.round_number % 6 == 2)


    

class Receive(Page):

    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 0

    def vars_for_template(self):
        return {
            'keep_amount': Constants.endowment - self.group.sent_amount 
        }


class Threat(Page):
    form_model = models.Group
    form_fields = ['threat']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 0 and (self.round_number % 6 == 3 or self.round_number % 6== 4)


class Negotiate(Page):
    form_model = models.Group
    form_fields= ['negotiate', 'offer']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 0 and (self.round_number % 6 == 5 or self.round_number % 6== 0)

class SendWithThreat(Page):
    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 1 and (self.round_number % 6 == 3 or self.round_number % 6== 4)

class SendWithNegotiate(Page):
    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 1 and (self.round_number % 6 == 5 or self.round_number % 6== 0)


class Offer(Page):
    form_model = models.Group
    form_fields = ['actual_offer']

    def is_displayed(self):
        return self.player.id_in_group % 2 == 0 and self.group.offer_accepted and (self.round_number % 6 == 5 or self.round_number % 6== 0)

page_sequence = [
    Instructions,
    # WaitForP2,
    Threat,
    Negotiate,
    WaitForP2,
    SendWithThreat,
    SendWithNegotiate,
    Send,
    WaitForP1,
    Receive,
    WaitForP2,
    Offer,
    ResultsWaitPage,
    Results,
    FinalResults
]
