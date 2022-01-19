# Full Stack Capstone project

## project description
This project performed as part of Udacity FSND program. it is casting agency that has three models actor,movies and cast model which connect the actors with the movie they act in.the project used python,flask and sqlalchemy.

## Getting Started

### Installing Dependencies

#### Python 3.8.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the project folder directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## Runnig the application locally

### Database Setup
- Update the database url in models.py file to connect with your database
- uncomment the db.create_all() or use the command
```bash
flask db upgrade
```

### Running the server
From within the `capstone` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
now you can find the app in localhost:5000

### Test the application using unittest
- Update the database name in test_app.py file to connect with your own database
- the run the file :

```bash
py test_app.py

```
test_app will test both the endpoint and the authorization behavior

## live app in heroku
- the [app](https://finalcapstone-app.herokuapp.com/) is hosted by heroku
- you can use the postman collection within this folder to test all the endpoint and authorization behavior in live  
- please note!!! that if you need to run the postman collection more than one time you will need to update the ids and the arguments that used in the request to avoid the errors.For example if you delete or patch movie already was deleted this will cause 404 error so you need to change the id. Also if you  post movie that you already post that will cause 400 because the name unique constraint so you will need to update the body of the request.   

## Endpoints Documentation
```

Endpoints
GET '/movies'
POST '/movies'
PATCH '/movies/<id>'
DELETE '/movie/<id>'

GET '/actors'
POST '/actors'
PATCH '/actors/<id>'
DELETE '/actors/<id>'

GET '/cast'
POST '/cast'
GET '/actors/<id>/movies'
GET '/movies/<id>/actors'





GET '/movies'
- Fetches a dictionary of movies from the database
- Request Arguments: None
- Returns: dictionary of all movies in the database  
{
    "movies": [
        {
            "id": 7,
            "name": "sideEffects",
            "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
        },
        {
            "id": 8,
            "name": "pink panther",
            "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
        }
    ],
    "success": true
}

POST '/movies'
- This endpoint will add a new movie to the database
- Request Arguments: it will take the movie name, and the release date of the movie
- Returns: An object with a  key, success, that has value of True to ensure that the movie was added successfully and dictionary of the added movie
{
  "success":True,
"movie": {
      "id": 8,
      "name": "pink panther",
      "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
  }
}

PATCH '/movies/8'
- This endpoint will edit existing movie
- Request Arguments: it will take the movie name, and the release date of the movie
- Returns: An object with a  key, success, that has value of True to ensure that the movie was updated successfully and dictionary of the updated movie
{
  "success":True,
"movie": {
      "id": 8,
      "name": "pink panther",
      "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
  }
}


DELETE '/movies/1'
- This endpoint take a movie id and delete the movie with that id from the database a
- Request Arguments: id
- Returns: An object with a  key, success, that has value of True to ensure that the question was deleted successfully and the id of deleted movies
{
  "success":True,
  'delete':1
}

GET '/actors'
- Fetches a dictionary of actors from the database
- Request Arguments: None
- Returns: dictionary of all actors in the database
{
    "actors": [
        {
            "gender": "F",
            "id": 7,
            "name": "Actor 1"
        },
        {
            "gender": "F",
            "id": 12,
            "name": "Actor XXXX"
        }
    ],
    "success": true
}

POST '/actors'
- This endpoint will add a new actor to the database
- Request Arguments: it will take the actor name, and the gender of the actor
- Returns: An object with a  key, success, that has value of True to ensure that the actor was added successfully and dictionary of the added actor
{
  "success":True,
"actor": {
      "id": 7,
      "name": "actor xxx",
      "gender": "M"
  }
}

PATCH '/actors/7'
- This endpoint will edit existing actor
- Request Arguments: it will take the actor name, and the gender of the actor
- Returns: An object with a  key, success, that has value of True to ensure that the movie was updated successfully and dictionary of the updated actor
{
  "success":True,
"actor": {
      "id": 7,
      "name": "actor2",
      "gender": "M"
  }
}

DELETE '/actors/1'
- This endpoint take a actor id and delete the actor with that id from the database
- Request Arguments: id
- Returns: An object with a  key, success, that has value of True to ensure that the actor was deleted successfully and the id of deleted actor
{
  "success":True,
  'delete':1
}

GET '/cast'
- Fetches a dictionary of cast from the database
- Request Arguments: None
- Returns: dictionary of all cast in the database
{
    "casts": [
        {
            "actor_id": 6,
            "id": 2,
            "movie_id": 6
        },
        {
            "actor_id": 7,
            "id": 3,
            "movie_id": 6
        }
    ],
    "success": true
}

POST '/cast'
- This endpoint will add a new cast to the database
- Request Arguments: it will take the movie id, and the actor_id
- Returns: An object with a  key, success, that has value of True to ensure that the cast was added successfully and dictionary of the added cast
{
  "success":True,
"cast": {
      "id": 8,
      "movie_id": "2",
      "actor_id": "1"
  }
}

GET '/movies/1/actors'
- using the relationship in cast model to obtain all actors who work in movie with id 1 from the database
- Request Arguments: movie id
- Returns: dictionary of  actors who work in one movie in the database
{
  "actors": [
    {
        "gender": "F",
        "id": 7,
        "name": "Actor 1"
    },
    {
        "gender": "F",
        "id": 13,
        "name": "Actor yyyy"
    }
],
"success": true
}

GET '/actors/1/movies'
- using the relationship in cast model to obtain all movies who done by the same
- Request Arguments: actor id
- Returns: dictionary of movies which done by actor with id=1

{
    "movies": [
        {
            "id": 6,
            "name": "movie name",
            "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
        },
        {
            "id": 8,
            "name": "pink panther",
            "releaseDate": "Sun, 01 Jan 2006 00:00:00 GMT"
        }
    ],
    "success": true
}

DELETE '/cast/1'
- This endpoint take a cast id and delete the cast with that id from the database a
- Request Arguments: id
- Returns: An object with a  key, success, that has value of True to ensure that the cast was deleted successfully and the id of deleted cast
{
  "success":True,
  'delete':id
}

```


## Auth0
1. permissions:
  get:movies		
  get:actors
  get:cast
  delete:movie		
  delete:actor
  delete:cast
  post:movie		
  post:actor
  post:cast
  patch:movie
  patch:actor
2. roles:
  - Casting Assistant
    - Can view actors and movies and cast
  - Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
  - Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie and cast from the database
3. Access Token:
  - Casting Assistant:
      eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRFazJyQ0pwcFJrSFpySzVlMEJ1aiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmR1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDY0YjVkYTAxZTJjNTAwNjkyMTIzY2EiLCJhdWQiOiJjYXN0IiwiaWF0IjoxNjQyNTQ5MTA1LCJleHAiOjE2NDI2MzU1MDUsImF6cCI6IlE3aUp2Vlhoa3dUOUw4Tmo4eWFOMU00Rm50Q2NvdnJaIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmNhc3QiLCJnZXQ6bW92aWVzIl19.fhTfKEiHYT0cM1j4O_FbewS8Fl06CE_2kBFbu-BI5-ItYztvTmqN9MzalAtv3eONVcjOXf4lfeJ6T61iEEmG1egjBrXX-PBrT_C3kbJ-aaenrMa9R_S9Rf8Rr1T-ecSjKSMQPsIySiuTDATns1j5ZmEjwANCG3kusvjDSKWAcwSV8GGETXztaiuhkZtogOh2_1PtqIZpaZkr8vmKX_TVHOU24DVMyaQbdqWOVsCtuhmlmOat1oZHgunLyY1Lu9zTqpOlBM4uJNSQWsS_c00CewFpSP-QSrRoVWmvsC4casuHyzhunFw6rb-t5cmuKy_CMjjp4igW9tRpmMjGCcznVw
  - Casting Director:
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRFazJyQ0pwcFJrSFpySzVlMEJ1aiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmR1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDY0YjYzNjAzNDYyMzAwNjlmNzQ0NWYiLCJhdWQiOiJjYXN0IiwiaWF0IjoxNjQyNTQ5Mzc4LCJleHAiOjE2NDI2MzU3NzgsImF6cCI6IlE3aUp2Vlhoa3dUOUw4Tmo4eWFOMU00Rm50Q2NvdnJaIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmNhc3QiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.pNXLYzObNE01DJSaVRe94KQhEimDBMwDYDBEORewyMUTWohbPxGOh-eK0pZZFpb9g1oL0X_AbVJ8U_JEmnzP_QGlk_R1HpboWxlbDMd6yfSG7AQ5uvpZglnQ_7-33AZ8kxXCRmZzAFVS2l-Dt56wWjE30bOXEkr6tO_PbT4aA7dGlU5Bh2RsuKKvLAldTyO64JiATKO2zcUK_8rIvyh0FIJdFGizzhhhqaShVsCXt8qDuTHGFhnC_4oOLrM6aqABVHvOUsvxScFoZ5xC_73MskrvsBqEVOtzjoX--Nd5G0dAro2Xxz4vQdqrYGzQXxJCE65aXVPsKFHf685elYsJvA

  - Executive Producer:
     access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRFazJyQ0pwcFJrSFpySzVlMEJ1aiJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LWZzbmR1LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwMzAyMTMxNzA1NzkwMTQwMDI1NCIsImF1ZCI6ImNhc3QiLCJpYXQiOjE2NDI1NDg0OTIsImV4cCI6MTY0MjYzNDg5MiwiYXpwIjoiUTdpSnZWWGhrd1Q5TDhOajh5YU4xTTRGbnRDY292cloiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTpjYXN0IiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDpjYXN0IiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDpjYXN0IiwicG9zdDptb3ZpZSJdfQ.jG0YmRVa9CvOzvjeO_GnmCsIo4bU3F32PUU2X6V_vok6fDwtzlChnLioD2FDyCp_gJhUySPSM9f1cJaOvAULH66RI3XWEqwz66yb9--OT_tc2d-gBcPzS1Cs3W7i3qRsPYIoCzxhtPqF6qKZCQBglh-5KGN5MeX3woJn3wBPOFjdBSw0cNKTAB30clTDXxS7w1pflFjCt5wxUbWBx_Ou7ji0XlZHOL1eovNs4x4q39cJTOGk38dUBeRg6uGbTFmYRFrvoryIFeTWdxzZER0o3iEn3oJC5OTEU3CqMSZe6OS2xRT89FlP6_hNpoYqJELTPTOQUq4TvfAL9MQ8wh6EUw
