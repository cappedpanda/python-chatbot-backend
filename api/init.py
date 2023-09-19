from flask import Flask
from flask_restful import (Resource, Api)

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)


class Initiation(Resource):
    # Initialisation message class

    @staticmethod
    def post():
        json_object = dict({
            'success': 'Message sent with success',
            'bot': dict(msg='Bonjour, je suis à votre disposition. Que puis-je faire pour vous ?',
                        quickReplies=True, quicks=["congé", "contrats", "obligation patronale"])
        })

        return json_object, 200, {'Access-Control-Allow-Origin': '*',
                                  'Content-Type': 'application/json', }


