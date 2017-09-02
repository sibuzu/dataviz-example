# api/settings.py

URL_PREFIX = 'api'
MONGO_DBNAME = 'nobel_prize'

DOMAIN = {'winners_all': {
    'item_title': 'winners',
    'schema': {
        'country': {'type': 'string'},
        'catagory': {'type': 'string'},
        'name': {'type': 'string'},
        'year': {'type': 'integer'},
        'gender': {'type': 'string'},
        'mini_bio': {'type': 'string'},
        'bio_image': {'type': 'string'}
    },
    'url': 'winners'
}}

X_DOMAINS = '*'
HATEOAS = False
PAGINATION = False
