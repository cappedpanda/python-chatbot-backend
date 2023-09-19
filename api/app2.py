from flask import Flask, jsonify, request, json, Response, send_from_directory
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, abort)
from requests import put, get
import requests
import os

from pymongo import MongoClient

# static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

client = MongoClient('localhost', port=27017)
db = client['pandachatbot']

get1 = db.data.find_one({"intent": "abmissibilite_conge"})
get2 = db.data.find_one({"intent": "procedure_conge"})
get3 = db.data.find_one({"intent": "duree_conge",
                         "entity": "naissance"})
get4 = db.data.find_one({"intent": "duree_conge",
                         "entity": "mariage"})
get5 = db.data.find_one({"intent": "duree_conge",
                         "entity": "decès"})
get6 = db.data.find_one({"intent": "duree_conge",
                         "entity": "circoncision"})
get7 = db.data.find_one({"intent": "duree_conge",
                         "entity": "l'operation chirurgicale"})

convs = {
    'procedure_conge': get2['response'],
    'duree_conge': {'naissance': get3['response'],
                    'mariage': get4['response'],
                    'decès': get5['response'],
                    'circoncision': get6['response'],
                    'l\'operation chirurgicale': get7['response']
                    },
    'admissibilite_congé': get1['response'],
    'insult': "It's not nice to talk like that !! ",
    'how_are_you': "Better than you, what about you ?"
}

images = {
    'procedure_conge': "/static/hello.jpg",
    'duree_conge': "/static/bye.jpg",
    'admissibilite_congé': "/static/insult.jpg",
    'how_are_you': "/static/how_are_you.jpg",
    'get_help': "Didn't exist ! "
}


def abort_if_conv_doesnt_exist(conv_id):
    if conv_id not in convs:
        abort(404, response="Conversation {} doesn't exist".format(conv_id))
        return False
    else:
        return True


parser = reqparse.RequestParser()
parser.add_argument('intent', 'entity')


def is_empty(structure):
    if len(structure) == 0:
        return True
    else:
        return False


class Initiation(Resource):
    @staticmethod
    def get():
        json_object = dict({
            'success': 'Message is sent with success',
            'bot': dict(msg='Bonjour, je suis à votre disposition. Que puis-je faire pour vous ?',
                        quickReplies=True, quick=["congé", "contrats", "obligation patronale"])
        })

        return json_object, 200, {'Access-Control-Allow-Origin': '*',
                                  'Content-Type': 'application/json', }


api.add_resource(Initiation, '/init')


class Conversation(Resource):

    @staticmethod
    def get():
        global entitiz, response
        url = "http://127.0.0.1:5002/parse"
        data = request.get_json()
        body = {"query": data['msg']}
        intent = requests.post(url, data=json.dumps(body))
        entity = requests.post(url, data=json.dumps(body))
        text = requests.post(url, data=json.dumps(body))
        intent = intent.json()['intent']['name']
        entity_array = entity.json()['entities']
        length = len(entity_array)
        i = 0
        entitiz = list()
        while i != length:
            entitiz.append(entity_array[i]['value'])
            i = i + 1
        text = text.json()['text']
        entity_value = entitiz[0]

        if convs[intent]:
            json_object = dict(bot={
                'msg': 'Bonjour, je suis à votre disposition. Que puis-je faire pour vous ?',
                'quickReplies': True,
            },
                response=convs[intent] if is_empty(entitiz) else convs[intent][entity_value],
                intent=intent,
                entity=entitiz,
                image={
                    'type': 'image',
                    'img_url': images[intent]
                })
            return json_object, 200, {'Access-Control-Allow-Origin': '*',
                                      'Content-Type': 'application/json', }

        else:
            json_object = {'response': 'Sorry i didn\'t understand you !!'}
            return json_object, 200, {'Access-Control-Allow-Origin': '*'}

    @staticmethod
    def delete(conv_id):
        abort_if_conv_doesnt_exist(conv_id)
        del convs[conv_id]
        return '', 204

    @staticmethod
    def put(conv_id):
        args = parser.parse_args()
        intent = {'intent': args['intent']}
        convs[conv_id] = intent
        return intent, 201


api.add_resource(Conversation, '/convs')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
