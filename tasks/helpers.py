import sqlalchemy
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:abcd1234@localhost/comic?charset=utf8'


def db_connect():
    """Connects to the database and return a session"""

    uri = SQLALCHEMY_DATABASE_URI

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(uri)

    # create a Session
    Session = sessionmaker(bind=con)
    session = Session()

    return con, session
