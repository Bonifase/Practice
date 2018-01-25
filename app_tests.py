import os
import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.user

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
    #test home page
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far'

    def login(self, username, password):
        return self.app.post('/login', data=dict(username=username,password=password), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
    #test login and logout fuctionalities works
    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in'
        rv = self.logout()
        assert 'You were logged out'
        rv = self.login('adminx', 'default')
        assert 'Invalid username' 
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' 
    #test  add list functionalities work
    def test_lists(self):
        self.login('admin', 'default')
        rv = self.app.post('/add_list', data=dict(
        id='<value>', title='<anything>', qnty='<anything>', date='<value>'), follow_redirects=True)
        assert 'value' 
        assert '&lt;anything&gt;' 
        assert 'anything'
        assert 'value'
if __name__ == '__main__':
    unittest.main()