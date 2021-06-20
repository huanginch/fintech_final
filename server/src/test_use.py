
import py_firebase

#py_firebase.generate_data()
"""
data = request.get_json()
qrcode = data.get('qrcode')
event = data.get('event')
ticket_type = data.get('ticket_type')
username = get_jwt_identity()
"""
qrcode = "adbdfefwe"
event = "粽協"
username = 'gahua'
ticket_type = "搖滾區"


json = {'qrcode':qrcode , 'event':event , 'ticket_type': ticket_type , 'username':username}
#py_firebase.init()
py_firebase.generate_data()
"""
py_firebase.setData(json,"addTicket")
json2 = {'qrcode':"test2" , 'event':"test2" , 'ticket_type': "test2" , 'username':username}
py_firebase.setData(json2,"addTicket")
test = {'username':'gahua', 'event': "粽協"}
test2 = {'username':'gahua', 'event': "柯基跳舞秀"}

print(py_firebase.getData(test,"checkTicket"))
print(py_firebase.getData(test2,"checkTicket"))

"""