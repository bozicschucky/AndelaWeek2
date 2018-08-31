
# StackOverFlow-Lite
StackOverFlow-Lite App is an application that provides users with the ability to reach out to ask a question and get an answer.

# Build status  
[![Build Status](https://travis-ci.org/bozicschucky/AndelaWeek2.svg?branch=ft-heroku)](https://travis-ci.org/bozicschucky/AndelaWeek2)
[![Coverage Status](https://coveralls.io/repos/github/bozicschucky/AndelaWeek2/badge.svg?branch=ft-heroku)](https://coveralls.io/github/bozicschucky/AndelaWeek2?branch=ft-heroku)
[![Maintainability](https://api.codeclimate.com/v1/badges/ae1d59f2e0eda6149a6f/maintainability)](https://codeclimate.com/github/bozicschucky/AndelaWeek2/maintainability)

# Getting Started



**Application Features**

* Posting questions
* Answering user's questions
* Answering user's questions
* User can get a questions by id
* User can delete a specific question
* User can select a answer as a favorite


**Usage**
  * checkout the documentated version [StackOverFlow-Lite](https://stackoverflowlite2.herokuapp.com/)


* Some of the data arguments to be passed in postman
  * Users register/Login Endpoints takes the following data.  
  ` {
        "username": "string",
        "password": "string"
          }
    `    
   * Users Question json data Endpoints takes the following data.  
   `
   {
      "title": "string",
      "body": "string"
    }
    `

   * Users Answer json data Endpoints takes the following data.  
   `
   {
      "body": "string",
      "accept_status":'false'
    }
    `


* To interact with the API via Postman, use the link below  
    * The  base url is ` https://stackoverflowlite2.herokuapp.com/api/v2/ `

    * Then use the following endpoints to perform the specified tasks

    EndPoint                            | Functionality
    ------------------------            | ----------------------
    `POST /auth/register `                     | User first has to register
    `POST /auth/login `                     | User login in to get a jwt token
    `GET /questions `                     | User can get all questions asked
    `GET /questions/<int:id>  `               | User can a particular question asked
    `POST /questions            `         | User can create a question
    ` POST /questions/<int:id>/answers`        | Create a particular answer to a question
    ` DELETE /questions/<int:id>       `       | Delete a particular question asked

# How To Manually Test It:

  1. Clone the project to your local machine:

    * `git clone https://github.com/bozicschucky/AndelaWeek2.git`

  2. Navigate to project directory:

    * `cd AndelaWeek2`

  3. Change branch to `ft-heroku`:

     `git checkout ft-heroku`

      * Activate a virtual environment using `python3 -m virtualenv venv`
      * pip install requirements.txt using `pip install -r requirements.txt`
      * Then run the flask app using `python run.py`   to run the whole project
      * Visit the endpoints described above using post man or the documentated version to test the endpoints

  4. To run the unittests:
      * set up a test database called 'api_test'
      * set the database name in the Os environment using `export APP_SETTINGS="testing"`
      * using Nose test runner run the tests using `nosetests --with-coverage`
      * this should run all the app tests and return the coverage


  4.  Tools used to develop this Api.  
        * Postgres version 10  
        * Flask 1.0.2  
        * Flask-JWT-Extended   
        * Flask-restplus 0.11.0  
        * Autoenv   
        * Swaggerui To document the API   





# Authors
 - Sekito charles

# License
MIT
