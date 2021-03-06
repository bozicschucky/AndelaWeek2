import os
from flask_restplus import Resource, fields
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)
from .app import api
from apicore.models.db import DBhandler

if os.getenv('APP_SETTINGS') == 'testing':
    db_handler = DBhandler(host='localhost', database='',
                           user='postgres', password='sudo')
else:
    db = os.getenv('Database')
    db_handler = DBhandler(host=os.getenv('host'), database='',
                           user=os.getenv('User'),
                           password=os.getenv('Password'))
# db_handler.create_table()
# db_handler.drop_table('users', 'answers', 'questions')

question = api.model('Question', {
    'title': fields.String(required=True,
                           description='The question title', min_length=10),

    'body': fields.String(required=True,
                          description='The question details', min_length=10)
})

answer = api.model('Answer', {
    'body': fields.String(description='The Answer details', min_length=10),
    'accept_status': fields.Boolean(description='The Answer accept status',
                                    default=False)
})


user = api.model('User', {
    'username': fields.String(required=True,
                              description='username', min_length=6),
    'password': fields.String(required=True,
                              description='password', min_length=8)
})

jwt = {'Authorization': {'Authorization Bearer': 'Bearer',
                         'in': 'header',
                         'type': 'string',
                         'description': 'Enter jwt token'}}


@api.route('/auth/register')
class register(Resource):
    """Get username and password and register them"""

    @api.expect(user, validate=True)
    def post(self):
        """ Register a User"""
        data = api.payload
        username = data['username']
        password = data['password']
        return db_handler.register(username, password)


@api.route('/auth/login')
class login(Resource):
    """Login a user and return a token"""

    @api.expect(user, validate=True)
    def post(self):
        """ Login a user and return a token"""
        data = api.payload
        username = data['username']
        password = data['password']
        user, pasword_hash = db_handler.get_user(username)
        if user and db_handler.confirm_password_hash(password, pasword_hash):
            print('The user is confirmed')
            access_token = create_access_token(identity=username)
            return {'message': 'Token created',
                    'access_token': access_token}, 201
        return {'message': 'Invalid username or password'}, 401


@api.route('/questions')
class AllQuestions(Resource):
    """Get and create questions as specified"""

    @jwt_required
    @api.doc(params=jwt)
    def get(self):
        """Get all questions asked """
        current_user = get_jwt_identity()
        print(current_user)
        questions = db_handler.get_all_questions(current_user)
        return questions

    @jwt_required
    @api.doc(params=jwt)
    @api.expect(question, validate=True)
    def post(self):
        """Creates a question for a logged in user """
        current_user = get_jwt_identity()
        data = api.payload
        title = data['title']
        body = data['body']
        author = current_user
        return db_handler.create_question(title, body, author)


@api.route('/questions/<int:_id>')
class Question(Resource):
    """Shows single items of the resources created"""

    @jwt_required
    @api.doc(params=jwt)
    def get(self, _id):
        ''' Get a given resource/question based on id '''
        return db_handler.get_question(_id)

    @jwt_required
    @api.doc(params=jwt)
    def delete(self, _id):
        '''Delete a certain resource/question given an id'''
        current_user = get_jwt_identity()
        db_handler.delete_questions(_id, current_user)
        return {'message': 'question {} deleted'.format(_id)}, 202


@api.route('/questions/<int:_id>/answers')
class QuestionsReply(Resource):
    """Reply to a specific question"""
    @jwt_required
    @api.doc(params=jwt)
    @api.expect(answer, validate=True)
    def post(self, _id):
        '''Get a question and reply to it with an Answer '''
        current_user = get_jwt_identity()
        data = api.payload
        db_handler.answer_question(current_user, _id, data['body'])
        return {'message': 'answer created for  question {}'.format(_id)}, 201


@api.route('/profile')
class Userprofile(Resource):
    """Shows single user profile"""

    @jwt_required
    @api.doc(params=jwt)
    def get(self):
        current_user = get_jwt_identity()
        ''' Returns the user profile '''
        return db_handler.user_profile(current_user)


@api.route('/questions/<int:question_id>/answers/<int:ans_id>')
class Answerupdate(Resource):
    """Mark an answer as accepted or update an answer"""
    @jwt_required
    @api.doc(params=jwt)
    @api.expect(answer, validate=False)
    # @api.marshal_with(answer, skip_none=True, code=201)
    def put(self, question_id, ans_id):
        data = api.payload
        question_id = question_id
        answer_id = ans_id
        current_user = get_jwt_identity()
        # print(current_user)
        accept_status = data['accept_status']
        body = data['body']
        # print(answer_id, question_id)
        return db_handler.update(current_user, body, accept_status, question_id, answer_id)


@api.errorhandler
def server_error_handler(error):
    '''Default error handler for 401 errors'''
    return {'message': str(error)}, getattr(error, 'code', 401)
