import os
# To generate a new secret key:
# >>> import random, string
# >>> "".join([random.choice(string.printable) for _ in range(24)])
# path for DB:
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Secret key:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@B$akYw,vd3t!aNKFc-*~V'
    # setup for DB:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
