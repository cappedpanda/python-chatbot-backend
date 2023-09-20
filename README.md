# RH Chatbot Backend

RH_Chatbot_backend is a Python API used to manage the backend (questions / answers) of the application called "RH BOT".


## Prerequisites

To run the project in a local environment, you need a pipenv tool installed to run the project in a virtual environment.


## Installation and use of the virtual environment

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements or :

```bash
# Init the virtual env
pipenv --python 3.7
# Enter the virtual env
pipenv shell
# Install project dependencies
pipenv install --dev
# Run local NLP server
cd RH_Chatbot_backend/nlp
python bot-run.py
# Run local development server
python main.py
```
Now go to the http://127.0.0.1:5000/init and http://127.0.0.1:5000/ask links to query the server and receive responses.


## Utilization

With a POST method the link 'http://127.0.0.1:5000/init' allows to send the initial message to the user as soon as the interface is provided.

Thus, the link 'http://127.0.0.1:5000/ask' allows to receive questions from the user and to generate a response based on the link of the NLP server and the database containing the answers of each intention and entities.

With the help of Postman, with the link 'http://127.0.0.1:5000/ask' and a POST method, we can provide a BODY which is indeed a Json object like the example below:

```
{
	"msg": "quelles sont les conditions pour demander un congé ?",
	"nlp-url": "http://127.0.0.1:5002/parse",
	"collection": "contrats"
}

```

And as output, the API similarly returns a Json object as below:

```
{
    "success": "Message sent with success",
    "text": "quelles sont les conditions pour demander un congé ?",
    "msg-type": "text",
    "bot": {
        "response": "Pour acquérir la possibilité d’obtenir un congé annuel, il faut passer une période minimale de 6 mois en travaillant dans l’entreprise.",
        "quickReplies": true,
        "quicks": [
            "congé",
            "contrats",
            "obligation patronale"
        ]
    }
}
```

And all requests information are saved in project master Database in collection named "history".


## Database

For the parameters of the project database named "pandachatbot", the "data" & "history" collections necessary for resolving chatbot responses and recording conversational history are available in the folder 'RH_Chatbot_backend/collections'.

Thus, the configuration of the database is possible within the module 'RH_Chatbot_backend/api/db.py' precisely in the class 'DB(object)', where the developer can change the name, the domain, the port, the username and password of the database.

Example:

```
class DB(object):
    # Database model

    Domain = '127.0.0.1'
    Port = 27017
    Username = 'admin'
    Password = 'admin'
    Database = 'pandachatbot'
    Collection = None
    authMechanism = 'SCRAM-SHA-256'
```

