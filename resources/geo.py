from  flask import Response, request
from flask_restful import Resource
from database.model import User
from database.getmongo import getImages, getToAi
from flask import jsonify
#import shapefile as shp
from .user import getEmail
import os, io
import json
import fiona
import rasterio
import rasterio.mask
from zipfile import ZipFile
import requests
from pymongo import MongoClient
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['test']
collection_currency = db['geo_info']

coord = []
antcoord = []
email = ''

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
        with open('result.json', 'w') as fp:
            json.dump(body, fp)
        with open('result.json') as f:
            file_data = json.load(f)
        collection_currency.insert(file_data)
        client.close()
        global coord
        for points in body["geo_coord"]:
            x , y = points.split(",")
            x = float(x)
            y = float(y)
            coord.append([y, x])
        #print(coord)
        r = getImages(body["date"], body["satelite"], body["cloudCouverage"], body["geo_coord"])
        return r,200
    
def geoSaveImage(email,addlinks):
    local = client['test']
    collection = local['user']
    users = collection.find({"user_email": email})
    newlinks = ""
    for item in users:
        user = item
    for item in user["user_imgs"]:
        newlinks = newlinks + item + ";"
    for item in addlinks:
        newlinks = newlinks + item + ";"
    myquerry = {"user_email": email}
    newvalues = {"$set": {"user_imgs": newlinks}}
    collection.update_one(myquerry, newvalues)

    




class AIRequest(Resource):
    #make requests to AI
    def post(self):
        body = request.get_json()
        req = body['images']
        r = getToAi(req)
        print(r)
        global coord, antcoord
        print (coord)
        if not coord:
            coord = antcoord
        else:
            antcoord = coord
        r.insert(0, coord)
        coord = []
        retorno = requests.post('http://127.0.0.1:8922/ia', json=r)
        retornodata= retorno.json()
        print(retornodata)
        email = getEmail()
        geoSaveImage(email, retornodata['links'])
        return retornodata, 200
    def get(self):
        pload = {'_id':'1234567','Status':'Done'}
        r = requests.post('front url',data = pload)
        return 200

class SHPFile(Resource):
    def post(self):
        filezip = request.files
        print(filezip['file'])
        filezip['file'].save("file.zip")
        file_name = "file.zip"
        vet = []
        with ZipFile(file_name, 'r') as zip:
            zip.printdir()
            print('aew caralho')
            zip.extractall()
            print('foi')
        for file in os.listdir('./layers'):
            if file.endswith('.shp'):
                with fiona.open(os.path.join("./layers", file), "r") as shapefile:
                    shapes = [feature["geometry"] for feature in shapefile]
                for coord in shapes[0]['coordinates'][0]:
                    vet.append(coord[0])
                    vet.append(coord[1])
                #vet = shapes[0]['coordinates'][0]
        for file in os.listdir('./layers'):
            os.remove(os.path.join("./layers", file))
        print(vet)
        env = {}
        env['geo_coord'] = vet
        return env, 200