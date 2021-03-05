#!flask/bin/python
# -- coding: utf-8 --

from flask import Flask, jsonify
from flask import request as req
import os

import requests
import json

app = Flask(__name__)
APP_VERSION = 5
@app.route('/', methods=['GET', 'POST'])
def index():
    args = req.json
    if args != None:
        i = args.get("index", 0)
    else:
        i = 0
    NEXT_SERVICE = os.environ.get("NEXT_SERVICE", None)

    if NEXT_SERVICE == None:
        return jsonify(dict(index=i+1, version=APP_VERSION))
    else:
        resp = requests.post("http://%s:8080/" % NEXT_SERVICE, data=dict(index=i, version=APP_VERSION))
        if resp.ok:
            resp_json = resp.json()
            resp_json["index"] = resp_json["index"] + 1
            return jsonify(resp_json)
        else:
            return jsonify(dict(index=i+1, error="Next service error", version=APP_VERSION))

if __name__ == '__main__':
    ERROR_FLAG = os.environ.get("ERROR_FLAG")
    if ERROR_FLAG != None:
        raise Exception("Bingo! - %s" % APP_VERSION)
    app.run(host='0.0.0.0', port=8080, debug=True)



