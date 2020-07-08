from  flask import Response, request
from flask_restful import Resource
from database.model import User
from database.getmongo import getImages, getToAi
from flask import jsonify
import shapefile as shp
from osgeo import ogr
import os
import json
import requests
from pymongo import MongoClient
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['test']
collection_currency = db['geo_info']

coord = []
antcoord = []

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
        print(coord)
        r = getImages(body["date"], body["satelite"], body["cloudCouverage"], body["geo_coord"])
        return r,200
    

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

class AIRequest(Resource):
    #make requests to AI
    def post(self):
        body = request.get_json()
        req = body['images']
        r = getToAi(req)
        global coord, antcoord
        antcoord = coord
        print (coord)
        if not coord:
            coord = antcoord
        r.insert(0, coord)
        retorno = requests.post('http://127.0.0.1:8922/ia', json=r)
        del coord[:]
        return Response('', status=200)
    def get(self):
        pload = {'_id':'1234567','Satus':'Done'}
        r = requests.post('front url',data = pload)
        return 200

class SHPFile(Resource):
    def post(self):
        body = request.values
        daShapefile = r"C:\Users\mathe\layers\POLYGON.shp"
        driver = ogr.GetDriverByName('ESRI Shapefile')

        dataSource = driver.Open(daShapefile, 0) # 0 means read-only. 1 means writeable.
        # Check to see if shapefile is found.
        if dataSource is None:
            print ('Could not open %s' % (daShapefile))
        else:
            print ('Opened %s' % (daShapefile))
            layer = dataSource.GetLayer()
            featureCount = layer.GetFeatureCount()
            print ("Number of features in %s: %d" % (os.path.basename(daShapefile),featureCount))
        return Response([], 200)