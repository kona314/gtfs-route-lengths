import sys

try:
    import geopy
except ImportError:
    print("This script requires the geopy module. Use `pip install geopy`")
    sys.exit()

import statistics, math
from geopy import distance

PATH_TO_GTFS = "" #specify path to your extracted, plain-text GTFS data here, or run in same directory

if PATH_TO_GTFS == "":
    PATH_TO_GTFS = input("Where is your extracted GTFS data? Leave blank for same directory.\n")

shapes = open("{}/shapes.txt".format(PATH_TO_GTFS), "r")
routes = open("{}/routes.txt".format(PATH_TO_GTFS), "r")
trips = open("{}/trips.txt".format(PATH_TO_GTFS), "r")

routesForShapes = {}
lengths = {}

def matchRoutes():
    routesTemp = {}
    with routes as r:
        routeHeader = next(r).split(",")
        ROUTE_ID = routeHeader.index("route_id")
        ROUTE_NAME = routeHeader.index("route_short_name")
        for route in routes:
            route = route.split(",")
            routesTemp[route[ROUTE_ID]] = route[ROUTE_NAME]
    with trips as t:
        tripHeader = next(t).split(",")
        SHAPE_ID = tripHeader.index("shape_id")
        ROUTE_ID = tripHeader.index("route_id")
        for trip in trips:
            trip = trip.split(",")
            routesForShapes[trip[SHAPE_ID]] = routesTemp[trip[ROUTE_ID]]

def getLengths():
    currentId = ""
    currentLength = 0
    lastll = None
    first = True
    with shapes as s:
        shapesHeader = next(s).split(",")
        SHAPE_ID = shapesHeader.index("shape_id")
        SHAPE_PT_LAT = shapesHeader.index("shape_pt_lat")
        SHAPE_PT_LON = shapesHeader.index("shape_pt_lon")
        for part in s:
            l = part.split(",")
            thisID = l[SHAPE_ID]
            lat = l[SHAPE_PT_LAT]
            lon = l[SHAPE_PT_LON]
            thisll = (lat, lon)
            if first:
                currentId = thisID
                lastll = thisll
                first = False
            if currentId != thisID:
                if currentId in routesForShapes and routesForShapes[currentId] in lengths:
                    lengths[routesForShapes[currentId]] = statistics.mean([lengths[routesForShapes[currentId]],currentLength])
                elif currentId in routesForShapes: 
                    lengths[routesForShapes[currentId]] = currentLength
                else:
                    lengths[currentId] = currentLength
                currentId = thisID
                currentLength = 0
                lastll = thisll
            else:
                currentLength += geopy.distance.distance(lastll, thisll).miles
                lastll = thisll

matchRoutes()
getLengths()
sortedLengths = sorted(lengths, key=lengths.get, reverse=True)
for i in sortedLengths:
    l = str(math.ceil(lengths[i]*100)/100)
    if len(l) < 5:
        l = l + "0"
    print(i, ": ", l, " miles")