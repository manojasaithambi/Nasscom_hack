# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 12:40:36 2018

@author: Manoj
"""

from flask import Flask, request, jsonify
import json
from shutil import copyfile
import os
from os.path import basename
from label_image_mod import main

approot = os.path.dirname(os.path.abspath(__file__))+"\\"

app = Flask(__name__)

class ExceptionHandler(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        return rv

@app.errorhandler(ExceptionHandler)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/healthstatus', methods = ['GET'])
def getHealthstatus():
    return "service is executing"

@app.route('/image_recognition', methods = ['POST'])
def parseFile():
    req = request.json; 
    print(req)
    response = {}
    file = req['img']; print('input-->', file)
    #print(basename(file))
    #file.save(approot+'/input/'+basename(file))
    #print(file)
    response = ''
    try:
        resValues = main(file)
        response = {'status':1,'response':resValues}
    except ValueError as ve:
           print(ve) 
           response = {'status':0}
    
    response=json.dumps(response)
    print('output-->', response)
    return response
	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=6001,debug=True)