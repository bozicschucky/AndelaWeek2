from flask_restplus import Resource, fields
from .app import api


question = api.model('Question', {
    'author': fields.String(description='Author name', required=True, min_length=5),
    'title': fields.String(required=True,
                           description='The question title', min_length=10),

    'body': fields.String(required=True,
                          description='The question details', min_length=10)
})

answer = api.model('Answer', {
    'body': fields.String(required=True,
                          description='The Answer details', min_length=10)
})


@api.route('/auth/register')
class register(Resource):
    """Get username and password and register them"""

    def post(self):
        """ Register a User"""
        return {'message': 'user is registered'}, 201


@api.route('/auth/login')
class login(Resource):
    """Login a user and return a token"""

    def post(self):
        """ Login a user and return a token"""
        return {'message': 'Invalid username and password'}, 400


@api.route('/questions')
class AllQuestions(Resource):
    """Get and create questions as specified"""

    def get(self):
        """Get all questions asked """
        return {'questions': 'all questions'}

    def post(self):
        """Creates a question """
        return {'questions': 'created'}


@api.route('/questions/<int:_id>')
class Question(Resource):
    """Shows single items of the resources created"""

    def get(self, _id):
        ''' Get a given resource/question based on id '''
        return {'message': 'question given an id'}

    def delete(self, _id):
        '''Delete a certain resource/question given an id'''
        return {'message': 'question {} deleted'.format(_id)}, 204


@api.route('/questions/<int:_id>/answers')
class QuestionsReply(Resource):
    def post(self, _id):
        return {'message': 'answer created for  question {}'.format(_id)}, 201


@api.errorhandler
def server_error_handler(error):
    '''Default error handler for 500 errors'''
    return {'message': str(error)}, getattr(error, 'code', 500)
