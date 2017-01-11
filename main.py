#!/usr/bin/env python

# Put your properties' addresses here.
PropertyLocations = ["11 Walmgate, York, YO1 9TX"]

# Turn off this to omit the requirement of Keras.
AcceptablePrediction = True

# Put your desired addresses here.
Locations = ["YO10 5DD", "YO10 5GP", "YO1 7LZ", "York Railstation"]
LocationNames = ["West Campus", "East Campus", "York City Centre", "York Railstation"]

SelectiveLocations = []
SelectiveLocationNames = []
SelectionNames = []

API_KEY = "AIzaSyC7lgoGeM6FChC_3wGFA0Uv2V2DGAu9Ed0"

import json, requests
from Route import *

def requestRouteJson(origin, destination, mode):
    # Feed following parameters in with sequence.
    # Origin
    # Destination
    # Mode = (driving | walking | bicycling | transit)
    # Key
    urlMask = "https://maps.googleapis.com/maps/api/directions/json?origin=\"%s\"&destination=\"%s\"&mode=%s&key=%s"
    return json.loads(requests.get(url = urlMask % (origin, destination, mode, API_KEY)).text)
def requestPlacesJson(location):
    urlMask = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=5000&keyword=supermarket&key=%s"
    return json.loads(requests.get(url = urlMask % (location, API_KEY)).text)

def getDistance(jsonResult):
    return jsonResult["routes"][0]["legs"][0]["distance"]["value"] / 1000.0
def getTime(jsonResult):
    return jsonResult["routes"][0]["legs"][0]["duration"]["value"] / 60.0
def getLatLngString(jsonResult):
    loc = jsonResult["routes"][0]["legs"][0]["start_location"]
    return str(loc["lat"]) + ',' + str(loc["lng"])

def getRoute(origin, destination):
    jResult = requestRouteJson(origin, destination, "walking")
    distance = getDistance(jResult)
    walkTime = getTime(jResult)
    jResult = requestRouteJson(origin, destination, "transit")
    busTime = getTime(jResult)
    global propertyLocation
    propertyLocation = getLatLngString(jResult)
    return Route(distance, walkTime, busTime, AcceptablePrediction)

def main():
    for rentProperty in PropertyLocations:
        for place in Locations:
            print getRoute(rentProperty, place)
        assert propertyLocation != ""
        results = requestPlacesJson(propertyLocation)["results"]
        print "Found " + str(len(results)) + " supermarkets around."
        global SelectiveLocations, SelectiveLocationNames, SelectionNames
        SelectiveLocations += [[]]
        SelectiveLocationNames += [[]]
        for supermarket in results:
            print supermarket["name"], ", Address:", supermarket["vicinity"]
            SelectiveLocations[-1] += [supermarket["vicinity"]]
            SelectiveLocationNames[-1] += [supermarket["name"]]
            SelectionNames += ["Most Acceptable Supermarket"]
        for i in range(len(SelectiveLocations)):
            dictLocNameAndRoute = {}
            for x in range(len(SelectiveLocations[i])):
                route = getRoute(rentProperty, SelectiveLocations[i][x])
                dictLocNameAndRoute[SelectiveLocationNames[i][x]] = route
                print SelectiveLocationNames[i][x],"\t", route, "Accept rate:", str(route.getAcceptableProbability()) + "%"
            closestSupermarket = ""
            closestRoute = dictLocNameAndRoute[SelectiveLocationNames[i][0]]
            for key in dictLocNameAndRoute:
                if dictLocNameAndRoute[key] < closestRoute:
                    closestRoute = dictLocNameAndRoute[key]
                    closestSupermarket = key
            print SelectionNames[i] + ": ", closestSupermarket, closestRoute, "Accept rate:", str(closestRoute.getAcceptableProbability()) + "%"

if __name__ == '__main__':
    main()

