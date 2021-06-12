# app.py

# Required imports
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func
from flask import Flask, request, jsonify, make_response, render_template, url_for, redirect
from flask_restful import Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from firebase_admin import credentials, firestore, initialize_app
from server.src.user import User
from datetime import datetime, timedelta
from functools import wraps

# Initialize Flask app
app = Flask(__name__,template_folder='templates')
api = Api(app)
app.config['SECRET_KEY'] = 'fintechfinal'
app.config["JWT_TOKEN_LOCATION"] = ['cookies']
app.config["JWT_COOKIE_SECURE"] = False
jwt = JWTManager(app)

# api.add_resource(Users,'/all-users')
# api.add_resource(User,'/user')

@app.route('/')
def index():
    return render_template('Home.html')

@app.route('/login', methods =['POST', 'GET'])
def login():
    if request.method == 'GET' :
        return render_template('Login.html')
    else:
        # creates dictionary of form data
        auth = request.get_json()
        if not auth or not auth.get('username') or not auth.get('password'):
            # returns 401 if any username or / and password is missing
            return make_response('Username or Password missing',401, {'WWW-Authenticate' : 'Basic realm ="Login required !!"'})
    
        user = User()
        
        if not user:
            # returns 403 if user does not exist
            return make_response("User Not Found",403, {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'})
    
        if (user.username == auth.get('username') and user.password == auth.get('password')):
            # generates the JWT Token
            access_token = create_access_token(identity=user.username)
            response = jsonify(access_token=access_token)
            set_access_cookies(response, access_token)
            return response

        # returns 403 if password is wrong
        return make_response('Wrong Username or Password',403, {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'})

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/ticket', methods=["GET","POST"])
@jwt_required()
def ticket():
    return render_template('ticket.html')

@app.route('/ticket_info', methods=["GET","POST"])
@jwt_required()
def ticket_info():
    return render_template('ticket_info.html')

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