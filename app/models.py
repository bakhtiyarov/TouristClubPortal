from app import db
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from wand.image import Image, ImageProperty

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
	#resized to 320x240; original will be contain at basedir/avatars/md5(email).png
	avatar = db.Column(db.LargeBinary)

	def __init__(self, username, e_mail, password, role, status):
		self.nickname = username
		self.email = e_mail
		self.role = role
		self.password = bcrypt.hashpw(password, bcrypt.gensalt())
		self.status = status


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

	def load_avatar(self, picture):
		img = Image()
		avatar = picture
		User.query.filter_by(email=self.email).update({'avatar' : self.avatar})
		db.session.commit()
