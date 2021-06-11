import os
import unittest

from __init__ import app, db

#TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.app=app
        self.app.config['SECRET_KEY'] = 'myscecretkey12345'
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['DEBUG'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:manju123@localhost/f1'
        self.app = self.app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        self.app.run(host="192.168.0.13", debug=True)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()