from  flask import Response, request
from flask_restful import Resource
from satsearch import Search
from satstac import Item
import json
import requests

class CatRequest(Resource):
    def post(self):
        body = request.get_json()
        geom = {
            "type": "Polygon",
            "coordinates": [
            [
                #body["geo_coord"]
            ]
            ]
        }
        print(body)
        cloud = "eo:cloud_cover<" + "90"#body['cloud']
        time = "2018-02-01/2018-02-10"#body["time"]
        
        search = Search(intersects=geom,
                        #time=time,
                        property=[cloud])
        items = search.items()

        #for item in items:
            #print(item.assets["thumbnail"]["href"])
        return 200

