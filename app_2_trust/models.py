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

        #loading treatments: #be sur to change this code to match tratments assigned in additions
        if self.round_number == 1:
            treatment = itertools.cycle([1, 2])
            for p in self.get_players():
                p.treatment = next(treatment) #this is just to keep it for the database. the code below is the useful one because thisone does not persist between rounds or apps
                p.participant.vars['treatment'] = p.treatment #this one is the one to use throught the entire code

        if self.round_number == 1:
            # SHUFFLER
            self.session.vars['full_data'] = [i for i in shifter(self.get_group_matrix())]

            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            metarole = itertools.cycle([True, False]) # The order of roles. True for sender first, False for receiver first
            for p in self.get_players():
                p.metarole = next(metarole)
                p.participant.vars['metarole'] = p.metarole
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
            print("[[ APP_2_TRUST ]] - CREATING SESSION - ###############################################################")


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

    def set_payoffs(self):
        #this code could be reduced if I use get_players() "Returns a list of all the groups in the subsession"
        for p in self.get_players():
            if self.round_number == 1:
                p1 = self.get_player_by_id(1)
                p2 = self.get_player_by_id(2)
            elif self.round_number == 2:
                p1 = self.get_player_by_id(2)
                p2 = self.get_player_by_id(1)

        # trust payoffs
        if p1.sent_amount == Constants.send_choices[0]:
            p1.t_temp_payoff = Constants.endowment
            p2.t_temp_payoff = Constants.endowment
        elif (p1.sent_amount == Constants.send_choices[1] and p2.sent_back_amount_if1 == True) or (p1.sent_amount == Constants.send_choices[2] and p2.sent_back_amount_if2 == True):
            p1.t_temp_payoff = int(((Constants.endowment - p1.sent_amount) + (p1.sent_amount * Constants.factor) + Constants.endowment) / 2)
            p2.t_temp_payoff = p1.t_temp_payoff
        elif (p1.sent_amount == Constants.send_choices[1] or  p1.sent_amount == Constants.send_choices[2]) and (p2.sent_back_amount_if1 == False or p2.sent_back_amount_if2 == False):
            p1.t_temp_payoff = Constants.endowment - p1.sent_amount
            p2.t_temp_payoff = Constants.endowment + (p1.sent_amount * 3)

        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - ROUND NUMBER ==> ", self.round_number, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P.METAROLE ==> ", p.participant.vars['metarole'], " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P1.T.TEMP.PAYOFF ==> ", self.get_player_by_id(1).t_temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - P2.T.TEMP.PAYOFF ==> ", self.get_player_by_id(2).t_temp_payoff, " <== ]]")
        print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (TRUST-TEMP) - ###############################################################")

        # BELIEFS
        # belief answers and markers (sender)
        if p2.sent_back_amount_if1 == p1.sender_belief_if1:
            p1.pay_sender_belief_if1 = True
        else:
            p1.pay_sender_belief_if1 = False
        if p2.sent_back_amount_if2 == p1.sender_belief_if2:
            p1.pay_sender_belief_if2 = True
        else:
            p1.pay_sender_belief_if2 = False
        if p2.participant.vars['treatment'] == p1.sender_belief_shock:
            p1.pay_sender_belief_shock = True
        else:
            p1.pay_sender_belief_shock = False

        # belief answers and markers (receiver)
        if p1.sent_amount == p2.receiver_belief:
            p2.pay_receiver_belief = True
        else:
            p2.pay_receiver_belief = False
        if p1.participant.vars['treatment'] == p2.receiver_belief_shock:
            p2.pay_receiver_belief_shock = True
        else:
            p2.pay_receiver_belief_shock = False

        if self.round_number == 1:
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - ROUND NUMBER ==> ", self.round_number, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_if1 ==> ", self.get_player_by_id(1).pay_sender_belief_if1, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_if2 ==> ", self.get_player_by_id(1).pay_sender_belief_if2, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_sender_belief_shock ==> ", self.get_player_by_id(1).pay_sender_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_receiver_belief ==> ", self.get_player_by_id(2).pay_receiver_belief, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - B.pay_receiver_belief_shock ==> ", self.get_player_by_id(2).pay_receiver_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS) - ###############################################################")
        elif self.round_number == 2:
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) ROUND NUMBER ==> ", self.round_number, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_if1 ==> ", self.get_player_by_id(2).pay_sender_belief_if1, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_if2 ==> ", self.get_player_by_id(2).pay_sender_belief_if2, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_sender_belief_shock ==> ", self.get_player_by_id(2).pay_sender_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_receiver_belief ==> ", self.get_player_by_id(1).pay_receiver_belief, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) B.pay_receiver_belief_shock ==> ", self.get_player_by_id(1).pay_receiver_belief_shock, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS) ###############################################################")

        # beliefs payoffs (temp):
        for p in self.get_players():
            p.b_temp_payoff = sum([0 if e is None else e for e in [p.pay_sender_belief_if1, p.pay_sender_belief_if2, p.pay_sender_belief_shock, p.pay_receiver_belief, p.pay_receiver_belief_shock]])
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS (BELIEFS-TEMP) - PLAYER_ID_INSUBSESSION ==> ", p.id_in_subsession, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS-TEMP) - P.B_TEMP_PAYOFF ==> ", p.b_temp_payoff, " <== ]]")
            print("[[ APP_2_TRUST ]] - GROUP/SET.PAYOFFS - (BELIEFS-TEMP) ###############################################################")


    def t_final_payoff(self):
        pass

#        print("[[ APP_2_TRUST ]] - GROUP/T_FINAL_PAYOFF (BELIEFS - TEMP) - P.T_FINAL_PAYOFF ==> ", p.t_final_payoff, " <== ]]")
#        print("[[ APP_2_TRUST ]] - GROUP/T_FINAL_PAYOFF (BELIEFS - TEMP) - P.B_FINAL_PAYOFF ==> ", p.b_final_payoff, " <== ]]")


    # Beliefs Payoffs
# save this code for posterity.  print("[[ APP_2_TRUST ]] - BBBBBB - GROUP.MATRIX R2 ==> ", self.get_players()[0].get_others_in_subsession(), " <== ]]",) #  get_others_in_subsession() is a player methodd. So it has to be called on a player object (get_players()[0] wich is a group method)
class Player(BasePlayer):

    treatment = models.IntegerField()
    metarole = models.BooleanField()

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

    t_temp_payoff = models.IntegerField() # payoff per round of trust
    t_final_payoff = models.IntegerField() # final payoff for trust

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
            (1, 'No Shock'),
            (2, 'Random Shock'),
            (3, 'Intentional Shock'),
        ],
    )

    pay_sender_belief_if1 = models.BooleanField()
    pay_sender_belief_if2 = models.BooleanField()
    pay_sender_belief_shock = models.BooleanField()

    receiver_belief = models.IntegerField(
        choices=[
            (0, '0'),
            (1, '1'),
            (2, '2'),
        ],
    )

    receiver_belief_shock = models.IntegerField(
        choices=[
            (1, 'No Shock'),
            (2, 'Random Shock'),
            (3, 'Intentional Shock'),
        ],
    )

    pay_receiver_belief = models.BooleanField()
    pay_receiver_belief_shock = models.BooleanField()

    b_temp_payoff = models.IntegerField() # payoff per round of belief
    b_final_payoff = models.IntegerField() # final payoff for belief
