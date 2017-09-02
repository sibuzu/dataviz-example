# api/settings.py

URL_PREFIX = 'api'
MONGO_DBNAME = 'nobel_prize'
DOMAIN = {'winners': {
    'schema': {
        'country': {'type': 'string'},
        'catagory': {'type': 'string'},
        'name': {'type': 'string'},
        'year': {'type': 'integer'},
        'gender': {'type': 'string'},
    }
}}

X_DOMAINS = 'http://localhost:8080'
