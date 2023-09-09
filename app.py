from flask import Flask, request, jsonify
from flask_cors import cross_origin
import json
from hashlib import sha256

app = Flask(__name__)


@app.route('/test', methods=['POST'])
@cross_origin()
def getHash():
    f = request.json
    return sha256(f['text'])

if __name__ == '__main__':
    app.run(debug=True)
