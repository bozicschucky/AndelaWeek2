import unittest
import json
from apicore.app import app
from apicore.models.db import DBhandler


class APITestCase(unittest.TestCase):
    """Unit testing class for the API endpoints"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.db_handler = DBhandler(host="localhost", database="",
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
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

    def test_acces_endpoint_without_token(self):
        ''' Tests a user accesing  a protected endpoint without jwt '''
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn('Missing Authorization Header', str(res.data))

    def test_can_get_all_questions(self):
        '''Test can get a question with jwt auth '''
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

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
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

        login_response = response.json
        self.token = login_response['access_token']
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

    def test_can_get_a_question(self):
        '''Test can get a queston '''
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

        login_response = response.json
        self.token = login_response['access_token']
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        rv = self.client.get('api/v2/questions/1',
                             content_type='application/json',
                             headers={'Authorization':
                                      'Bearer {}'.format(self.token)})
        self.assertEqual(rv.status_code, 200)
        self.assertIn('I am getting errors when i run pytest', str(rv.data))

    def test_can_get_many_questions(self):
        '''Test can get many  questons '''
        question1 = {
            "author": "Tester",
            "title": "How do i work with JWT",
            "body": "I am writing unitests and they dont work \
                             i need a fix for this. Thanks"
        }

        question2 = {
            "author": "Tester",
            "title": "I am facing merge conflicts",
            "body": "How do i use version control and git \
                             to solve this. Thanks"
        }

        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered',
                      str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

        login_response = response.json
        self.token = login_response['access_token']
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        res = self.client.post('/api/v2/questions',
                               data=json.dumps(question1),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        res = self.client.post('/api/v2/questions',
                               data=json.dumps(question2),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        rv = self.client.get('api/v2/questions',
                             content_type='application/json',
                             headers={'Authorization':
                                      'Bearer {}'.format(self.token)})
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            'I am getting errors when i run pytest', str(rv.data))
        self.assertIn('How do i work with JWT', str(rv.data))
        self.assertIn('I am facing merge conflicts', str(rv.data))

    def test_can_create_answer_to_question(self):
        '''Test can create an answer to question '''
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered', str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

        login_response = response.json
        self.token = login_response['access_token']
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        answer = {"body": "Use windows because its cool",
                  'accept_status': False}
        res = self.client.post('/api/v2/questions/1/answers',
                               data=json.dumps(answer),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

    def test_delete_question(self):
        ''' Test can delete a question '''
        response = self.client.post('api/v2/auth/register',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('user is successfully registered',
                      str(response.data))

        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(self.user),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created', str(response.data))

        login_response = response.json
        self.token = login_response['access_token']
        res = self.client.post('/api/v2/questions',
                               data=json.dumps(self.question),
                               content_type='application/json',
                               headers={'Authorization':
                                        'Bearer {}'.format(self.token)})
        self.assertEqual(res.status_code, 201)

        rv = self.client.delete('api/v2/questions/1',
                                content_type='application/json',
                                headers={'Authorization':
                                         'Bearer {}'.format(self.token)})
        self.assertEqual(rv.status_code, 202)

    def tearDown(self):
        print('-----Tearing down ------------')
        self.db_handler.drop_table('users', 'answers', 'questions')


if __name__ == '__main__':
    unittest.main(verbosity=2)
