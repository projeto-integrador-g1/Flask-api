from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_routes
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'Cluster0',
    'host': 'mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority',
}

initialize_db(app)
initialize_routes(api)
app.run(host='127.0.0.1', port=4002)
