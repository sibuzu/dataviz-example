

from sqlalchemy import create_engine

engine = create_engine('sqlite:///data/nobel_prize.db', echo=True)
