from unittest import TestCase
from server import app
from model import connect_to_db

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""



        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'mypaleta'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1


    # ~=~=~=~=~=~=~=~CHANGE BEFORE TESTING DB =~=~=~=~=~=~=~=~=~=~=
        connect_to_db(app, 'postgresql:///paleta')
    # ~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~

    def test_homepage_route(self):
        """ Test homepage route rendering """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Welcome to Paleta', result.data)

    def test_gallery_route(self):
        """ Test gallery route rendering """

        result = self.client.get('/gallery')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<h2>Paleta Gallery</h2>', result.data)


    def test_profile_route(self):
        """ Test profile route rendering """

        result = self.client.get('/users/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Profile</h2>', result.data)

    def test_filter_route(self):
        """ Test profile route rendering """

        result = self.client.get('/image_filter')
        self.assertEqual(result.status_code, 200)
        self.assertIn('<p>Enter a hex color:', result.data)


    def test_login(self):
        result = self.client.post("/login",
                                  data={"email": "jahlela5@gmail.com", "password": "jahlela"},
                                  follow_redirects=True)
        self.assertIn("Successfully logged in!", result.data)


    def test_logout(self):
        result = self.client.get("/logout", follow_redirects=True)
        self.assertIn("Successfully logged out!", result.data)




if __name__ == "__main__":
    import unittest
    unittest.main()

