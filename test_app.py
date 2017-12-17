import os
import unittest
import app
from app import user

class AppTestCase(unittest.TestCase):

    def test_login(self):
        tester = app.login()
        response = tester.post('/login', { username: 'Bonifase', password_cadidate: 'qwerty' })
        self.assertEquals(session.username, 'Bonifase')


if __name__ == '__main__':
    unittest.main()
