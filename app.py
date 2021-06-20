# app.py

# Required imports
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect, flash
from flask_restful import Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime, timedelta
from functools import wraps

#firebase-python
from server.src import py_firebase

# 藍星api
from datetime import time
import time
from server.src.Crypto import *

# qrcode
from server.src import QRcode


# Initialize Flask app
app = Flask(__name__,template_folder='templates',static_url_path='')
api = Api(app)
app.config['SECRET_KEY'] = 'fintechfinal'
app.config["JWT_TOKEN_LOCATION"] = ['cookies']
app.config["JWT_COOKIE_SECURE"] = False
jwt = JWTManager(app)

py_firebase.init()

# api.add_resource(Users,'/all-users')
# api.add_resource(User,'/user')

#未授權的路由請求會重新導向至登入頁面 
@jwt.unauthorized_loader
def custom_unauthorized_response(_err):
    flash("請先登入")
    return redirect(url_for('login'))

# 連線逾時會重新導向到登入頁面
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    flash("連線逾時，請重新登入")
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/home')
@jwt_required()
def home():
    user = get_jwt_identity()
    return render_template('Home.html', user=user)

@app.route('/login', methods =['POST', 'GET'])
def login():
    if request.method == 'GET' :
        return render_template('Login.html')
    else:
        # get json data from request
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            # returns 401 if any username or / and password is missing
            return make_response('Username or Password missing',401, {'WWW-Authenticate' : 'Basic realm ="Login required !!"'})

        ##compare auth.get('username') with firebase here
        (log_success,username) = py_firebase.getData(auth,'login')

        if log_success:
            # generates the JWT Token
            access_token = create_access_token(identity=username)
            response = jsonify(access_token=access_token)
            set_access_cookies(response, access_token)
            return response
        else:
            return make_response('Wrong Username or Password',403, {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'})

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/ticket', methods=["GET","POST"])
@jwt_required()
def ticket():
    title = request.args.get("title")
    user = get_jwt_identity()
    return render_template('ticket.html',user=user,title=title)

@app.route('/ticket_info_1', methods=["GET","POST"])
@jwt_required()
def ticket_info_1():
    user = get_jwt_identity()
    data = {
        "username" : user,
        "event" : "文藝復興"
    }
    check = py_firebase.getData(data,"checkTicket")
    return render_template('ticket_info_1.html',user=user,check=check,data=data)

@app.route('/ticket_info_2', methods=["GET","POST"])
@jwt_required()
def ticket_info_2():
    user = get_jwt_identity()
    data = {
        "username" : user,
        "event" : "演唱會"
    }
    check = py_firebase.getData(data,"checkTicket")
    return render_template('ticket_info_2.html',user=user,check=check,data=data)

@app.route('/ticket_info_3', methods=["GET","POST"])
@jwt_required()
def ticket_info_3():
    user = get_jwt_identity()
    data = {
        "username" : user,
        "event" : "粽協"
    }
    check = py_firebase.getData(data,"checkTicket")
    return render_template('ticket_info_3.html',user=user,check=check,data=data)

@app.route('/cart', methods=["GET","POST"])
@jwt_required()
def cart():
    data = {
        "MerchantID":"MS121046056",
        "RespondType":"JSON",
        "TimeStamp": str(int(time.time())),
        "Version":"1.6",
        "MerchantOrderNo":"S_"+str(int(time.time())),
        "Amt":"2400",
        "ItemDesc":"BACK TO 70’S 西洋金曲演唱會",
        "Email":"s24527109@gmail.com",
        "LoginType":"0"
    }
    parse_data = gen_query_string(data)
    trade_info = create_mpg_aes_encrypt(parse_data.encode())
    trade_sha = create_mpg_sha_encrypt(trade_info)

    user = get_jwt_identity()
    return render_template('cart.html',user=user,trade_info=trade_info,trade_sha=trade_sha)

@app.route('/myticket', methods=["GET","POST"])
@jwt_required()
def myticket():
    if request.method == 'GET' :
        return render_template('qrcode.html')
    else:
        data = request.get_json()
        qrcode = data.get('qrcode')
        event = data.get('event')
        ticket_type = data.get('ticket_type')
        username = get_jwt_identity()
        json = {'qrcode':qrcode , 'event':event , 'ticket_type': ticket_type , 'username':username}
        py_firebase.setData(json,"addTicket")

@app.route('/qrcode', methods=["GET","POST"])
@jwt_required()

def qrcode():
    user = get_jwt_identity()
    #QRcode.QRcode()
    #img_path = QRcode.qrPath()
    return render_template('qrcode.html',user=user)
    

# 以下註解部分為google官方提供的code
# @app.route('/add', methods=['POST'])
# def create():
#     """
#         create() : Add document to Firestore collection with request body.
#         Ensure you pass a custom ID as part of json body in post request,
#         e.g. json={'id': '1', 'title': 'Write a blog post'}
#     """
#     try:
#         id = request.json['id']
#         todo_ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/list', methods=['GET'])
# def read():
#     """
#         read() : Fetches documents from Firestore collection as JSON.
#         todo : Return document that matches query ID.
#         all_todos : Return all documents.
#     """
#     try:
#         # Check if ID was passed to URL query
#         todo_id = request.args.get('id')
#         if todo_id:
#             todo = todo_ref.document(todo_id).get()
#             return jsonify(todo.to_dict()), 200
#         else:
#             all_todos = [doc.to_dict() for doc in todo_ref.stream()]
#             return jsonify(all_todos), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/update', methods=['POST', 'PUT'])
# def update():
#     """
#         update() : Update document in Firestore collection with request body.
#         Ensure you pass a custom ID as part of json body in post request,
#         e.g. json={'id': '1', 'title': 'Write a blog post today'}
#     """
#     try:
#         id = request.json['id']
#         todo_ref.document(id).update(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

# @app.route('/delete', methods=['GET', 'DELETE'])
# def delete():
#     """
#         delete() : Delete a document from Firestore collection.
#     """
#     try:
#         # Check for ID in URL query
#         todo_id = request.args.get('id')
#         todo_ref.document(todo_id).delete()
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1',port=5000)