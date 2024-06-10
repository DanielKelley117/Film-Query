import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from credentials import *

# Use a service account.
#cred = credentials.Certificate('warmup-project-cs3050-0c4ff5204787.json')

#app = firebase_admin.initialize_app(cred)

#db = firestore.client()
get_credentials()

#Gather User input 
JSON_filename = input("Enter the name of the JSON file: ")

f = open(JSON_filename)
# returns JSON object as
# a dictionary
data = json.load(f)

for object in data:
    doc_ref = db.collection("Movies").document(object["Release"])
    rank = object["Rank"]
    release = object["Release"]
    max_theaters = object["max_th"]
    opening = object["Opening"]
    perc_tot_gr = object["perc_tot_gr"]
    opening_theaters = object["open_th"]
    opening_date = object["Open"]
    closing_date = object["Close"]
    distributor = object["Distributor"]
    gross = object["GrossValues"]
    
    doc_ref.set({"rank": rank, "release": release, "maxTheaters": max_theaters, "open": opening, "percentTotalGross": perc_tot_gr, "openingTheaters": opening_theaters, "openDate": opening_date, "closingDate": closing_date, "distributor": distributor, "gross": gross})