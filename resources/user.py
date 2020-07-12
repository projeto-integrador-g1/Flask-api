from  flask import Response, request
from database.model import User
from flask_restful import Resource
import smtplib
from pymongo import MongoClient
client = MongoClient('mongodb+srv://piAdmin:pi1234@cluster0-vpcqm.gcp.mongodb.net/test?retryWrites=true&w=majority', 27017)
user_email = ""
db = client['test']
collection_currency = db['user']

class UsersApi(Resource):
    #Get all users
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)
    #Register an user
    def post(self):
        body = request.get_json()
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 200

class UserApi(Resource):
    #Tries to get an specific user by id
    
    def post(self):
        global user_email
        body = request.get_json()
        print(body['email'])
        user_email = body['email']
        return 200
    def get(self):
        try:
            global user_email
            email = user_email
            print('teoricamente sapoha tá cheia' + email)
            user = collection_currency.find({"user_email": email})
            for us in user:
                resp = us
            test = {}
            test['user_imgs'] = resp['user_imgs']
            return test, 200
        except:
            return Response("User not Found", status=500)
    #Update selected user
    def put(self, id):
        try:
            body = request.get_json()
            User.objects.get(id=id).update(**body)
            return '', 200
        except:
            return Response("User not Found", status=500)
    #Deletes selected user
    def delete(self, id):
        try:
            User.objects.get(id=id).delete()
            return 'User Removed', 200
        except:
            return Response("User not Found", status=500)
    

def getEmail():
    global user_email
    return user_email

class RecoverAPI(Resource):
    def get(self, id):
        try:
            user = User.objects.get(id=id).to_json()
            sender = 'email@email.com'
            link = "password recover front"
            receivers = user['user_email']
            message = f"""From: From Person {sender}
                    To: To Person {receivers}
                    MIME-Version: 1.0
                    Content-type: text/html
                    Subject: Recuperação senha

                    link para recuperação de senha :
                    {link}

                    <b>This is HTML message.</b>
                    <h1>This is headline.</h1>
                    """
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)         
            return Response("", status=200)
        except:
            return Response("User not Found", status=500)
    def post(self):
        body = request.get_json()
        #add JWT features