from otree.api import *
import pandas as pd
import csv

doc = """
An interactive button
"""

class Messages(ExtraModel):
    participant_id = models.StringField()
    message = models.StringField()

class C(BaseConstants):
    NAME_IN_URL = 'Button'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    EARN_BEL = 2
    LOSS_BEL = 0

class Subsession(BaseSubsession):
    pass

def creating_session(subsession: Subsession):
   pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    choice = models.StringField(label="", blank=True)


# PAGES

class Button(Page):
    form_model = 'player'
    form_fields = ['choice']
    

  
    


page_sequence = [Button]
