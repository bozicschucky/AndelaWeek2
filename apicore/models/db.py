import psycopg2
from pprint import pprint
from passlib.hash import pbkdf2_sha256 as sha256
from .questions import Question
from .users import User
from .answers import Answer


class DBhandler(User, Answer, Question):
    """ DBhandler class for postgres"""

    def __init__(self, host, database, user, password):
        try:
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.conn = psycopg2.connect(host=self.host,
                                         database=self.database,
                                         user=self.user,
                                         password=self.password)
            # host="localhost", database="api", user="postgres", password="sudo"
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            print('Connection successful')
        except (Exception, psycopg2.DatabaseError) as e:
            pprint(e, "Can't connect to the db ")

    def close_db_connection(self):
        ''' closes connection to a database '''
        print('committing changes to db')
        self.conn.commit()
        print('db connection closed ')
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        '''creates tables in the postgres database'''
        commands = (
            """
            CREATE TABLE IF NOT EXISTS  users(
              id serial,
              username VARCHAR(25) UNIQUE NOT NULL,
              password VARCHAR(100) NOT NULL,
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
              published_date timestamp DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            );
            """,
        )
        for command in commands:
            self.cursor.execute(command)
            print('tables created successfully')
        # self.close_db_connection()

    def drop_table(self, *table_names):
        ''' Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            pprint('all tables dropped')
            self.cursor.execute(drop_table)

    def hash_password(self, password):
        return sha256.hash(password)

    def confirm_password_hash(self, password, pasword_hash):
        return sha256.verify(password, pasword_hash)

    def register(self, username, password):
        ''' adds users to the database '''
        password = self.hash_password(password)
        user = User(username, password)
        sql = "INSERT INTO users(username,password) VALUES ('{}' ,'{}')".format(
            user.username, user.password)
        pprint(sql)
        self.cursor.execute(sql)
        return {'message': 'User successfully registered'}

    def get_user(self, username):
        '''Gets a user to the database '''
        try:

            sql = "SELECT id,username,password FROM users WHERE username = '{}'".format(
                username)
            self.cursor.execute(sql)
            user = self.cursor.fetchone()
            username = user[1]
            password = user[2]
            return user, password
        except Exception as e:
            # print({'error': 'User not found {}'.format(e)})
            return{'message': 'User not found'}, 404

    def create_question(self, title, body, author):
        ''' Create a question '''
        user_sql = "SELECT id FROM users WHERE username = '{}'".format(
            author)
        self.cursor.execute(user_sql)
        user = self.cursor.fetchone()
        print(user[0])
        # user_id
        question = Question(title, body, author)
        sql = "INSERT INTO questions(user_id,title,body,author) VALUES ({} ,'{}','{}','{}')".format(
            user[0], question.title, question.body, question.author)
        print(sql)
        self.cursor.execute(sql)
        return {'message': 'Question created'}, 201

    def get_all_questions(self, current_user):
        ''' Gets one questions from a database'''
        sql = "SELECT id,title,body FROM questions WHERE author = '{}' ".format(
            current_user)
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        questions = [questions for questions in rows]
        # print(questions)
        last_questions = []
        for index in range(len(questions)):
            # print(question)
            user_questions = (
                {'id': questions[index][0],
                 'title': questions[index][1],
                 'body': questions[index][2]})
            last_questions.append(user_questions)

        return {'all_questions': last_questions}

    def get_question(self, _id, current_user):
        ''' Gets one questions from a database table based on user'''
        try:
            question_sql = "SELECT title,body,author,published_date FROM questions WHERE id = {} AND author = '{}'".format(
                _id, current_user)
            self.cursor.execute(question_sql)
            question = self.cursor.fetchone()
            print(question)
            # question_id = question[0]
            print(question)
            answers_sql = "SELECT id,body,accept_status FROM answers WHERE question_id = {}".format(
                _id)
            self.cursor.execute(answers_sql)
            answers = self.cursor.fetchall()
            answers = [row for row in answers]
            fetched_answers = []
            for index in range(len(answers)):
                user_answers = (
                    {
                        'id': answers[index][0],
                        'body': answers[index][1]
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

    def answer_question(self, _id, body):
        ''' Creates an answer to a question '''
        question_sql = "SELECT id FROM questions WHERE id = {}".format(_id)
        self.cursor.execute(question_sql)
        question = self.cursor.fetchone()
        question_id = question[0]
        print(question[0])
        # question_id
        sql = "INSERT INTO answers(question_id,body) VALUES ({},'{}')".format(
            question_id, body)
        print(sql)
        self.cursor.execute(sql)

    def update(self, accept_status, question_id):
        ''' updates the question asked '''
        sql = 'UPDATE answers SET accept_status = {} WHERE id = {}'.format(
            accept_status, question_id)
        self.cursor.execute(sql)
        return {'message': 'Answer status updated'}

    def delete_questions(self, _id, current_user):
        '''Deletes a question given an id '''
        sql = "DELETE FROM questions WHERE  id = {} AND author = '{}' ".format(
            _id, current_user)
        rows_deleted = self.cursor.rowcount
        print(rows_deleted)
        self.cursor.execute(sql)
        return {"message": "Question {} deleted".format(_id)}


db = DBhandler(host="localhost", database="api",
               user="postgres", password="sudo")

# db.get_question()
