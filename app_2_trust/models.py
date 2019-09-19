from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools, random


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'app_2_trust'
    players_per_group = 2
    num_rounds = 2

    endowment = 2
    factor = 3

    send_choices = [0, 1, 2]
    #send_back_choices = [x*3 for x in send_choices]

def shifter(m): # https://groups.google.com/forum/#!searchin/otree/perfect$20stranger|sort:date/otree/rciCzbTqSfQ/Sbl2-3KqAQAJ
    group_size_err_msg = 'This code will not correctly work for group size not equal 2'
    assert Constants.players_per_group == 2, group_size_err_msg
    m = [[i.id_in_subsession for i in l] for l in m]
    f_items = [i[0] for i in m]
    s_items = [i[1] for i in m]
    for i in range(Constants.num_rounds):
        yield [[i, j] for i, j in zip(f_items, s_items)]
        s_items = [s_items[-1]] + s_items[:-1]


class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            # SHUFFLER
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]

            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            metarole = itertools.cycle([True, False]) # The order of roles. True for sender first, False for receiver first
            #metaround = itertools.cycle([True, False])# The round to be payed. True for first round, False for second.
            for p in self.get_players():
                p.metarole = next(metarole)
                p.participant.vars['metarole'] = p.metarole
#            for g in self.get_groups():
#                g.metaround = next(metaround)
#        elif self.round_number == 2:
#            self.group_randomly(fixed_id_in_group = True)
        #SHUFFLER
        fd = self.session.vars['full_data']
        self.set_group_matrix(fd[self.round_number - 1])

        print("[[ APP_2_TRUST ]] - CREATING SESSION - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_2_TRUST ]] - CREATING SESSION - GROUP.MATRIX ==> ", self.get_group_matrix(), " <== ]]")
        print("[[ APP_2_TRUST ]] - CREATING SESSION - PAYING_ROUND ==> ", self.session.vars['paying_round'], " <== ]]")
        for p in self.get_players():
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PLAYER_ID_INGROUP ==> ", p.id_in_group, " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
            #print("[[ APP_2_TRUST ]] - CREATING SESSION - METAROLE ==> ", p.metarole, " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - PVARS.METAROLE ==> ", p.participant.vars['metarole'], " <== ]]")
            #print("[[ APP_2_TRUST ]] - CREATING SESSION - METAROUND ==> ", g.metaround, " <== ]]")
            print("[[ APP_2_TRUST ]] - CREATING SESSION - ###############################################################")

#    def set_groups_as_r1(self):
#        self.group_like_round(1)
#        print("[[ APP_2_TRUST ]] - CREATING SESSION - UNDO_SHUFFLE - GROUP.MATRIX R1 ==> ", self.get_group_matrix(), " <== ]]")
#        print("[[ APP_2_TRUST ]] - CREATING SESSION - ###############################################################")
#
#    def set_groups_as_r2(self):
#        self.group_like_round(2)
#        print("[[ APP_2_TRUST ]] - CREATING SESSION - UNDO_SHUFFLE - GROUP.MATRIX R2 ==> ", self.get_group_matrix(), " <== ]]")
#        print("[[ APP_2_TRUST ]] - CREATING SESSION - ###############################################################")


class Group(BaseGroup):

    #Group Shifter
    def shifter(m):
        group_size_err_msg = 'This code will not correctly work for group size not equal 2'
        assert Constants.players_per_group == 2, group_size_err_msg
        m = [[i.id_in_subsession for i in l] for l in m]
        f_items = [i[0] for i in m]
        s_items = [i[1] for i in m]
        for i in range(Constants.num_rounds):
            yield [[i, j] for i, j in zip(f_items, s_items)]
            s_items = [s_items[-1]] + s_items[:-1]

    #Trust Payoffs
    def set_payoffs(self):
        for p in self.get_players():
            if self.round_number == 1:
                p1 = self.get_player_by_id(1)
                p2 = self.get_player_by_id(2)
            elif self.round_number == 2:
                p1 = self.get_player_by_id(2)
                p2 = self.get_player_by_id(1)
        if p1.sent_amount == Constants.send_choices[0]:
            p1.temp_payoff = Constants.endowment
            p2.temp_payoff = Constants.endowment
        elif (p1.sent_amount == Constants.send_choices[1] and p2.sent_back_amount_if1 == True) or (p1.sent_amount == Constants.send_choices[2] and p2.sent_back_amount_if2 == True):
            p1.temp_payoff = int(((Constants.endowment - p1.sent_amount) + (p1.sent_amount * Constants.factor) + Constants.endowment) / 2)
            p2.temp_payoff = p1.temp_payoff
        elif (p1.sent_amount == Constants.send_choices[1] or  p1.sent_amount == Constants.send_choices[2]) and (p2.sent_back_amount_if1 == False or p2.sent_back_amount_if2 == False):
            p1.temp_payoff = Constants.endowment - p1.sent_amount
            p2.temp_payoff = Constants.endowment + (p1.sent_amount * 3)

        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - P1.TEMP.PAYOFF ==> ", self.get_player_by_id(1).temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - P2.TEMP.PAYOFF ==> ", self.get_player_by_id(2).temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - ###############################################################")

    def trust_final_payoff(self):
        print("[[ APP_2_TRUST ]] - GROUP/TRUST_FINAL_PAYOFF - ROUND_NUMBER ==> ", self.round_number, " <== ]]")
        for p in self.get_players():
            p.trust_final_payoff = p.in_round(self.session.vars['paying_round']).temp_payoff

        print("[[ APP_2_TRUST ]] - GROUP/TRUST_FINAL_PAYOFF - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/TRUST_FINAL_PAYOFF - P1.TRUST_FINAL_PAYOFF ==> ", p.trust_final_payoff, " <== ]]")
    print("[[ APP_2_TRUST ]] - GROUP/TRUST_FINAL_PAYOFF - ###############################################################")

####    # Beliefs Payoffs
####    def set_payoff_belief(self): # Here I wanted to shuffle groups as they where in previous rounds to get their places and execute that commented out code below.
####        #it didnt work because the print showd e the same group matrix as in round one even when asking to use it as in round 2
####        #
#####        self.subsession.set_groups_as_r1()
####        self.set_groups_as_r1()
####        print("[[ APP_2_TRUST ]] - GROUP/ GROUP.MATRIX_AS_IN_ROUND_1 ==> ", self.subsession.get_group_matrix()," <== ]]")
#####        for p in self.get_players():
#####            p1 = self.get_player_by_id(1)
#####            p2 = self.get_player_by_id(2)
#####        self.subsession.set_groups_as_r2()
####        self.set_groups_as_r1()
####        print("[[ APP_2_TRUST ]] - GROUP/ GROUP.MATRIX_AS_IN_ROUND_2 ==> ", self.subsession.get_group_matrix()," <== ]]")
####
####    def set_groups_as_r1(self):
####        self.subsession.group_like_round(1)
####        print("[[ APP_2_TRUST ]] - UNDO_SHUFFLE - GROUP.MATRIX R1 ==> ", self.subsession.get_group_matrix(), " <== ]]")
####        print("[[ APP_2_TRUST ]] - UNDO_SHUFFLE - ###############################################################")
####
####    def set_groups_as_r2(self):
####        self.subsession.group_like_round(2)
####        print("[[ APP_2_TRUST ]] - UNDO_SHUFFLE - GROUP.MATRIX R2 ==> ", self.subsession.get_group_matrix(), " <== ]]")
####        print("[[ APP_2_TRUST ]] - UNDO_SHUFFLE - ###############################################################")


class Player(BasePlayer):

    metarole = models.BooleanField()
    temp_payoff = models.IntegerField() # payoff per round of trust
    trust_final_payoff = models.IntegerField() # final payoff for trust

    sent_amount = models.IntegerField(
        choices = Constants.send_choices
    )

    sent_back_amount_if1 = models.BooleanField(
        choices=[
            (False, 'No reciprocar'),
            (True, 'Reciprocar'),
        ],
    )

    sent_back_amount_if2 = models.BooleanField(
        choices=[
            (False, 'No reciprocar'),
            (True, 'Reciprocar'),
        ],
    )

    #beliefs
    sender_belief_if1 = models.BooleanField(
        choices=[
            (False, 'No Reciprocó'),
            (True, 'Si Reciprocó'),
        ],
    )

    sender_belief_if2 = models.BooleanField(
        choices=[
            (False, 'No Reciprocó'),
            (True, 'Si Reciprocó'),
        ],
    )

    sender_belief_shock = models.IntegerField(
        choices=[
            (0, 'No Shock'),
            (1, 'Random Shock'),
            (2, 'Intentional Shock'),
        ],
    )

    receiver_belief = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
        ],
    )

    receiver_belief_shock = models.IntegerField(
        choices=[
            (0, 'No Shock'),
            (1, 'Random Shock'),
            (2, 'Intentional Shock'),
        ],
    )


