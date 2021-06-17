import firebase_admin
from firebase_admin import db
import json

cred_obj = None
default_app = None

def init():
    cred_obj = firebase_admin.credentials.Certificate('firebase_key/fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://fintech-61df3-default-rtdb.firebaseio.com/'
	})



def checkLogin(auth,ref):
    username = auth.get('username')
    password = auth.get('password')
    for account in ref.get().values():
        if username in account:
            return (password == account[username] , username)



def getData(auth,method):
    ref = db.reference("/")
    if method == 'login':
        ref = db.reference("/userAccount")
        return checkLogin(auth,ref)
    else:
        return "undefined method"



def generate_data():
    cred_obj = firebase_admin.credentials.Certificate('firebase_key/fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://fintech-61df3-default-rtdb.firebaseio.com/'
	})
    ref = db.reference("/userAccount")
    ref.push({'raccoon':'smart'})
    ref.push({'gahua':"corgi87"})
    ref.push({'deptmis':'deptmis'})
    ref.push({'test':'test'})


#generate_data()

"""
cred_obj = firebase_admin.credentials.Certificate('firebase_key/fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://fintech-61df3-default-rtdb.firebaseio.com/'
	})
ref = db.reference("/userAccount")
#ref.push({'test':'test'})
#print( )
print( ref.get().values())
#print("gahua" in ref.get().values())

for i in ref.get().values():
    print("gahua" in i)
    print("corgi87" == i['gahua'])
"""