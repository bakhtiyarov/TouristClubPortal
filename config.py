import os


CSRF_ENABLED = True
SECRET_KEY = 'klgjwrtosklmklsdngklsjnaldfjwiout4ruowerjdf'


basedir = os.path.abspath(os.path.dirname(__file__))

available_db = {'postgresql' : 'postgresql://',
				'sqlite' : 'sqlite:///'}

DB_USERNAME = 'mtc'
DBL_PASSWORD = 'MSU_MTC'
DB_HOST = 'localhost'
DB_NAME = 'touristicClub'

SQLALCHEMY_DATABASE_URI = available_db['postgresql'] + DB_USERNAME + ':' + DBL_PASSWORD + '@' + DB_HOST + '/' + DB_NAME
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True