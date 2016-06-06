#!/usr/bin/python

# This grabs relevant map data for determining whether or not a location is
# viable

from PIL import Image

import math
import numpy
#from urllib import urlopen # Alternatively, one can use the requests library
import requests
from cStringIO import StringIO

API_KEY = "AIzaSyC3tbVdhbQsl76YEANr6t585tYSw-Lteec"
RGB_TOLERANCE = 50

RGB_WATER = [179, 207, 255]

def getImageFromURL(url):
    #f = StringIO(urlopen(url).read()) 
    response = requests.get(url)
    f = StringIO(response.content)
    image = Image.open(f,'r')
    return image

def getRGB(image,x,y):
    #pixels = image.load()
    #pixels = numpy.array(image)
    #pixels = list(image.getdata())
    pixels = image.convert('RGB')
    r, g, b = pixels.getpixel((x,y))
    return r, g, b

def getRGBDiff(r1, g1, b1, r2, g2, b2):
    return math.sqrt(
        (r1 - r2)**2 + 
        (g1 - g2)**2 +
        (b1 - b2)**2
        )

def getPositionImage(lng,lat,width,height,zoom):
    url = \
    "http://maps.googleapis.com/maps/api/staticmap?center=%f,%f&size=%dx%d&zoom=%d&maptype=roadmap&sensor=false&key=%s" \
    % (lat,lng,width,height,zoom,API_KEY)
    print url
    image = getImageFromURL(url) 
    return image

def isPositionWater(lng,lat):
    posImg = getPositionImage(lng,lat,1,1,200)
    rgb = getRGB(posImg,0,0)
    diff = (abs(getRGBDiff(
            rgb[0], rgb[1], rgb[2],
            RGB_WATER[0], RGB_WATER[1],RGB_WATER[2]
            )))
    print "DIFF: " + str(diff)
    return diff < RGB_TOLERANCE

if __name__ == "__main__": 
    pos = ("-17.3265590668,-51.8444595337").split(",")
    lng = float(pos[0])
    lat = float(pos[1])

    print "Is water? " + str(isPositionWater(lng, lat))
    img = getPositionImage(lng,lat,1,1,200)
    rgb = getRGB(img,0,0)
    print str(rgb) 
    print "Saving"
    img.save("savedImage.png","PNG")
