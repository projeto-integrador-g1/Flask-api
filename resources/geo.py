from  flask import Response, request
from flask_restful import Resource
from database.model import User
import json
import requests
from pymongo import MongoClient
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['test']
collection_currency = db['geo_info']

class GeoRequest(Resource):
    ## Will get and save geo location requested by the user 
    # that will be processed by the AI
    def post(self):
        body = request.get_json()
        #geo = GeoInfo(**body).save()
        #id = geo.id
        #r = request.post('http://127.0.0.1:8922/ia/', json={"key": "value"})
        #r.status_code
        #r.json(body)
        body.save('test.json')
        with open('test.json') as json_file:
            file_data = json.load(json_file)
        collection_currency.insert(file_data)
        client.close()
        return {'Sucess'}, 200
    #Return all requests made to the AI

        
class GeoSaveImage(Resource):
    ## Will get and save the processed image to the specifc user
    def post(self):
        body = request.get_json()
        user = User.objects.get(id=body['user_id']).to_json()
        print(body)
        print(user)
        user = user[46:]
        user = '{' + user
        print(user)
        userjson = json.loads(user)
        print(userjson)
        userjson['user_imgs'] = str(userjson['user_imgs']) + str(body['user_imgs']) + ';'
        User.objects.get(id=body['user_id']).update(**userjson)
        return Response('', status=200)