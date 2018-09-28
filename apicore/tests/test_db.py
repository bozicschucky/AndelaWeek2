import unittest
from apicore.models.db import DBhandler


class DBModelTestCase(unittest.TestCase):
    """Unit testing class for the API endpoints"""

    def setUp(self):
        self.db_handler = DBhandler(host="localhost", database="",
                                    user="postgres", password="sudo")
        self.db_handler.create_table()

    def test_register_user(self):
        '''Tests user Registeration to a given user to a database '''
        self.assertIn({'message': 'user is successfully registered'},
                      self.db_handler.register('chucky', 'password'))

    def test_get_user(self):
        '''Test user registeration and getting a registered user '''
        self.db_handler.register('charlse', 'password')
        self.assertEqual(2, len(self.db_handler.get_user('charlse')))

    def test_create_question(self):
        '''Test question creation  '''
        self.db_handler.register('charlse', 'password')
        question = self.db_handler.create_question('I need some help',
                                                   'How do i fix \
                                                    python imports', 'charlse')
        self.assertEqual(({'message': 'Question created'}, 201), question)

    def tearDown(self):
        print('-----Tearing down ------------')
        self.db_handler.drop_table('users', 'answers', 'questions')
