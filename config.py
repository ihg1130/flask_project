import os

BASE_DIR = os.path.dirname(__file__)


SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"


# CLIENT_ID = "6925e2e950e402e6d1d144af81ee1292"
# CLIENT_SECRET = "MGFMXFDJnsuFW4c8azm0dXXkX1N93H3w"
# REDIRECT_URI = "http://localhost:5000"
# SIGNOUT_REDIRECT_URI = "http://localhost:5000/logout"

