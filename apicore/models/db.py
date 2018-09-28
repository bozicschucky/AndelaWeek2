import psycopg2
from pprint import pprint
from passlib.hash import pbkdf2_sha256 as sha256
from .questions import Question
from .users import User
from .answers import Answer
import os


class DBhandler(User, Answer, Question):
    """ DBhandler class for postgres"""

    def __init__(self, host, database, user, password):
        if os.getenv('APP_SETTINGS') == 'testing':
            self.db = 'api_test'
        else:
            self.db = os.getenv('Database')

        try:
            self.host = host
            self.database = self.db
            self.user = user
            self.password = password
            self.conn = psycopg2.connect(host=self.host,
                                         database=self.database,
                                         user=self.user,
                                         password=self.password)
            print(self.database)
            print(os.getenv('APP_SETTINGS'))
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print('Connection successful')
        except (Exception, psycopg2.DatabaseError) as e:
            pprint(e, "Can't connect to the db ")

    def create_table(self):
        '''creates tables in the postgres database'''
        commands = (
            """
            CREATE TABLE IF NOT EXISTS  users(
              id serial,
              username VARCHAR(25) UNIQUE NOT NULL,
              password VARCHAR(100) NOT NULL,
              join_date timestamp DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS questions(
              id serial,
              user_id int NOT NULL,
              title VARCHAR(100) NOT NULL,
              body VARCHAR(1000) NOT NULL,
              author VARCHAR(100) NOT NULL,
              published_date timestamp DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            """,
            """
            CREATE TABLE IF NOT EXISTS  answers(
              id serial,
              question_id int NOT NULL,
              body VARCHAR(2550),
              accept_status boolean DEFAULT FALSE,
              author VARCHAR(100) NOT NULL,
              published_date timestamp DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              FOREIGN KEY (question_id) REFERENCES questions(id) \
              ON DELETE CASCADE
            );
            """,
        )
        for command in commands:
            self.cursor.execute(command)

    def drop_table(self, *table_names):
        ''' Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            self.cursor.execute(drop_table)

    def hash_password(self, password):
        return sha256.hash(password)

    def confirm_password_hash(self, password, pasword_hash):
        return sha256.verify(password, pasword_hash)

    def register(self, username, password):
        ''' adds users to the database '''
        try:
            password = self.hash_password(password)
            user = User(username, password)
            sql = "INSERT INTO users(username,password) VALUES \
            ('{}' ,'{}')".format(user.username, user.password)
            self.cursor.execute(sql)
            return {'message': 'user is successfully registered'}, 201
        except Exception as e:
            return {'message': 'username {} \
                    already taken '.format(username)}, 400

    def get_user(self, username):
        '''Gets a user to the database '''
        try:

            sql = "SELECT id,username,password FROM users \
             WHERE username = '{}'".format(username)
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            username = user[1]
            password = user[2]
            return user, password
        except Exception as e:
            return{'message': 'User not found'}, 404

    def create_question(self, title, body, author):
        ''' Create a question '''
        user_sql = "SELECT id FROM users WHERE username = '{}'".format(
            author)
        self.cursor.execute(user_sql)
        user = self.cursor.fetchone()
        question = Question(title, body, author)
        sql = "INSERT INTO questions(user_id,title,body,author) \
         VALUES ({} ,'{}','{}','{}')".format(
            user[0], question.title, question.body, question.author)
        self.cursor.execute(sql)
        return {'message': 'Question created'}, 201

    def get_all_questions(self, current_user):
        ''' Gets one questions from a database'''
        sql = "SELECT id,title,body FROM questions \
         WHERE author = '{}' ORDER BY published_date desc ".format(
            current_user)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        questions = [questions for questions in rows]
        last_questions = []
        platform = []

        sql = """ SELECT id,title,body,author FROM questions WHERE
                    author != '{}' ORDER BY published_date desc """\
                    .format(current_user)
        self.cursor.execute(sql)
        row = self.cursor.fetchall()
        platform_questions = [questions for questions in row]
        for index in range(len(questions)):
            user_questions = (
                {'id': questions[index][0],
                 'title': questions[index][1],
                 'body': questions[index][2]})
            last_questions.append(user_questions)

        for index in range(len(platform_questions)):
            plat_questions = (
                {'id': platform_questions[index][0],
                 'title': platform_questions[index][1],
                 'body': platform_questions[index][2],
                 'author': platform_questions[index][3]})
            platform.append(plat_questions)

        return {'all_questions': last_questions,
                'user': current_user, 'platform_questions': platform}

    def get_question(self, _id):
        ''' Gets one questions from a database table based on user'''
        try:
            question_sql = """ SELECT title,body,author,published_date FROM
                            questions WHERE id = {} ORDER BY
                                        published_date desc """.format(_id)
            self.cursor.execute(question_sql)
            question = self.cursor.fetchone()
            answers_sql = """ SELECT id,body,accept_status,author FROM answers
             WHERE question_id = {} ORDER BY published_date desc""".format(_id)
            self.cursor.execute(answers_sql)
            answers = self.cursor.fetchall()
            answers = [row for row in answers]
            fetched_answers = []
            for index in range(len(answers)):
                user_answers = (
                    {
                        'id': answers[index][0],
                        'body': answers[index][1],
                        'status': answers[index][2],
                        'author': answers[index][3]
                    })
                fetched_answers.append(user_answers)
            return {'question': {'title': question[0],
                                 'body': question[1],
                                 'author': question[2],
                                 'date': str(question[3]),
                                 'answers': fetched_answers

                                 }}
        except Exception as e:
            return{'message': 'Quesion {} does\'nt exist'.format(_id)}, 404

    def answer_question(self, author, _id, body):
        ''' Creates an answer to a question '''
        try:
            question_sql = "SELECT id FROM questions WHERE id = {}".format(_id)
            self.cursor.execute(question_sql)
            question = self.cursor.fetchone()
            question_id = question[0]
            answer = Answer(body)
            sql = "INSERT INTO answers(question_id,body,author) \
             VALUES ({},'{}','{}')".format(
                question_id, answer.body, author)
            self.cursor.execute(sql)
        except Exception as e:
            return {'message': 'Question does\'nt exist'}

    def user_profile(self, current_user):
        ''' returns the logged in user profile '''
        sql = "SELECT id,title,body FROM questions \
         WHERE author = '{}' ORDER BY published_date desc ".format(
            current_user)
        self.cursor.execute(sql)
        questions = self.cursor.fetchall()
        question_ids = []
        answers = []
        recent_questions = []
        for i in range(len(questions)):
            question_ids.append(questions[i][0])
            recent_questions.append(questions[i][1])
        print(question_ids)
        for i in question_ids:
            answers_sql = "SELECT id,body,accept_status \
             FROM answers WHERE question_id = {}".format(
                i)
            self.cursor.execute(answers_sql)
            user_answers = self.cursor.fetchall()
            details = {
                str(i): user_answers
            }
            answers.append(details)

        number_of_questions = len(questions)
        data = {
            'username': current_user,
            'number_of_questions': number_of_questions,
            'recent': recent_questions,
            'question_ids': question_ids,
            'answers': answers
        }
        return data, 200

    def update(self, current_user, body,
               accept_status, question_id, answer_id):
        ''' updates the question asked '''
        user_sql = "SELECT author FROM questions \
         WHERE author = '{}' AND id={} ".format(current_user, question_id)
        self.cursor.execute(user_sql)
        question_author = self.cursor.fetchone()

        if question_author:
            question_author = question_author[0]
        elif question_author is None:
            question_author = False

        answer_sql = """ SELECT author FROM answers WHERE author='{}'
                            AND question_id = {} AND id = {} """.format(
            current_user, question_id, answer_id)
        self.cursor.execute(answer_sql)
        answer = self.cursor.fetchone()
        answer_author = answer
        if answer_author:
            answer_author = answer_author[0]
        elif answer_author is None:
            answer_author = False

        if question_author:
            sql = """ UPDATE answers SET accept_status = {}
                            WHERE id = {} AND question_id = {}
                            """.format(accept_status, answer_id, question_id)
            self.cursor.execute(sql)
            return {'message': 'Answer status updated'}, 200
        elif answer_author:

            sql = "UPDATE answers SET body = '{}' WHERE id = {}".format(
                body, answer_id)
            self.cursor.execute(sql)
            return {'message': 'Answer Body updated successfully'}, 200
        else:
            return {'message': 'You are not allowed to update these details'},\
                401

    def delete_questions(self, _id, current_user):
        '''Deletes a question given an id '''
        sql = """ DELETE FROM questions WHERE  id = {}
                        AND author = '{}' """.format(_id, current_user)
        self.cursor.execute(sql)
        return {"message": "Question {} deleted".format(_id)}
