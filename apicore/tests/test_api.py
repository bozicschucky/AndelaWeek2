import unittest
import json
from apicore.app import app
from apicore.models.db import DBhandler


class APITestCase(unittest.TestCase):
    """Unit testing class for the API"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.db_handler = DBhandler(host="localhost", database="api_test",
                                    user="postgres", password="sudo")
        self.db_handler.create_table()
        self.client = self.app.test_client()
        self.user = {
            'username': 'tester',
            'password': 'password'
        }
        self.question = {
            "author": "Tester",
            "title": "I am getting errors when i run pytest",
            "body": "I am having issues with the code i \
                            have written i need a fix for this"
        }
        self.token = ''

    def test_user_register(self):
        ''' Tests whether a given user can register through the app '''
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

    def test_user_login(self):
        ''' Tests whether a given user can register through the app '''
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

    def test_can_get_all_questions(self):
        '''Test can get a question with jwt auth '''
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))
        login_response = response.json
        self.token = login_response['access_token']
        rv = self.client.get('api/v2/questions',
                             content_type='application/json',
                             headers={'Authorization':
                                      'Bearer {}'.format(self.token)})
        self.assertEqual(rv.status_code, 200)

    def test_can_create_a_question(self):
        '''Test can create a queston '''
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_get_a_question(self):
        '''Test can create a queston  using a question id'''
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        response = self.client.get('/api/v2/questions/36')
        self.assertEqual(response.status_code, 200)
        self.assertIn('I am getting errors when i run pytest',
                      str(response.data))

    def tearDown(self):
        print('-----Tearing down ------------')
        self.db_handler.drop_table('users', 'answers', 'questions')
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
