import random
from otree.api import *

# Author and description
author = 'MP'
doc = """
MPL risk elicitation à la Holt&Laury
"""

# Constants for the experiment (payoffs, app name, etc.)
class C(BaseConstants):
    NAME_IN_URL = 'MPL'  # App name for URL
    PLAYERS_PER_GROUP = None  # No grouping
    NUM_ROUNDS = 1  # Single round
    # Payoff values for lotteries A and B
    A_h = 2.00  # Lottery A high payoff
    A_l = 1.60  # Lottery A low payoff
    B_h = 3.85  # Lottery B high payoff
    B_l = 0.10  # Lottery B low payoff

# Group class: used for grouping players (not used in this app, but required by oTree)
class Group(BaseGroup):
    pass

# Subsession class: represents a round of the experiment (not used here, but required by oTree)
class Subsession(BaseSubsession):
    pass

class Player(BasePlayer):
    # 10 main choices for the MPL table (A or B)
    HL_1 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_2 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_3 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_4 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_5 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_6 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_7 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_8 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_9 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    HL_10 = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal)
    # Demo choice for instructions
    HL = models.CharField(choices=['A', 'B'], widget=widgets.RadioSelectHorizontal, blank=True)

    # Questionnaire fields (demographics and feedback)
    sex = models.StringField(widget=widgets.RadioSelectHorizontal(), choices=['Male', 'Female', 'Other'])
    age = models.IntegerField(choices=range(18, 60, 1))
    comment = models.TextField(label="Your comment here:")
    like = models.IntegerField(choices=[1, 2, 3, 4, 5], widget=widgets.RadioSelectHorizontal)

    # Variables for payoff calculation
    row = models.IntegerField()  # Randomly selected row for payment
    drawn = models.IntegerField()  # Random draw for outcome
    choice = models.CharField()  # Player's choice in selected row

# Compute payoff for a player based on random row and outcome
def set_payoff_HL(player: Player):
    # Randomly select a row (1-10) for payment
    player.row = random.randint(1, 10)
    # Randomly select a draw (1-10) to determine outcome
    player.drawn = random.randint(1, 10)
    # Get the player's choice (A or B) for the selected row
    choices = [player.HL_1, player.HL_2, player.HL_3, player.HL_4, player.HL_5,
               player.HL_6, player.HL_7, player.HL_8, player.HL_9, player.HL_10]
    player.choice = choices[player.row - 1]
    # Assign payoff based on choice and draw: if drawn <= row, use high payoff; else, low payoff
    if player.drawn <= player.row:
        player.payoff = float(C.A_h) if player.choice == "A" else float(C.B_h)
    else:
        player.payoff = float(C.A_l) if player.choice == "A" else float(C.B_l)
    print(player.payoff)

# Instruction page with demo MPL
class Instructions(Page):
    form_model = 'player'
    form_fields = ['HL']  # Demo choice for instructions

# Main MPL choice page (10 rows)
class PageHL(Page):
    form_model = 'player'
    form_fields = [
        'HL_1', 'HL_2', 'HL_3', 'HL_4', 'HL_5',
        'HL_6', 'HL_7', 'HL_8', 'HL_9', 'HL_10',
    ]  # All 10 choices
    @staticmethod
    def vars_for_template(player: Player):
        # Pass payoff values to template for display
        return {'A_h': C.A_h, 'A_l': C.A_l, 'B_h': C.B_h, 'B_l': C.B_l}
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoff_HL(player)  # Compute payoff after choices

# Alternative MPL page with table display
class PageHL_2(Page):
    form_model = 'player'
    form_fields = [
        'HL_1', 'HL_2', 'HL_3', 'HL_4', 'HL_5',
        'HL_6', 'HL_7', 'HL_8', 'HL_9', 'HL_10'
    ]
    @staticmethod
    def vars_for_template(player: Player):
        # Build a table of lottery options for display in the template.
        # Each row in the table represents one decision (out of 10),
        # and contains the details for lottery A, lottery B, and the field name for the choice input.
        lottery_table = []
        
        for i in range(1, 11):
            # Define the structure for lottery A in this row
            lottery_a = {
                'prob_high': i,  # Probability (out of 10) of high payoff
                'prob_low': 10 - i,  # Probability (out of 10) of low payoff
                'payoff_high': C.A_h,  # High payoff amount for A
                'payoff_low': C.A_l,   # Low payoff amount for A
                'description': f"{i}/10 chance of €{C.A_h}, {10-i}/10 chance of €{C.A_l}"
            }
            
            # Define the structure for lottery B in this row
            lottery_b = {
                'prob_high': i,  # Probability (out of 10) of high payoff
                'prob_low': 10 - i,  # Probability (out of 10) of low payoff
                'payoff_high': C.B_h,  # High payoff amount for B
                'payoff_low': C.B_l,   # Low payoff amount for B
                'description': f"{i}/10 chance of €{C.B_h}, {10-i}/10 chance of €{C.B_l}"
            }
            
            # Append the row to the table, including the field name for the choice input (e.g., HL_1, HL_2, ...)
            lottery_table.append({
                'row_number': i,
                'lottery_a': lottery_a,
                'lottery_b': lottery_b,
                'choice_field': f'HL_{i}'  # Field name for this row's choice
            })
        
        # Return the table and constants for use in the template
        return {
            'lottery_table': lottery_table,  # List of all rows for the table
            'A_h': C.A_h, 
            'A_l': C.A_l, 
            'B_h': C.B_h, 
            'B_l': C.B_l
        }
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        set_payoff_HL(player)

# Outcome page: shows the randomly selected row, draw, and payoff
class OutcomeHL(Page):
    @staticmethod
    def vars_for_template(player: Player):
        # Prepare outcome details for the results template:
        # - row: which row was randomly selected for payment
        # - value: the random draw that determines which outcome is paid
        # - choice: player's choice (A or B) in the selected row
        # - p_A_1, p_A_2, p_B_1, p_B_2: used for displaying lottery probabilities
        return {
            'row': player.row,  # Randomly chosen row
            'value': player.drawn,  # Randomly chosen value
            'choice': player.choice,  # Player's choice
            'p_A_1': player.row,
            'p_A_2': 10 - player.row,
            'p_B_1': player.row,
            'p_B_2': 10 - player.row
        }

# Page sequence for the experiment
page_sequence = [Instructions, PageHL_2, OutcomeHL]
