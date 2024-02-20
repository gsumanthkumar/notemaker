# NoteMaker CRUD API WITH DJANGO REST FRAMEWORK
[Django REST framework](http://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

## Requirements
- Python 3.12.0
- Django 5.0.2
- Django REST Framework

## Installation
After you cloned the repository, you want to create a virtual environment, so you have a clean python installation.
You can do this by running the command
```
python -m venv env
```

After this, it is necessary to activate the virtual environment, you can get more information about this [here](https://docs.python.org/3/tutorial/venv.html)

You can install all the required dependencies by running
```
pip install -r requirements.txt
```
We have to make migrations after installing requirements.

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have three resources, `signup`,`notes`,`notesvh` so we will use the following URLS - `/notes/`,`signup`,`notesvh` and `/notes/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`signup/` | POST | CREATE | User Signup
`login/` | POST | CREATE | User Login
`signout/` | POST | CREATE | User Logout
`notes/create/` | POST | CREATE | Create Note
`notes/id/` | GET | READ | Get a single Note
`notes/share/`| POST | CREATE | Share not with other users
`notes/id/` | PUT | UPDATE | Update a Note
`notes/id/` | DELETE | DELETE | Delete a Note
`notes/version-history/id/`| GET | READ | Get Note Version History

## Use
We can test the API using [Postman](https://www.postman.com/)

```

First, we have to start up Django's development server.
```
python manage.py runserver

For understanding Payload ->

signup/ - POST

curl --location 'http://127.0.0.1:8000/signup/' \
--header 'Cookie: csrftoken=zMcnzOIhKQaziKCuOxKfan3wQvpxYWfe; sessionid=42c6y9mj512vi09kehhbjxlpcq9t99zw' \
--form 'username="test6"' \
--form 'password="test7"'

login/ - POST

curl --location 'http://127.0.0.1:8000/login/' \
--header 'Cookie: csrftoken=JgcBVVbIjSpZlFAX4m2myQ6wxa9FXeto; sessionid=kyewtvvgmkxfeqe3og2tvuhvzfhwvbbx' \
--form 'username="test1"' \
--form 'password="test1"'

signout/ - POST

curl --location --request POST 'http://127.0.0.1:8000/signout/' \
--header 'Authorization: Token 0976b0f012d394a64916fc0c7869096d54310c18' \
--header 'Cookie: csrftoken=JgcBVVbIjSpZlFAX4m2myQ6wxa9FXeto; sessionid=kyewtvvgmkxfeqe3og2tvuhvzfhwvbbx'

notes/create/ - POST

curl --location 'http://127.0.0.1:8000/notes/create/' \
--header 'Authorization: Token 1193548f4ca78826f866aa47dcd1e6d42369801e' \
--header 'Cookie: csrftoken=bRNyao4snr0D7RyUuaUguzVOFckxOObt; sessionid=8upjli25lxv4e1e2r879p83ctvbkdavq' \
--form 'text="sample notes 10"'

notes/id/ - GET, PUT, DELETE

curl --location 'http://127.0.0.1:8000/notes/3/' \
--header 'Authorization: Token 1193548f4ca78826f866aa47dcd1e6d42369801e' \
--header 'Cookie: csrftoken=JgcBVVbIjSpZlFAX4m2myQ6wxa9FXeto; sessionid=kyewtvvgmkxfeqe3og2tvuhvzfhwvbbx'

notes/share/ - POST

curl --location 'http://127.0.0.1:8000/notes/share/' \
--header 'Authorization: Token 1193548f4ca78826f866aa47dcd1e6d42369801e' \
--header 'Cookie: csrftoken=bRNyao4snr0D7RyUuaUguzVOFckxOObt; sessionid=8upjli25lxv4e1e2r879p83ctvbkdavq' \
--form 'nid="17"' \
--form 'shared_with="45"'

notes/version-history/id/ - GET

curl --location 'http://127.0.0.1:8000/notes/version-history/18/' \
--header 'Authorization: Token 1193548f4ca78826f866aa47dcd1e6d42369801e' \
--header 'Cookie: csrftoken=JgcBVVbIjSpZlFAX4m2myQ6wxa9FXeto; sessionid=kyewtvvgmkxfeqe3og2tvuhvzfhwvbbx'
```
Only authenticated users can use the API services:
```
http http://127.0.0.1:8000/notes/3 "Authorization: Token 1193548f4ca78826f866aa47dcd1e6d42369801e"
```
we get the note with id = 3
```
{"id":3,"text":"sample notes 1","created_at":"2024-02-20T07:44:33.450502Z","updated_at":"2024-02-20T07:44:33.450568Z","owner":2,"shared":[],"owner_name":"test1","message":"Note Fetched successfully."}

```

## Create users and Tokens

First we need to create a user, so we can log in
```
http POST http://127.0.0.1:8000/signup/  username="USERNAME" password="PASSWORD" 
```

After we create an account we can use those credentials to get a token

To get a token first we need to request
```
http http://127.0.0.1:8000/login/ username="username" password="password"
```
after that, we get the token
```
{
    "status": "Logged in",
    "token": "1193548f4ca78826f866aa47dcd1e6d42369801e"
}```


The API has some restrictions:
-   The notes are always associated with a creator (user who created it).
-   Only authenticated users may create and see notes.
-   Only the creator and Shared users of a note may update or delete it.
-   The API doesn't allow unauthenticated requests.
