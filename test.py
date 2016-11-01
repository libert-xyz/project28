#import os
#import app
import main
from main import app, db
import sqlalchemy
#from app import db
import unittest
from models import User
from flask import url_for
from flask_login import current_user

#import tempfile
#from models import User


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    #Render login
    def test_loginPage(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        self.assertIn(b'Login', response.data)

    #login test

    def create_initial_user(self):
        u = User(email='admin@hoes.com',password='12345')
        db.session.add(u)
        db.session.commit()
        return u

    # def login(self,email,password):
    #     return self.app.post('/login', data=dict(
    #         email=email,
    #         password=password
    #     ), follow_redirects=True)

    # def test_login(self):
    #     rv = self.create_initial_user()
    #     #response = self.login('admin@root.com','sesamo')
    #     response = self.app.post('/login', data=dict(email=rv.email,password=rv.password),follow_redirects=True)
    #     #assert 'Welcome' in rv.data.
    #     self.assertIn(b'Welcome', response.data)

    #Test admin
    def test_users_can_login(self):
        #User.create(email='admin@joes.com', password='12345')
        u = User(name='admin')
        u.email='admin@joes.com'
        u.password_hash('sesamo')
        u.role = 'admin'
        db.session.add(u)
        db.session.commit()

        #tester = main.app.test_client(self)
        with self.app:
            response = self.app.post('/login',
                                        data={'email': 'admin@joes.com', 'password': 'sesamo'},
                                        follow_redirects=True)
            self.assertIn(b'Hi admin!', response.data)
            self.assertTrue(current_user.name == 'admin')
            self.assertFalse(current_user.is_anonymous)

    def test_admin_can_logout(self):

        u = User(name='admin')
        u.email='admin@joes.com'
        u.password_hash('sesamo')
        u.role = 'admin'
        db.session.add(u)
        db.session.commit()

        with self.app:
            response = self.app.post('/login',
                                        data={'email': 'admin@joes.com', 'password': 'sesamo'},
                                        follow_redirects=True)
            #self.assert_redirects(response, url_for('index'))
            self.app.get(url_for('logout'))
            self.assertTrue(current_user.is_anonymous)


    #Test admin page render

    # def test_admin_page(self):
    #
    #     rv = self.create_user()
    #     with self.login('admin@root.com','sesamo'):
    #         #rv = self.
    #         tester = main.app.test_client(self)
    #         #response = tester.get('/admin', content_type='html/text')
    #         response = tester.get('/admin')
    #         self.assertIn(b'Add Users', response.data)
    #
    #
    # def test_add_user(self):
    #     tester = main.app.test_client(self)
    #     response = tester.post('/add',data=dict
    #     (name='test',email='admin@root.com',password='sesamo',confirm='sesamo'),
    #     follow_redirects=True
    #     )
    #     self.assertIn(b'User Added', response.data)
    #
    #

    # def create_user(self):
    #     return self.app.post('/add',data=dict
    #     (name='test',email='admin@root.com',password='sesamo',confirm='sesamo'),
    #     follow_redirects=True)



    # # #Test edit user
    # def test_edit_user(self):
    #     tester = main.app.test_client(self)
    #     rv = self.create_user()
    #     response = tester.post('/user/edit/1',data=dict
    #     (name='testing',email='foo@bar.com'),
    #     follow_redirects=True
    #     )
    #     self.assertIn(b'User Edited', response.data)
    #
    # # #Test edit user
    # def test_delete_user(self):
    #     tester = main.app.test_client(self)
    #     rv = self.create_user()
    #     response = tester.post('/user/delete/1',data=dict
    #     (name='testing',email='foo@bar.com'),
    #     follow_redirects=True
    #     )
    #     self.assertIn(b'User Deleted', response.data)




if __name__ == '__main__':
    unittest.main()
