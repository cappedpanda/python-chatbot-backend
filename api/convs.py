# -*- coding: utf-8 -*-


import requests
from flask import Flask, request, json
from flask_restful import (Resource, Api, reqparse)
from api.db import DB, save
from api.models import NluObjectWithEntity, NluObjectSimple

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('intent', 'entity')


def is_empty(structure):
    if len(structure) == 0:
        return True
    else:
        return False


class Conversation(Resource):

    # POST Method built
    @staticmethod
    def post():

        global entitiz, nlu2, nlu

        # -- NLP treatment --

        # Input body composition
        data = request.get_json()

        body = dict({
            'query': data['msg'],
            'nlp-address': data['nlp-url'],
            'collection-name': data['collection']
        })

        # NLU post request
        intent = requests.post(url=body['nlp-address'], data=json.dumps(dict({'query': body['query']})))
        entity = requests.post(url=body['nlp-address'], data=json.dumps(dict({'query': body['query']})))
        text = requests.post(url=body['nlp-address'], data=json.dumps(dict({'query': body['query']})))
        date = intent.headers['Date']

        # Database class using
        db = DB()
        db.Collection = body['collection-name']
        db.init()

        # Extracting Intent and Entity
        intent = intent.json()['intent']['name']
        intent_confidence = entity.json()['intent']['confidence']
        entity_array = entity.json()['entities']

        # Implement entity array into list
        length = len(entity_array)
        i = 0
        entitiz = list()
        while i != length:
            entitiz.append(entity_array[i]['value'])
            i = i + 1

        text = text.json()['text']

        # Checking if the entity is none
        if not is_empty(entitiz):
            nlu2 = NluObjectWithEntity(body['collection-name'], intent, entitiz[0], response=None)
        nlu = NluObjectSimple(body['collection-name'], intent, response=None)

        # Saving request informations

        saves = dict(date=date, text=text, intent=intent, intent_confidence=intent_confidence, entities=entity_array)
        save(saves)

        # Sending Json Object with Headers & Response
        if nlu.find:
            json_object = dict({
                'success': 'Message sent with success',
                'text': text,
                'msg-type': 'text',
                'bot': dict(response=nlu.find_response if is_empty(entitiz) else nlu2.find_response,
                            quickReplies=True, quicks=["congé", "contrats", "obligation patronale"])
            })

            return json_object, 200, {'Access-Control-Allow-Origin': '*',
                                      'Content-Type': 'application/json'}

        else:
            json_object = {'response': 'Pouvez-vous mieux préciser ce vous voulez dire ??'}
            return json_object, 400, {'Content-Type': 'application/json'}
