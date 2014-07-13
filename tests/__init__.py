from flask.ext.testing import TestCase

from approot import models, create_app, db


class BaseTest(TestCase):
    def create_app(self):
        app = create_app('test')
        return app

    def init_data(self):
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

    def setUp(self):
        """ Reset tables """
        db.create_all()
        self.init_data()

    def tearDown(self):
        """ Clean db sesion and drop tables """
        db.drop_all()
