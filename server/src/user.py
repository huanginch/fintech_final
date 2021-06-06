from flask_restful import Resource, reqparse
from firebase_admin import credentials, firestore, initialize_app
import traceback
from flask import Flask, request, jsonify


# Initialize Firestore DB
# cred = credentials.Certificate('fintech-61df3-firebase-adminsdk-4vr8z-629365b6cf.json')
# default_app = initialize_app(cred)
# db = firestore.client()
# todo_ref = db.collection('todos')

class User(Resource):
    user_id = "123"
    username = "test"
    password = "test"