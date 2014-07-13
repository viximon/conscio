#!env/bin/python

import pprint
pp = pprint.PrettyPrinter(indent=4)

import os, sys
PROJECT_PATH = os.path.abspath('.')
sys.path.append(PROJECT_PATH)

from flask import current_app

from flask.ext.script import Manager
from flask.ext.script import Command, Option, Shell

from approot import models, create_app, db
#----------------------------------------------


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False, default='development')


@manager.command
def dump_config():
    pp.pprint(current_app.config)


@manager.command
def populate_demo_data():
    db.drop_all()
    db.create_all()
    u1 = models.User('demo', 'noone@nowhere.com')
    t1 = models.Task()
    t1.user = u1
    t1.name = 'Do CS101 assignment 7'
    t2 = models.Task()
    t2.user = u1
    t2.name = 'Update document'
    db.session.add(t1)
    db.session.add(t2)
    db.session.commit()


def _make_context():
    return dict(app=current_app, db=db, models=models)
manager.add_command('shell', Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
