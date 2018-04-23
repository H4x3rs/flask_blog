#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/31 23:57

from app import app

from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

from app.models.db import db
from app.models.users import Users
from app.models.users_roles import users_roles
from app.models.posts import Posts
from app.models.posts_tags import posts_tags
from app.models.comments import Comments
from app.models.tags import Tags
from app.models.roles import Roles

# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object 
migrate = Migrate(app, db)

# Create new Command
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app,
	db=db,
	User=Users,
	Post=Posts,
	Comment=Comments,
	Tag=Tags,
	Role = Roles,
	posts_tags=posts_tags,
	users_roles=users_roles)


if __name__ == '__main__':
    manager.run()
