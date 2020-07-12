import urllib.request, json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['metadata']
collection_currency = db['landsat']



def getImages(date, satelite, cloudCouverage, geo_coord):
    coord = []
    for points in geo_coord:
        x , y = points.split(",")
        x = float(x)
        y = float(y)
        coord.append([y, x])
    #print(coord)
    dt1 = datetime.strptime(date[0], "%Y-%m-%d")
    dt2 = datetime.strptime(date[1], "%Y-%m-%d")
    if dt1 > dt2:
        inicio = date[0]
        fim = date[1]
    else:
        inicio = date[1]
        fim = date[0]
    #inicio = date[0]
    #fim = date[1]
    cursor = collection_currency.find({ "geometry": {
                                                                "$geoIntersects": {
                                                                    "$geometry": {
                                                                        "type": "Polygon" ,
                                                                        "coordinates": [coord]
                                                                    }
                                                                }
        },
        "properties.eo:cloud_cover": {'$lte': cloudCouverage},
        "properties.datetime": {'$gt':fim, '$lt': inicio }
    })
    print(inicio)
    print(fim)
    info = {1:{'collection': '','scene_id': '','datetime': '','cloud_cover': '' ,'column': '','row': '', 'href': ''}}
    i=1
    for document in cursor:
        info[i] = {}
        info[i]['collection'] = document['properties']['collection']
        info[i]['scene_id'] = document['properties']['landsat:scene_id']
        info[i]['datetime'] = document['properties']['datetime']
        info[i]['geo_coord'] = document['geometry']['coordinates']
        info[i]['cloud_cover'] = document['properties']['eo:cloud_cover']
        info[i]['column'] = document['properties']['eo:column']
        info[i]['row'] = document['properties']['eo:row']
        info[i]['href'] = document['assets']['thumbnail']['href']
        i = i+1
        #print("Column: " + document['properties']['eo:column'] + "Row: " + document['properties']['eo:row'] + " Cloud " + str(document['properties']['eo:cloud_cover'])+ "data" + str(document['properties']['datetime']))
    return info

def getToAi(req):
    items = []
    for item in req:
        print(type(item))
        cursor = collection_currency.find({"properties.landsat:scene_id": item})
        for document in cursor:
            items.append(document)
    
    return items
