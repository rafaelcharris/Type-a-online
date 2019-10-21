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
    name_in_url = 'app_2_addition'
    players_per_group = None
    num_rounds = 40

    half_way = (num_rounds/2)
    #time_limit = 60*4
    shock = 0.2
    piece_rate = 1000

    addends = [[13, 21, 92, 25, 78], [14, 53, 50, 42, 81], [84, 26, 29, 19, 95], [34, 96, 81, 45, 39], [10, 12, 90, 67, 75],
               [80, 45, 56, 47, 82], [87, 36, 86, 46, 47], [46, 54, 95, 16, 77], [45, 31, 77, 51, 36], [95, 87, 88, 54, 10],
               [69, 13, 40, 63, 93], [99, 41, 21, 32, 48], [38, 61, 66, 12, 84], [23, 85, 99, 12, 48], [13, 73, 50, 39, 57],
               [25, 86, 18, 75, 91], [64, 89, 16, 96, 33], [39, 31, 69, 67, 68], [22, 40, 89, 83, 98], [88, 89, 45, 52, 61],
               [51, 54, 77, 77, 19], [45, 73, 97, 30, 85], [75, 37, 83, 90, 81], [43, 87, 77, 73, 11], [22, 58, 47, 68, 82],
               [22, 33, 61, 70, 72], [17, 29, 73, 78, 77], [19, 94, 96, 20, 80], [85, 73, 30, 39, 51], [28, 88, 66, 90, 26],
               [27, 48, 92, 35, 28], [65, 97, 62, 48, 34], [22, 34, 19, 69, 13], [18, 34, 64, 77, 64], [83, 76, 52, 48, 97],
               [10, 87, 59, 64, 53], [44, 45, 70, 81, 77], [34, 70, 47, 11, 50], [58, 20, 18, 28, 16], [14, 47, 70, 22, 29],
               [83, 27, 88, 17, 75], [27, 64, 51, 20, 93], [99, 68, 59, 70, 83], [85, 74, 99, 18, 74], [76, 86, 91, 95, 96],
               [12, 27, 45, 91, 38], [72, 83, 54, 64, 22], [48, 56, 35, 92, 96], [31, 58, 26, 62, 61], [35, 41, 40, 35, 86],
               [12, 70, 52, 53, 43], [75, 72, 19, 28, 17], [92, 95, 41, 94, 80], [93, 53, 85, 87, 43], [68, 41, 53, 22, 97],
               [45, 26, 50, 39, 98], [59, 37, 26, 26, 51], [88, 92, 72, 32, 36], [46, 48, 39, 95, 42], [26, 29, 56, 72, 59]]


class Subsession(BaseSubsession):
    
    def creating_session(self):

        #loading treatments:
        if self.round_number == 1:
            treatment = itertools.cycle([3, 2, 1])
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

            print("[[ APP_1_ADDITION ]] - CREATING SESSION - PLAYER_ID ==> ", p.id_in_group, " <== ]]")
            print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.PAR.VAR.TREATMENT ==> ",  p.participant.vars['treatment'], " <== ]]")
            #print("[[ APP_1_ADDITION ]] - CREATING SESSION - P.TREATMENT ==> ",  p.treatment, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - ADDENDS  ==> ",  p.addend_1, p.addend_2, p.addend_3, p.addend_4, p.addend_5, " <== ]]")
        print("[[ APP_1_ADDITION ]] - CREATING SESSION - SOLUTION ==> ",  p.solution, " <== ]]")
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
    final_payoff = models.IntegerField()

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
        self.acc_payoff = sum([i * Constants.piece_rate for i in [p.was_correct for p in self.in_previous_rounds()]])
        #self.acc_payoff = sum([i * self.session.config['piece_rate'] for i in [p.was_correct for p in self.in_previous_rounds()]])

        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ WAS_CORRECT_LIST ==> ", [p.was_correct for p in self.in_previous_rounds()], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - COUNTING_PAST.............--------------------------------]")

    def final_count(self): # In the last round the function counting past is not working, leaving the last info not inputed in the lists so i have to run it but using in_all_rounds()

        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ROUND NUMBER ==> ", self.round_number, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ PLAYER_ID ==> ", self.id_in_group, " <== ]]]")

        self.acc_was_correct = sum(filter(None, [p.was_correct for p in self.in_all_rounds()]))
        self.acc_payoff = int(sum([i * Constants.piece_rate for i in [p.was_correct for p in self.in_all_rounds()] if i != None]))  # this creates a list multiplying every correct '1' times the piece rate and then adds it all

        if self.participant.vars['treatment'] == 1:
            self.final_payoff = int(self.acc_payoff)
        elif self.participant.vars['treatment'] == 2 or self.participant.vars['treatment'] == 3:
            self.final_payoff = int(self.acc_payoff * Constants.shock)
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ TREATMENT ==> ", self.participant.vars['treatment'], " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_WAS_CORRECT ==> ", self.acc_was_correct, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ ACC_PAYOFF ==> ", self.acc_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............[[[ FINAL_PAYOFF ==> ", self.final_payoff, " <== ]]]")
        print("[[ APP_1_ADDITION]] - PLAYER - FINAL_COUNT.............--------------------------------]")

    def report_addition(self):
        #self.participant.vars['treatment'] = self.participant.vars['treatment']
        self.participant.vars['addition_acc_was_correct'] = self.acc_was_correct
        self.participant.vars['addition_acc_payoff'] = self.acc_payoff
        self.participant.vars['addition_final_payoff'] = self.final_payoff
        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_ADDITION.............ROUND NUMBER", self.round_number)
        print("[[ APP_1_ADDITION ]] - PLAYER - REPORT_ADDITION.............PVARS ARE", self.participant.vars)
