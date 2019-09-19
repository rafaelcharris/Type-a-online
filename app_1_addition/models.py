from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_2_trust'
    players_per_group = None
    num_rounds = 5

    half_way = (num_rounds/2)
    time_limit = 60*4
    #shock = 0.2
    #piece_rate = 1000 #this code is in settings.py

    addends = [
        [10, 10, 10, 10, 11],
        [10, 10, 10, 10, 12],
        [10, 10, 10, 10, 13],
        [10, 10, 10, 10, 14],
        [10, 10, 10, 10, 15],
    ]


class Subsession(BaseSubsession):
    
    def creating_session(self):

        #loading treatments:
        if self.round_number == 1:
            treatment = itertools.cycle([1, 2, 3])
            for p in self.get_players():
                p.treatment = next(treatment) #this is just to keep it for the database. the code below is the useful one because thisone does not persist between rounds or apps
                p.participant.vars['treatment'] = p.treatment #this one is the one to use throught the entire code

        #loading addends to each player in session
        for p in self.get_players():
            p.addend_1 = Constants.addends[self.round_number - 1][0]
            p.addend_2 = Constants.addends[self.round_number - 1][1]
            p.addend_3 = Constants.addends[self.round_number - 1][2]
            p.addend_4 = Constants.addends[self.round_number - 1][3]
            p.addend_5 = Constants.addends[self.round_number - 1][4]
            p.solution = p.addend_1 + p.addend_2 + p.addend_3 + p.addend_4 + p.addend_5

            print("[[ APP_1_ADDITION ]] - CREATING SESSION - ROUND NUMBER ==> ", self.round_number, " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - PLAYER_ID ==> ", p.id_in_group, " <== ]]")
            
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - ADDENDS  ==> ",  p.addend_1, p.addend_2, p.addend_3, p.addend_4, p.addend_5, " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - SOLUTION ==> ",  p.solution, " <== ]]")
            
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.TREATMENT ==> ",  p.treatment, " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.PAR.VAR.TREATMENT ==> ",  p.participant.vars['treatment'], " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION -------------------------------------------------------------]]")


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    addend_1 = models.IntegerField()
    addend_2 = models.IntegerField()
    addend_3 = models.IntegerField()
    addend_4 = models.IntegerField()
    addend_5 = models.IntegerField()

    solution = models.IntegerField()
    answer = models.IntegerField(min = 50, max = 495)

    treatment = models.IntegerField()

    was_correct = models.BooleanField()
    acc_was_correct = models.IntegerField()
    acc_payoff = models.IntegerField()
    final_payoff = models.FloatField()

    def counting_future(self):
        # For "before_next_page() in pages.py"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        if self.answer == self.solution:
            self.was_correct = True
        elif self.answer != self.solution:
            self.was_correct = False
        else:
            self.was_correct = "ERROR 69"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............[[[ WAS_CORRECT ==> ", self.was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_FUTURE.............--------------------------------]")

    def counting_past(self):
        # For vars_for_template() in pages.py"

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        self.acc_was_correct = sum([p.was_correct for p in self.in_previous_rounds()])
        self.acc_payoff = sum([i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_previous_rounds()]])

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ WAS_CORRECT_LIST ==> ", [p.was_correct for p in self.in_previous_rounds()], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............--------------------------------]")

    def final_count(self): # In the last round the function counting past is not working, leaving the last info not inputed in the lists so i have to run it but using in_all_rounds()

        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        self.acc_was_correct = sum([p.was_correct for p in self.in_all_rounds()])
        self.acc_payoff = sum([i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_all_rounds()]]) #this creates a list multiplying every correct '1' times the piece rate and then adds it all

        if self.participant.vars['treatment'] == 1:
            self.final_payoff = self.acc_payoff
        elif self.participant.vars['treatment'] == 2 or self.participant.vars['treatment'] == 3:
            self.final_payoff = self.acc_payoff * self.session.config['shock']
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ FINAL_PAYOFF ==> ", self.final_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ TEEEEEEEEEEEEESSSTTTT ==> ", [i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_all_rounds()]], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")
