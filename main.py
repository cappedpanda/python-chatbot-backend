import os

from api.convs import *
from api.init import *
from flask_cors import CORS

static_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
api = Api(app)

CORS(app)

if __name__ == '__main__':
    api.add_resource(Initiation, '/init')
    api.add_resource(Conversation, '/ask')
    app.run(host='0.0.0.0', debug=True)
