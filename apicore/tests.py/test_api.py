import unittest
import json
from coreapi.app import app
from apicore.models.db import DBhandler


class APITestCase(unittest.TestCase):
    """Unit testing class for the API"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client
        self.mock_data = {
            "_id": 1,
            "question_title": "How do i work with python",
            "question_body": "I am facing bug x"
        }

    def test_can_get_one_question(self):
        res = self.client().post('/api/v2/questions',
                                 data=json.dumps(self.mock_data),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 201)
        response = self.client().get('/api/v2/questions/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('How do i work with python', str(response.data))
        # self.db_handler = DBhandler('')

    def TearDown(self):
        pass
