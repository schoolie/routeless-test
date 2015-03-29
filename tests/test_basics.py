import unittest
from flask import current_app
from routeless import create_app, db
from routeless.models import User
import json

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_create_user(self):
        data = {'username': 'Brian',
                'email': 'brian.p.schoolcraft@gmail.com',
                'password': 'Amanda09'}

        json_data = json.dumps(data)

        response = self.client.post('/api/user',
                                data=json_data,
                                headers={'content-type':'application/json'})

        json_data = json.loads(response.data)
        print json_data['password_hash']
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['password'], 'Amanda09')

    def test_create_course(self):

        u = User(username='Brian', email='brian@example.com', password='cat')
        db.session.add(u)
        db.session.commit()

        data = {'centerlat': 45.23,
                'centerlon': 54.12,
                'creator_id': u.id,
                'zoom': 12,
                'map_layer': 'satellite'}

        json_data = json.dumps(data)

        response = self.client.post('/api/course',
                                data=json_data,
                                headers={'content-type':'application/json'})
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_data['centerlon'], 54.12)
        self.assertEqual(json_data['creator']['username'], 'Brian')

        data = {'id':1}
        json_data = json.dumps(data)
        response = self.client.get('/api/course',
                        data=json_data,
                        headers={'content-type':'application/json'})
        # print response.data

