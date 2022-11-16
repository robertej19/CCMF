import urllib.request, json
import datetime
import pandas as pd
import os, sys
import geopy.distance

#How do we know if it is a braintree train or not??

#TO grab latlong from mbta station data
# # # df_stops = pd.read_csv('MBTA_GTFS/stops.txt', sep=',', header=0)

# # # df_RT_stops = df_stops.query('zone_id == "RapidTransit"')

# # # df_rl_stops_not_unique = df_RT_stops[df_RT_stops['stop_desc'].str.contains("Red Line")]

# # # df_rl_stations = df_rl_stops_not_unique .drop_duplicates(subset='parent_station', keep="first")

# # # df_rl_stations.to_csv('rl_stations.csv', sep=',', encoding='utf-8', index=False)

df_rl_stations = pd.read_csv('rl_stations.csv', sep=',', header=0)

#print(df_rl_stations)


### Hardcoded station ordering for Red Line
ordered_stations = ['Alewife', 'Davis', 'Porter', 'Harvard', 'Central', 'Kendall/MIT', 'Charles/MGH', 'Park Street', 'Downtown Crossing', 'South Station', 'Broadway', 'Andrew', 'JFK/UMass',
        'North Quincy', 'Wollaston', 'Quincy Center', 'Quincy Adams', 'Braintree','Savin Hill', 'Fields Corner', 'Shawmut', 'Ashmont']



# 1970-01-01 09:00:00
with urllib.request.urlopen("https://cdn.mbta.com/realtime/VehiclePositions_enhanced.json") as url:
    data = json.load(url)
    #print(data)


#Realtime site: https://mbta.sites.fas.harvard.edu/T/subway-map.html
# more data: https://github.com/mbta/gtfs-documentation/blob/master/reference/gtfs-realtime.md
#print(data.keys())

header = data['header']
entity = data['entity']
#print(header.keys())

#print(entity[0].keys())
#sys.exit()
timestamp = header['timestamp']

#: 1668616977}
dt = datetime.datetime.fromtimestamp(timestamp)

#print(dt)


tracked_train_id = 1641
# # # if tracked_train_id == 0:
# # #     for key in entity:
# # #         #print(key.keys())
# # #         if key['vehicle']['trip']['route_id']=="Red":
# # #             print(key['vehicle']['vehicle']['consist'][0]['label'])
# # #             if tracked_train_id==0:
# # #                 tracked_train_id = key['vehicle']['vehicle']['consist'][0]['label']
# # #                 print(tracked_train_id)
# # #             print(key['vehicle']['current_stop_sequence'])
# # #         #print(key['vehicle']['trip']['route_id'])
# # # else:
# # #     for key in entity:
# # #         #print(key.keys())
# # #         if key['vehicle']['trip']['route_id']=="Red":
# # #             #print(key['vehicle']['vehicle']['consist'][0]['label'])
# # #             #if int(key['vehicle']['vehicle']['consist'][0]['label']) == tracked_train_id:
# # #             if int(key['vehicle']['vehicle']['consist'][0]['label']) > 0:

# # #                 print(tracked_train_id)
# # #                 current_stop = str(key['vehicle']['current_stop_sequence'])
# # #                 print(current_stop)
# # #                 try:
# # #                     print(df_stops[df_stops['stop_id']==current_stop]['stop_name'].values[0])
# # #                 except:
# # #                     pass



if tracked_train_id == 0:
    for key in entity:
        #print(key.keys())
        if key['vehicle']['trip']['route_id']=="Red":
            print(key['vehicle']['vehicle']['consist'][0]['label'])
            if tracked_train_id==0:
                tracked_train_id = key['vehicle']['vehicle']['consist'][0]['label']
                print(tracked_train_id)
            print(key['vehicle']['current_stop_sequence'])
            direction_id = key['vehicle']['trip']['direction_id']
            print(direction_id)
        #print(key['vehicle']['trip']['route_id'])
else:
    for key in entity:
        #print(key.keys())
        if key['vehicle']['trip']['route_id']=="Red":
            if int(key['vehicle']['vehicle']['consist'][0]['label']) == tracked_train_id:
                
                #print(tracked_train_id)
                bearing = key['vehicle']['position']['bearing']
                current_status = key['vehicle']['current_status']
                current_stop = str(key['vehicle']['current_stop_sequence'])
                lat = key['vehicle']['position']['latitude']
                lon = key['vehicle']['position']['longitude']
                timestamp = key['vehicle']['timestamp']
                direction_id = key['vehicle']['trip']['direction_id'] # is southbound, 1 is northbound (towards Alewife)
                dt = datetime.datetime.fromtimestamp(timestamp)
                print(tracked_train_id, dt, bearing, lat, lon, current_status, current_stop, direction_id)


                coords_train = (float(lat), float(lon))

                lats, lons = df_rl_stations['stop_lat'].to_numpy(), df_rl_stations['stop_lon'].to_numpy()

                distance_to_station = []
                for station_lat,station_lon in zip(lats,lons):
                    coords_station = (station_lat, station_lon)
                    distance_to_station.append(geopy.distance.distance(coords_train, coords_station).miles)


                #dist_met = df_rl_stations.apply(lambda row: geopy.distance.distance(coords_train, (row['stop_lat'], row['stop_lon'])).miles, axis=1)
                #print(distance_to_station)
                sorted_dist = sorted(distance_to_station)
                stat_min_ind = distance_to_station.index(sorted_dist[0])
                stat_min2_ind= distance_to_station.index(sorted_dist[1])

                print(stat_min_ind)
                print(stat_min2_ind)

                #coords_2 = (52.406374, 16.9251681)
                min_station_name = df_rl_stations.iloc[stat_min_ind]['stop_name']
                min_station_name2 = df_rl_stations.iloc[stat_min2_ind]['stop_name']

                ordered_station_1_id = ordered_stations.index(min_station_name)
                ordered_station_2_id = ordered_stations.index(min_station_name2)

                print(ordered_station_1_id)
                print(ordered_station_2_id)

                if direction_id == 0:
                    station = min(ordered_station_1_id, ordered_station_2_id)
                else:
                    station = max(ordered_station_1_id, ordered_station_2_id)

                print("IN TRANSIT TO STATION: ", ordered_stations[station])



                #print geopy.distance.geodesic(coords_1, coords_2).km

                #df_rl_stations
                #print(current_stop)
                #try:
                #    print(df_stops[df_stops['stop_id']==current_stop]['stop_name'].values[0])
                #except:
                #    pass

#  "vehicle":{
#         "current_status":"STOPPED_AT",
#         "current_stop_sequence":70,
#         "position":
#                 {"bearing":85,
#                 "latitude":42.34758,
#                 "longitude":-71.07465

#https://www.mbta.com/developers/gtfs-realtime
#https://www.mbta.com/developers/gtfs-realtime

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

