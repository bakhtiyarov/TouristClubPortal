from app import db
from flask_sqlalchemy import SQLAlchemy

ROLE_USER = 0
ROLE_LEADER = 1
ROLE_ADMIN = 2

STATUS_BANNED = 0
STATUS_READ_ONLY = 1
STATUS_OK = 2


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(128), index=True)
	email = db.Column(db.String(128), index=True, unique=True)
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	password = db.Column(db.String(128))
	status = db.Column(db.SmallInteger, default=STATUS_READ_ONLY)

	def __repr__(self):
		return "User '%r' with e-mail <%r> and role " % (self.nickname, self.email) + ("admin" if self.role == ROLE_ADMIN else "user")

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)