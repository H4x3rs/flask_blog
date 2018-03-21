from .db import db

users_roles = db.Table(
	'users_roles',
	db.Column('user_id',db.String(50),db.ForeignKey('users.id')),
	db.Column('role_id',db.String(50),db.ForeignKey('roles.id'))
)
