from otree.api import *

# Constants for the PGG experiment (using new grammar: C for constants, UPPERCASE names)
class C(BaseConstants):
    NAME_IN_URL = 'PGG'  # App name for URL
    PLAYERS_PER_GROUP = 3  # Number of players per group
    NUM_ROUNDS = 4  # Number of rounds
    ENDOWMENT = cu(100)  # Each player's initial endowment
    MULTIPLIER = 2  # Multiplier for the public good

# Subsession class: represents a round of the experiment
class Subsession(BaseSubsession):
    pass

# Group class: stores group-level variables for each round
class Group(BaseGroup):
    total_choices = models.CurrencyField()  # Total contributions in the group
    individual_share = models.CurrencyField()  # Each player's share from the public good
    total_earnings = models.CurrencyField()  # Total earnings from the public good

# Player class: stores player-level variables for each round
class Player(BasePlayer):
    choice = models.CurrencyField(min=0, max=C.ENDOWMENT)  # Player's contribution
    payoff_final = models.CurrencyField()  # Sum of payoffs across all rounds

# FUNCTIONS
# Group players randomly in round 1, keep same groups in later rounds
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        subsession.group_randomly()
    else:
        subsession.group_like_round(1)

# Calculate payoffs for each group after all have contributed
def set_payoffs(group: Group):
    players = group.get_players()
    choices = [p.choice for p in players]  # List of all contributions
    print(choices)
    group.total_choices = sum(choices)  # Total group contribution
    group.total_earnings = group.total_choices * C.MULTIPLIER  # Public good total
    group.individual_share = group.total_earnings / C.PLAYERS_PER_GROUP  # Each player's share
    for p in players:
        # Each player's payoff: what they kept + their share from the public good
        p.payoff = C.ENDOWMENT - p.choice + group.individual_share
    # At the last round, sum up all payoffs for final result
    if group.round_number == C.NUM_ROUNDS:
        for p in players:
            hist = p.in_all_rounds()
            p.payoff_final = sum([g.payoff for g in hist])

# PAGES
# Instructions page: only shown in round 1
class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'common_proj': C.ENDOWMENT * C.PLAYERS_PER_GROUP,  # Total possible group endowment
        }

# Contribution page: player chooses how much to contribute
class Contribute(Page):
    form_model = 'player'
    form_fields = ['choice']
    @staticmethod
    def vars_for_template(player: Player):
        return {
            'round_number': player.round_number,
            'endowment': C.ENDOWMENT,
        }

# Wait page: waits for all players to contribute, then calculates payoffs
class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)

# Results page: shows outcome for the current round and history
class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        hist = player.in_all_rounds()  # All rounds for this player
        # Safely get group-level attributes for each round
        history_contrib = [getattr(g.group, 'total_choices', 0) for g in hist]
        # If you use a graph, you may need to import safe_json or use json.dumps
        try:
            from otree.api import safe_json
            history_contrib_json = safe_json(history_contrib)
        except ImportError:
            import json
            history_contrib_json = json.dumps(history_contrib)
        data_hist = [
            [g.choice for g in hist],  # Player's contributions
            [getattr(g.group, 'individual_share', 0) for g in hist],  # Player's share from public good
            [g.payoff for g in hist]  # Player's payoff
        ]
        print(data_hist)
        table_hist = []
        for j in range(0, player.round_number):
            t = [j+1]  # Round number
            for i in data_hist:
                t.append(i[j])
            table_hist.append(t)
        amount_kept = C.ENDOWMENT - player.choice  # What player kept this round
        return {
            'history_contrib': history_contrib_json,
            'round_number': player.round_number,
            'kept': amount_kept,
            'table_hist': table_hist
        }

# Final results page: only shown in last round
class FinalResults(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        return {'payoff_final': player.payoff_final}

# Sequence of pages in the experiment
page_sequence = [Instructions, Contribute, ResultsWaitPage, Results, FinalResults]
