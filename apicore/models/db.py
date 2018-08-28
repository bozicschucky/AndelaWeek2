import psycopg2
from pprint import pprint
from passlib.hash import pbkdf2_sha256 as sha256


class DbConnect():
    """ DBhandler class for postgres"""

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost", database="api", user="postgres", password="sudo"
            )
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
              published_date timestabmp DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            );
            """,
        )
        for command in commands:
            self.cursor.execute(command)
            print('tables created successfully')
        self.close_db_connection()

    def drop_table(self, *table_names):
        ''' Drops the tables created '''
        for table_name in table_names:
            drop_table = "DROP TABLE IF EXISTS {} CASCADE".format(table_name)
            pprint('all tables dropped')
            self.cursor.execute(drop_table)

    def hash_password(self, password):
        return sha256.hash(password)

    def register(self, username, password):
        ''' adds users to the database '''
        sql = "INSERT INTO users(username,password) VALUES ('{}' ,'{}')".format(
            username, password)
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
            return {'error': 'User not found {}'.format(e)}
