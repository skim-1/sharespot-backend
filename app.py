from flask import Flask, request, jsonify
from flask_cors import cross_origin
import json
from hashlib import sha256

app = Flask(__name__)

def import_logins():
    with open('./logins.json') as f:
        return json.load(f)

def dump_logins(injson):
    with open('./logins.json', 'w') as f:
        json.dump(injson, f)

def import_hash():
    with open('./hash.json') as f:
        return json.load(f)

def dump_hash(injson):
    with open('./hash.json', 'w') as f:
        json.dump(injson, f)


@app.route('/createlogin', methods=['POST'])
@cross_origin()
def createLogin():
    f = request.json
    logs = import_logins()

    try:

        for x in logs['user-ids']:
            if x['user email'] == f['user email']:
                return 'failed, account already exists'

        logs['user-ids'].append({'user email': f['user email'], 'user password': f['user password'], 'usbs': []})
        dump_logins(logs)
        return {"create_status": "success"}.headers.add('Access-Control-Allow-Origin', '*')
    except:
        return {"create_status": "failed"}


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    f = request.json

    logs = import_logins()

    for x in logs['user-ids']:
        if x['user email'] == f['user email']['username']:
            if x['user password'] == f['user password']['password']:
                return {"authentication_status": "success"}
            else:
                return {"authentication_status":"failed"}

    return {"authentication_status": "does not exist"}

@app.route('/ping', methods=['GET'])
@cross_origin()
def ping():
    return 'pong'

@app.route('/addusb', methods=['POST'])
@cross_origin()
def addusb():
    f = request.json
    usbs = import_hash()
    print(f)
    hash = sha256(str(len(usbs["hashes"])).encode('utf-8')).hexdigest()

    usbs["hashes"].append(
        {
            'hash': hash,
            'locations': [
                {
                    'location':f['location'],
                    'image':f['image'],
                    'text':f['text'],
                    'userid':f['userid']
                }],
        })

    users = import_logins()

    for x in users['user-ids']:
        if x['user email'] == f['user email']:
            users['usbs'].append(hash)

    dump_logins(users)
    dump_hash(usbs)

    return hash


@app.route('/addlocation', methods=['POST'])
@cross_origin()
def addlocation():
    f = request.json
    usbs = import_hash()


    try:
        for x in usbs["hashes"]:
            if x['hash'] == f['hash']:
                x['hash']['locations'].append(
                    {
                        'location':f['location'],
                        'image':f['image'],
                        'text':f['text'],
                        'userid':f['userid']
                    }
                )
            return 'error: usb not found'
    except:
        return 'error: add request failed'


@app.route('/getusbs', methods=['GET'])
@cross_origin()
def getusbs():
    usbs = import_hash()
    return usbs

@app.route('/getusb', methods=['POST'])
@cross_origin()
def getusb():
    f = request.json
    usbs = import_hash()
    try:
        for x in usbs["hashes"]:
            print('\n')
            if (x["hash"] == f["usb-hash"]):
                return x
        return {"status": "usb not found"}
    except:
        return {"status": "post request not successful"}

if __name__ == '__main__':
   app.run(debug=True)
    ##app.run("0.0.0.0")
