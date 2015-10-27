import os


CSRF_ENABLED = True
SECRET_KEY = 'klgjwrtosklmklsdngklsjnaldfjwiout4ruowerjdf'


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

#TODO: migrate to PostgreSQL
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True