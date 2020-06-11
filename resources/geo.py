from  flask import Response, request
from flask_restful import Resource
from database.model import GeoInfo, User
import json
import requests

class GeoRequest(Resource):
    ## Will get and save geo location requested by the user 
    # that will be processed by the AI
    def post(self):
        body = request.get_json()
        geo = GeoInfo(**body).save()
        id = geo.id
        r = request.post('http://127.0.0.1:8922/ia/', json={"key": "value"})
        r.status_code
        r.json(body)
        return {'Request id': str(id)}, 200
    #Return all requests made to the AI
    def get(self):
        geo = GeoInfo.objects().to_json()
        return Response(geo, mimetype="application/json", status=200)

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