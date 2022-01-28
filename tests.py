import unittest

from server import app
from model import db, connect_to_db


class ServerTestsLogin(unittest.TestCase):
    """tests for my restroom finding site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"search for a restroom", result.data)

    def test_user_profile(self):
        result = self.client.get("/user")
        self.assertIn(b"Comments", result.data)

    def test_bowlmates(self):
        result = self.client.get("/bowlmates")
        self.assertIn(b"Welcome", result.data)
   


class ServerTestsLogout(unittest.TestCase):
    """tests for my restroom finding site"""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn(b"search for a restroom", result.data)

    def test_login_page(self):
        result = self.client.get("/login")
        self.assertIn(b"Create an", result.data)





if __name__ == "__main__":
    unittest.main()
    