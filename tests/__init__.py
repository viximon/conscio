import unittest

from approot import models, create_app, db


class BaseTest(unittest.TestCase):

    def __call__(self, result=None):
        self._pre_setup()
        super(BaseTest, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        self.app = create_app('test')
        self.client = self.app.test_client()
        print self.app.__dict__
        # now you can use flask thread locals
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()

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
        db.session.remove()
        db.drop_all()

    def assert200(self, response):
        self.assertTrue(response.status_code == 200)
