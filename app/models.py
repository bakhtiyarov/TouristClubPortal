from app import db
import bcrypt
from wand.image import Image, ImageProperty

ROLE_USER = 0
ROLE_LEADER = 1
ROLE_ADMIN = 2

STATUS_BANNED = 0
STATUS_READ_ONLY = 1
STATUS_OK = 2


class InvalidIdException(Exception):
	def __init__(self, id, tableName):
		self.invalidId = id
		self.table = tableName

	def __repr__(self):
		return "Exception 'invalid database id '%d' in table %r'!" % (self.invalidId, self.table)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(128), index=True)
	second_name = db.Column(db.String(128), index=True)
	patronymic = db.Column(db.String(128))
	email = db.Column(db.String(128), index=True, unique=True)
	role = db.Column(db.SmallInteger, default=ROLE_USER)
	password = db.Column(db.String(128))
	status = db.Column(db.SmallInteger, default=STATUS_READ_ONLY)
	passport_data = db.Column(db.String(32), db.ForeignKey('passport_data.id'))
	#resized to 320x240; original will be contain at basedir/avatars/md5(email).png
	avatar = db.Column(db.LargeBinary)

	def __init__(self, first_name, second_name, patronymic, e_mail, password, role, status):
		self.first_name = first_name
		self.second_name = second_name
		self.patronymic = patronymic
		self.email = e_mail
		self.role = role
		self.password = bcrypt.hashpw(password, bcrypt.gensalt())
		self.status = status

	def __repr__(self):
		if self.role == ROLE_USER:
			role = 'user'
		elif self.role == ROLE_ADMIN:
			role = 'admin'
		else:
			role = 'leader'
		return "User '%r' with e-mail <%r> and role %r" % (self.first_name, self.email, role)

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

	def in_one_group_with(self, other):
		raise NotImplementedError
		return False

	def load_avatar(self, picture):
		self.avatar = picture.make_blob()
		User.query.filter_by(email=self.email).update({'avatar' : self.avatar})
		db.session.commit()

class PassportData(db.Model):
	__tablename__ = 'passport_data'
	id = db.Column(db.Integer, primary_key=True)
	ser = db.Column(db.String(2))
	num = db.Column(db.String(32))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	#names and patronymics can differ from user table.
	first_name = db.Column(db.String(128))
	second_name = db.Column(db.String(128), index=True)
	patronymic = db.Column(db.String(128))

	birthday = db.Column(db.Date(), index=True)
	mobile_phone = db.Column(db.String(32))
	additional_phone = db.Column(db.String(32))
	work_phone = db.Column(db.String(32))
	home_phone = db.Column(db.String(32))
	second_email = db.Column(db.String(128))
	skype_account = db.Column(db.String(128))
	facebook_account = db.Column(db.String(128))
	vk_account = db.Column(db.String(128))
	issue_date = db.Column(db.Date())
	issuer = db.Column(db.String(128))
	release_date = db.Column(db.Date())
	address = db.Column(db.Text())
	work_place = db.Column(db.String(128))

	def __repr__(self):
		return "Passport data for user %r %r %r" % (self.first_name, self.patronymic, self.second_name)

	def __init__(self, user_id):
		self.user_id = user_id
		if User.query.get(user_id) is None:
			raise InvalidIdException(user_id, 'Passport')
		self.first_name = User.query.get(user_id).first_name
		self.second_name = User.query.get(user_id).second_name


class Hike(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	begin = db.Column(db.Date(), index=True)
	end = db.Column(db.Date())
	area = db.Column(db.String(128))
	category = db.Column(db.SmallInteger)
	route = db.Column(db.Text())
	max_altitude = db.Column(db.Integer())
	leader = db.Column(db.Integer(), db.ForeignKey('user.id'))
	route_document_num = db.Column(db.String(32), index=True)
	report_url = db.Column(db.Text())


class HikeMembership(db.Model):
	""" Link before user and hike - user can have many hikes and hike can have many users;"""

	__tablename__ = 'hike_membership'
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	hike_id = db.Column(db.Integer(), db.ForeignKey('hike.id'))
	is_active = db.Column(db.Boolean(), index=True)
	position = db.Column(db.String(128))


class Norm(db.Model):
	"""Represent results of physical norm delivering"""
	id = db.Column(db.Integer(), primary_key=True)
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
	date = db.Column(db.Date(), index=True)
	run = db.Column(db.DateTime())
	tightening = db.Column(db.SmallInteger())
	ups = db.Column(db.SmallInteger())
	press = db.Column(db.SmallInteger())
	squats_left = db.Column(db.SmallInteger())
	squats_right = db.Column(db.SmallInteger())

	def check_squats(self):
		return self.squats_left + self.squats_right >= 25

