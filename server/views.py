from math import sin, cos, sqrt, atan2, radians
from typing import Mapping
from django.shortcuts import render
from requests import request
import json
from django.http import HttpResponse,JsonResponse
import pymongo

connect_string='mongodb+srv://Ankrsi1997:Ankrsi1997@cluster0.rxyud.mongodb.net/TripCab?retryWrites=true&w=majority'
#connect_string='mongodb+srv://Ankrsi12:Ankrsi12@cluster0.fiulc.mongodb.net/TripCab?retryWrites=true&w=majority'
client = pymongo.MongoClient(connect_string)
db = client['TripCab']
collection=db["carLiveLatLong"]

def find_distance(lat1,lon1,lat2,lon2):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    dlon = lon2-lon1
    dlat = lat2-lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R*c
    return distance

def list(request):
    allcarlist=collection.find()
    return HttpResponse(allcarlist, content_type="application/json")

def updateLatLong(request):
    global_ip=request.META.get('HTTP_X_REAL_IP')
    if global_ip:
        ip = global_ip.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    json_data = request.body
    pythondata = json.loads(json_data)
    pythondata['ip']=ip
    try:
        add=collection.insert_one(pythondata)
        if(add.acknowledged):
            return HttpResponse("add", content_type="application/json")
        else:
            return HttpResponse("Not add", content_type="application/json")
    except:
        update=collection.update_one({"_id":pythondata['_id']},{"$set":pythondata})
        if(update.acknowledged):
            return HttpResponse("update", content_type="application/json")
        else:
            return HttpResponse("Not update", content_type="application/json")

def nearestcab(request,latlong):
    allcarlatlong=collection.find()
    carnum=""
    ulatlong=latlong.split(',')
    for i in allcarlatlong:
        if i['carStatus']=='online':
            carlatlong=i['carLatLong'].split(',')
            r=find_distance(float(ulatlong[0]),float(ulatlong[1]),float(carlatlong[0]),float(carlatlong[1]))
            if r<=3.0:
                carnum=i['_id']
                break
    if carnum == "":
        return JsonResponse("{no car found}",safe=False)
    else:
        return JsonResponse(carnum,safe=False)


    
