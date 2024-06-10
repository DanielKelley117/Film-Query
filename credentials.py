import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def get_credentials():
    cred = credentials.Certificate('warmup-project-cs3050-0c4ff5204787.json')

    app = firebase_admin.initialize_app(cred)

    #db = firestore.client()
    return firestore.client()
