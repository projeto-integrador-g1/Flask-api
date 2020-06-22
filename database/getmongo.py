import urllib.request, json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['metadata']
collection_currency = db['landsat']

# def getImages(date, satelite, cloudCouverage, geo_coord):
#     i = 1
#     info = {1:{'collection': '','scene_id': '','datetime': '','cloud_cover': '' ,'column': '','row': '', 'href': ''}}
#     cursor = collection_currency.find({})
#     for document in cursor:
#         if "010/022" in document['links'][0]['href'] and int(document['properties']['eo:cloud_cover']) < 20:
#             info[i] = {}
#             info[i]['collection'] = document['properties']['collection']
#             info[i]['scene_id'] = document['properties']['landsat:scene_id']
#             info[i]['datetime'] = document['properties']['datetime']
#             info[i]['geo_coord'] = document['geometry']['coordinates']
#             info[i]['cloud_cover'] = document['properties']['eo:cloud_cover']
#             info[i]['column'] = document['properties']['eo:column']
#             info[i]['row'] = document['properties']['eo:row']

#             with urllib.request.urlopen(document['links'][0]['href']) as url:
#                 data = json.loads(url.read().decode())
#                 #print(data['assets']['thumbnail']['href'])
#                 info[i]['href'] = data['assets']['thumbnail']['href']
#                 i = i + 1
#                 with open("test.txt", "a") as myfile:
#                     myfile.write(data['assets']['thumbnail']['href'] + "\n")
#     #print(info)
#     return info
#     with open("my.json","w") as f:
#         json.dump(info,f)

# def getImages(date, satelite, cloudCouverage, geo_coord):
#     ano_inicio, mes_inicio, dia_inicio = date[0].split('-')
#     ano_fim, mes_fim, dia_fim = date[1].split('-')
#     inicio = datetime(int(ano_inicio), int(mes_inicio), int(dia_inicio))
#     fim = datetime(int(ano_fim), int(mes_fim), int(dia_fim))
#     cursor = collection_currency.find({ "properties.datetime": {'$gt':inicio, '$lt': fim },
#                                         "properties.eo:cloud_cover": {'$lte': cloudCouverage}
#                                         })
#     for document in cursor:
#         print(document)

def getImages(date, satelite, cloudCouverage, geo_coord):
    coord = []
    for points in geo_coord:
        x , y = points.split(",")
        x = float(x)
        y = float(y)
        coord.append([y, x])
    print(coord)
    cursor = collection_currency.find({ "geometry.coordinates": {
                                                                "$geoIntersects": {
                                                                    "$geometry": {
                                                                        "type": "Polygon" ,
                                                                        "coordinates": [coord]
                                                                    }
                                                                }
        }
    })
    for document in cursor:
        print(document)