#! /env python
# _*_ coding:utf8 _*_
# @author:Ren
# @time:2017/8/31 23:57

from flaskblog import app

from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

from flaskblog.models import db
from flaskblog.models.users import Users
from flaskblog.models.posts import Posts
from flaskblog.models.posts_tags import posts_tags
from flaskblog.models.comments import Comments
from flaskblog.models.tags import Tags

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
	posts_tags=posts_tags)


if __name__ == '__main__':
    manager.run()
