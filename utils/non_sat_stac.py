import urllib.request, json, time, urllib, os.path
from pathlib import Path
from urllib.error import HTTPError
from pymongo import MongoClient
import socket
import errno
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['metadata']
collection_currency = db['landsat']


with open('catalog.json') as f:
    file_data = json.load(f)

file_data = file_data["links"]
i=1
for item in file_data[4::]:
    #print(item["href"])
    column = item["href"][:3]

    columnlink = f"https://landsat-stac.s3.amazonaws.com/landsat-8-l1/{column}/catalog.json"
    #print(columnlink)
    while(True):
        try:
            columndata = urllib.request.urlopen(columnlink)
            break
        except:
            print('Falhou Column')
    data = json.loads(columndata.read())
    
    data = data["links"]
    for item2 in data[3::]:
        row = item2["href"][:3]
        rowlink = f"https://landsat-stac.s3.amazonaws.com/landsat-8-l1/{column}/{row}/catalog.json"
        #print(rowlink)
        while(True):
            try:
                rowdata = urllib.request.urlopen(rowlink)
                break
            except:
                print('Falhou Row')
        data2 = json.loads(rowdata.read())
        data2 = data2["links"]
        for item3 in data2[3::]:
            salvar=True
            idfinal = item3["href"]

            finallink = f"https://landsat-stac.s3.amazonaws.com/landsat-8-l1/{column}/{row}/{idfinal}"
            while(True):
                try:
                    savedata = urllib.request.urlopen(finallink)
                    break
                except HTTPError as err:
                    if err.code == 404:
                        salvar=False
                        print('404' + idfinal[11:])
                        break
                except ConnectionResetError:
                    print('Falhou Final')
                except socket.error as error:
                    print('Falhou Final')
                
            if salvar == True:
                savedata = json.loads(savedata.read())
                savedata['_id'] = savedata['id']
                del savedata['id']
                #with open('json_dump/'+ idfinal[11:], 'w') as fp:
                #    json.dump(savedata, fp)
                collection_currency.insert(savedata)
                print(i)
                i = i + 1
client.close()