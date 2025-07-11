from os import environ


SESSION_CONFIGS = [
    dict(name='inputs',
         display_name="Inputs",
         app_sequence=['inputs'],
         num_demo_participants=1,
         ),
    dict(name='MPL',
         display_name="MPL",
         app_sequence=['MPL'],
         num_demo_participants=1,
         ),
    dict(name='group_roles',
         display_name="Group Roles",
         app_sequence=['groups_roles'],
         num_demo_participants=4,
         ),
    dict(name='PGG',
         display_name="Public Goods Game",
         app_sequence=['PGG'],
         num_demo_participants=3,
         )

    # dict(
    #     name='MPL',
    #     display_name="MPL",
    #     app_sequence=['MPL'],
    #     num_demo_participants=1,
    # ),
    #     dict(
    #     name='group_roles',
    #     display_name="group_roles",
    #     app_sequence=['groups_roles'],
    #     num_demo_participants=10,
    # ),
    #         dict(
    #     name='PGG',
    #     display_name="PGG",
    #     app_sequence=['PGG'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4301659428929'

INSTALLED_APPS = ['otree']
