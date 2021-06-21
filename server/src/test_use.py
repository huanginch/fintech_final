import py_firebase
qrcode = "adbdfefwe"
event = "粽協"
username = 'gahua'
ticket_type = "搖滾區"

py_firebase.init()
json = {'qrcode':qrcode , 'event':event , 'ticket_type': ticket_type , 'username':username}


json2 = {'qrcode':"test2" , 'event':"粽協" , 'ticket_type': "test2" , 'username':username}
py_firebase.setData(json2,"addTicket")
test = {'username':'gahua',"orderID" : "for test","QRcode": "RRR", 'event': "粽協"}
py_firebase.setData(test,"generateQR")
test2 = {'username':'gahua'}
print(py_firebase.getData(test2,"getTicketInfo"))
#print(py_firebase.getData(test,"checkTicket"))
#print(py_firebase.getData(test2,"checkTicket"))

