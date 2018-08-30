
# StackOverFlow-Lite
StackOverFlow-Lite App is an application that provides users with the ability to reach out to ask a question and get an answer.

#Build status
[![Build Status](https://travis-ci.org/bozicschucky/AndelaWeek2.svg?branch=ft-heroku)](https://travis-ci.org/bozicschucky/AndelaWeek2)

# Getting Started



**Application Features**

* Posting questions
* Answering user's questions
* Answering user's questions
* User can get a questions by id
* User can delete a specific question
* User can select a answer as a favorite


**Usage**

* On the browser,visit the following url

* Some of the data arguments to be passed in postman
  * Users register/Login Endpoint takes the following data.  
  ` {
        "username": "string",
        "password": "string"
          }
    `    
   * Users Question json data Endpoint takes the following data.  
   `
   {
      "title": "string",
      "body": "string"
    }
    `

   * Users Answer json data Endpoint takes the following data.  
   `
   {
      "body": "string"
    }
    `


* To interact with the API via Postman, use the link below



    then use the following endpoints to perform the specified tasks

    EndPoint                            | Functionality
    ------------------------            | ----------------------
    `GET /questions `                     | User can get all questions asked
    `GET /questions/<int:id>  `               | User can a particular question asked
    `POST /questions            `         | User can create a question
    ` POST /questions/<int:id>/answers`        | Create a particular answer to a question
    ` DELETE /questions/<int:id>       `       | Delete a particular question asked

# How To Manually Test It:

  1. Clone the project to your local machine:

   `git clone https://github.com/bozicschucky/AndelaWeek2.git`

  2. Navigate to project directory:

   `cd AndelaWeek2`

  3. Change branch to `ft-db-API`:

     `git checkout ft-db-API`

      * Activate a virtual environment
      * pip install requirements.txt
      * The run the python run.py to run the whole project
      * Visit the endpoints descibed above using post man to test the endpoints


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
