import firebase_admin
from firebase_admin import db
import json

cred_obj = None
default_app = None


"""
使用前請確認有先在app.py跑過一次py_firebase.init()

方法:
getData(data,method):主要用於從資料庫取得資料，data為索引(格式為json/字典)，method為要做的事情(格式為字串)
    method = "login" : 用於登入，data = {'username' , 'password'}
                                回傳:布林值

    method = "checkTicket" : 用於驗證某活動的票卷是否已經買過，data = {'username' , 'event'}
                            回傳: 布林值

    method = "getTicketInfo" : 用於取得某使用者的票卷購買詳細資訊，data = {'username' , ('event'可給可不給) }
                                回傳: {'QRcode', 'orderID', 'qrcode', 'ticket_type'}
                                    {'event': {'QRcode', 'orderID', 'qrcode', 'ticket_type'} ,...} if no event sent


setData(data,method):主要用於送給資料庫資料，data為索引(格式為json/字典)，method為要做的事情(格式為字串)
    method = "addTicket" : 用於新增票卷(家華)，data = {username , oriderID, event, ticket_type}
    method = "generateQR" : 以orderID產生QRcode，data = {username , orderID , QRcode}


"""









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

    elif method =="getTicketInfo":
        username = data['username']
        ref = db.reference("/userAccount/"+username+"/tickets")
        ticketList = ref.get()
        if 'event' in data:         # has event name
            if data['event'] in ticketList:
                return ticketList[data['event']]
        else:
            return ticketList
        
    else:
        return "undefined method"
    


def setData(data,method):
    if method == "addTicket":       #data = {username , oriderID, event, ticket_type}
        ref = db.reference("/userAccount/"+data['username']+"/tickets/"+data['event'])
        data.pop('username')
        data.pop('event')
        ref.update(data)
    
    if method == "generateQR":      #data = {username , orderID , QRcode}
        ref = db.reference("/userAccount/"+data['username']+"/tickets/")
        ticketList = ref.get()
        for (tickey,ticval) in ticketList.items():
            if ticval['orderID'] == data['orderID']:
                temp = data.pop('QRcode')
                ref = ref.child(tickey)
                ref.update({"QRcode":temp})
                break


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

