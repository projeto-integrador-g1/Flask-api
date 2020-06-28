import urllib.request, json, time, urllib, os.path
from pathlib import Path
from urllib.error import HTTPError
from pymongo import MongoClient
import socket
import errno
import sys
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)

db = client['metadata']
collection_currency = db['landsat']




column = sys.argv[1]





rows = ['057','058','059','060','061','062','063','064','065','066','067','068','069','070','071','072','073','074','075','076','077','078','079','080','081','082','083']
i = 1
for row in rows:
        rowlink = f"https://landsat-stac.s3.amazonaws.com/landsat-8-l1/{column}/{row}/catalog.json"
        #print(rowlink)
        salvar=True
        while(True):
            try:
                rowdata = urllib.request.urlopen(rowlink)
                break
            except HTTPError as err:
                if err.code == 404:
                    salvar=False
                    print(rowlink)
                    print('404 Row')
                    break
            except ConnectionResetError:
                print('Falhou Row Reset')
            except socket.error as error:
                print('Falhou Row Socket')
        if salvar == True:
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
                        print('Falhou Final Reset')
                    except socket.error as error:
                        print('Falhou Final Socket')
                    
                if salvar == True:
                    savedata = json.loads(savedata.read())
                    savedata['_id'] = savedata['id']
                    del savedata['id']
                    #with open('json_dump/'+ idfinal[11:], 'w') as fp:
                    #    json.dump(savedata, fp)
                    collection_currency.insert(savedata)
                    #print(i)
                    i = i + 1
client.close()