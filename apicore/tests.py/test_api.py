import unittest
import json
from coreapi.app import app


class APITestCase(unittest.TestCase):
    """Unit testing class for the API"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client

    def TearDown(self):
        pass
