import unittest
import json
from coreapi.app import app
from apicore.models.db import DBhandler


class APITestCase(unittest.TestCase):
    """Unit testing class for the API"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.db_handler = DBhandler('')

    def TearDown(self):
        pass
