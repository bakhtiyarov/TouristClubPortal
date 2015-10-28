#!/usr/bin/env bash

virtualenv venv -p /usr/bin/python3

venv/bin/pip install flask
venv/bin/pip install flask-login
venv/bin/pip install flask-mail
venv/bin/pip install flask-sqlalchemy
venv/bin/pip install sqlalchemy-migrate
venv/bin/pip install flask-whooshalchemy
venv/bin/pip install flask-wtf
venv/bin/pip install flask-babel
venv/bin/pip install guess_language
venv/bin/pip install flipflop
venv/bin/pip install coverage
venv/bin/pip install py-bcrypt
venv/bin/pip install wand