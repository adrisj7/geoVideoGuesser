#!/usr/bin/python
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from random import randint
import math

import mapGrabber

MAX_LAT = math.atan(math.sinh(math.pi)) * 180 / math.pi
API_KEY = "AIzaSyC3tbVdhbQsl76YEANr6t585tYSw-Lteec"
# TODO: Make developer key a private thing.

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def new_youtube():
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=API_KEY)

def search_response_radius(youtube,location, radius, max_results):
    return youtube.search().list(
        type="video",
        videoEmbeddable='true',
        videoSyndicated='true',
        #eventType="live",
        location=location,
        locationRadius=radius,
        part="id,snippet",
        maxResults=max_results
        #order="date"
    ).execute()

def search_response_latest(youtube,max_results):
    return youtube.search().list(
        type="video",
        part="id,snippet",
        maxResults=max_results,
        order="date"
    )#.execute()

def get_response(youtube,ids,part):
    return youtube.videos().list(
        id=ids,
        part=part
    ).execute()


def youtube_search_distance(location,radius,max_results):
    youtube = new_youtube()

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = search_response_radius(youtube,location,radius,max_results)
    #print "RESPONSE: " + str(search_response)
    search_videos = []
    # Merge video ids
    for search_result in search_response.get("items", []):
        search_videos.append(search_result["id"]["videoId"])
    print str(search_videos)
    video_response = search_videos[2:]
    #video_ids = ",".join(search_videos)
    print "RESPONSE: " + str(video_response)

    # Call the videos.list method to retrieve location details for each video.
    #video_response = get_response(youtube,video_ids,"snippet,recordingDetails")
    videos = []
    # Add each result to the list, and then display the list of matching videos.
    for video in video_response:#.get("items", []): 
        video_result = video[0]
        print "VIDEO: " + "\n"*3 + str(video_result)
        print "RESULT: " + str(video_result) + 4*"\n"
        videos.append( {
            "name" :\
                video_result["snippet"]["title"],\
            "longitude":\
                video_result["recordingDetails"]["location"]["longitude"],\
            "latitude":\
                video_result["recordingDetails"]["location"]["latitude"],
            "thumbnail":\
                video_result["snippet"]["thumbnails"]["default"]["url"],\
            "title":\
                video_result["snippet"]["title"],\
            "id":\
                video_result["id"]
                
        })
    return videos

def youtube_get_random():
    youtube = new_youtube()

    # DEFAULT VIDEO for loop
    video = {
        "id": "sTSA_sWGM44",
        "longitude" : 0,
        "latitude" : 0,
    }
    attempt = 0
    
    while (not videoEdgeCaseCheck(video, attempt)):
        attempt += 1
        print "ATTEMPT: " + str(attempt)
        random_lat = randint(-90,90)
        random_lng = randint(-180,180)
    
        search_response = search_response_radius(
            youtube,
            "%f,%f" % (random_lat, random_lng),
            "100km"
            ,1
        ) 
        
    
        # Merge video ids
        video_id = search_response.get("items", [])[0]["id"]["videoId"]
        print "ID: " + str(video_id)
        video_response = (get_response(     \
                youtube,                   \
                video_id,                  \
                "snippet,recordingDetails" \
                ).get("items",[]))[0]
        print "RESPONSE " + str(video_response)
        video = {
    #        "name" :\
    #            video_response["snippet"]["title"],\
            "longitude":\
                video_response["recordingDetails"]["location"]["longitude"],\
            "latitude":\
                video_response["recordingDetails"]["location"]["latitude"],
    #        "thumbnail":\
    #            video_response["snippet"]["thumbnails"]["default"]["url"],\
            "id":\
                video_response["id"]
        }
    
    return video


# EDGE CASE CHECKER
# Checks that the video fulfills said requirements.
# This can be used to screw around and get videos from specific
# regions or areas. For not it's just to make sure that videos
# make sense.
def videoEdgeCaseCheck(video, attempt):
    
    # Give up after 100 tries
    if attempt > 100:
        return True

    # If on Antarctica
    # (becuase a lot of people decide to put there videos
    # there for some reason)
    if video["latitude"] < -68:
        return False

    # Can't have random videos that are on the North pole
    if video["latitude"] > 80:
        return False

    # If on the water.
    # You won't believe how many videos people just post 
    # in the middle of the ocean for no reason.
    # (That's a real shame, cause there are a few deep sea videos
    #   out there that look really cool)
    if mapGrabber.isPositionWater(
            video["longitude"],
            video["latitude"]):
        return False

    return True


def searchLocation(longitude,latitude,radius, maxresults):
    location = str(longitude) + "," + str(latitude)
#    argparser.add_argument("--max-results", help="Max results",
#            default=maxresults)
#    argparser.add_argument("--location", help="Coordinate Location",
#            default=str(longitude) + "," + str(latitude))
#    argparser.add_argument("--location_radius", help="Location Radius",
#            default=radius)
#    args = argparser.parse_args()
    try:
        return youtube_search_distance(location, radius, maxresults)
    except HttpError, e:
        return  "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

def searchRandom():
    try:
        return youtube_get_random()
    except HttpError, e:
        return  "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

if __name__ == "__main__":
    print str(searchRandom())
#    print searchLocation(40.668459, -73.837135,"1000km",10)
#    print str(searchLocation(-73.99094581604004,40.74198972871056,"100km",50))
#    argparser.add_argument("--q", help="Search term", default="")
#    argparser.add_argument("--max-results", help="Max results", default=10)
#    argparser.add_argument("--location", help="Coordinate Location",
#            default="40.668459, -73.837135")
#    argparser.add_argument("--location_radius", help="Location Radius",
#            default="100km")
#    args = argparser.parse_args()
#    try:
#        youtube_search(args)
#    except HttpError, e:
#        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
