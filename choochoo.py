import urllib.request, json 
import datetime


# 1970-01-01 09:00:00
with urllib.request.urlopen("https://cdn.mbta.com/realtime/VehiclePositions_enhanced.json") as url:
    data = json.load(url)
    #print(data)


#Realtime site: https://mbta.sites.fas.harvard.edu/T/subway-map.html

#print(data.keys())

header = data['header']
entity = data['entity']
#print(header.keys())

timestamp = header['timestamp']

#: 1668616977}
dt = datetime.datetime.fromtimestamp(timestamp)

print(dt)


tracked_train_id = 1637

if tracked_train_id == 0:
    for key in entity:
        #print(key.keys())
        if key['vehicle']['trip']['route_id']=="Red":
            print(key['vehicle']['vehicle']['consist'][0]['label'])
            if tracked_train_id==0:
                tracked_train_id = key['vehicle']['vehicle']['consist'][0]['label']
                print(tracked_train_id)
            print(key['vehicle']['current_stop_sequence'])
        #print(key['vehicle']['trip']['route_id'])
else:
    for key in entity:
        #print(key.keys())
        if key['vehicle']['trip']['route_id']=="Red":
            #print(key['vehicle']['vehicle']['consist'][0]['label'])
            if int(key['vehicle']['vehicle']['consist'][0]['label']) == tracked_train_id:
                print(tracked_train_id)
                print(key['vehicle']['current_stop_sequence'])
                
# EXAMPLE JSON FORMAT FOR ORANGE LINE        
        
# {"id":"O-5473941A",
#  "vehicle":{
#         "current_status":"STOPPED_AT",
#         "current_stop_sequence":70,
#         "position":
#                 {"bearing":85,
#                 "latitude":42.34758,
#                 "longitude":-71.07465
#                 },
#         "stop_id":"70015",
#         "timestamp":1668615485,
#         "trip":{
#             "direction_id":1,
#             "route_id":"Orange",
#             "schedule_relationship":"SCHEDULED",
#             "start_date":"20221116",
#             "start_time":"11:05:00",
#             "trip_id":"53244861"
#             },
#         "vehicle":{
#             "consist":[{"label":"1406"},
#                         {"label":"1407"},
#                         {"label":"1445"},
#                         {"label":"1444"},
#                         {"label":"1465"},
#                         {"label":"1464"}],
#             "id":"O-5473941A",
#             "label":"1406"
#             }
#      } 
# },
            
