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
    userlist = ref.get()
    if username in userlist:
        return (password == userlist[username]['password'] , username)



def getData(data,method):
    ref = db.reference("/")
    if method == 'login':                   #to login , data = {auth}
        ref = db.reference("/userAccount")
        return checkLogin(data,ref)
    
   
    elif method == 'checkTicket':   #check if ticket has been bought , data = {username,event} , returns true if bought before
        username = data['username']
        eventName = data['event']
        ref = db.reference("/userAccount/"+username+"/tickets")
        if ref.get() != None:
            for ticket in ref.get().keys():
                if eventName == ticket:
                    return True
            return False
        else:                             #not any ticket has been bought yet
            return False
    else:
        return "undefined method"
    


def setData(data,method):
    if method == "addTicket":       #data = {username , qrcode, event, ticket_type}
        ref = db.reference("/userAccount/"+data['username']+"/tickets/"+data['event'])
        data.pop('username')
        data.pop('event')
        ref.update(data)



def generate_data():
    cred_obj = firebase_admin.credentials.Certificate('firebase_key/fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
    default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://fintech-61df3-default-rtdb.firebaseio.com/'
	})
    ref = db.reference("/userAccount")
    ref.child('raccoon').set({'password' : 'smart'})
    ref.child('gahua').set({'password' : 'corgi87'})
    ref.child('test').set({'password' : 'test'})
    ref.child('gahua').update({
    'nickname': 'CORGI'
        })

    print(ref.get())
    print(ref.get()['gahua']['password'])
    ref = db.reference("aaa")
    print(ref.get() != None)


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