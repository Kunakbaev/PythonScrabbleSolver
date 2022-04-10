
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('firebaseServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://russiannounsbase-default-rtdb.firebaseio.com/'
})

ref = db.reference("/")
def getData():
    with open('shortNouns.json', 'r', encoding='utf-8') as fd:
        jj = json.load(fd)
        l = []
        for key in jj:
            l.append(jj[key])
        return l
   #return ref.get()



