import psycopg2
from pprint import pprint


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
