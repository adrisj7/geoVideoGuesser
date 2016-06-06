#!/usr/bin/python
from flask import Flask, request, jsonify
from statGrabber import searchLocation, searchRandom
#from json import dumps as json_dump

web = Flask(__name__)

WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
MAX_SEARCH_RESULTS = 50


# THIS MAKES THE SITE ACCEPT ALL REQUESTS
#TODO: Make this safer.
# THIS IS UNSAFE. DON'T USE THIS FOR FUTURE PRACTICE
@web.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@web.route("/getMapData")
def getMapData():
    lat = float(request.args.get("latitude"))
    lng = float(request.args.get("longitude"))
    radius = request.args.get("radius")
    videoDictList = [searchLocation(lat,lng,radius)]
    result = dictifyList(videoDictList)
    return jsonify(**result)
    #return json_dump(statGrabber.searchLocation(lat,lng,radius,MAX_SEARCH_RESULTS))

@web.route("/getRandomVideo")
def getRandomVideo():
    videoDictList = [searchRandom()]
    result = dictifyList(videoDictList)
    return jsonify(**result) 

def dictifyList(l):
    return {str(i):l[i] for i in range(len(l))}

if (__name__ == "__main__"):
    web.debug = True
    web.run(host=WEB_HOST,port=WEB_PORT)
