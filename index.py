from __main__ import app
import requests
from datetime import datetime
import overpy
from flask import render_template, request, redirect, url_for
from geopy import distance

import composition

def computeDistance(location1, location2):
    return distance.distance(location1, location2).m

def getDirection(zone_markers, first_stop):
    if len(zone_markers) < 2:
        return "unknown"
    if first_stop is None:
        return "unknown"
    nextLocation = (first_stop["stationinfo"]["locationY"], first_stop["stationinfo"]["locationX"])
    firstZone = (zone_markers[0]["lat"], zone_markers[0]["lon"])
    lastZone = (zone_markers[-1]["lat"], zone_markers[-1]["lon"])

    dist1 = computeDistance(nextLocation, firstZone)
    dist2 = computeDistance(nextLocation, lastZone)

    print("[DEBUG] Distance to first zone marker: " + str(dist1))
    print("[DEBUG] Distance to last zone marker: " + str(dist2))

    if dist1 < dist2:
        return "left"
    else:
        return "right"

overpass_api = overpy.Overpass()

def formatConnections(connections, departure):
    id = departure["departureConnection"]
    stops = None
    #print(str(connections))
    for connection in connections["connection"]:
        #print("---------------------------------- Dep: " + str(connection))
        if connection["departure"] is None or connection["departure"]["departureConnection"] is None:
            continue
        if connection["departure"]["departureConnection"] == id:
            stops = connection["departure"]["stops"]

    if stops is None:
        return ([], None)

    final = []
    for stop in stops["stop"]:
        final.append(stop["station"])

    print("[DEBUG] Stops of the train: " + str(final))
    if final == []:
        first_stop = None
    else:
        first_stop = stops["stop"][0]
    return (final, first_stop)

def getConnections(station_from, station_to):
    url = "http://api.irail.be/connections"
    params = {"from": station_from, "to": station_to, "format": "json"}
    response = requests.get(url, params=params)
    try:
        response = response.json()
    except requests.JSONDecodeError:
        print("[ERROR] Something went wrong while getting the connections")
        return None
    if response is None:
        print("[ERROR] Something went wrong while getting the connections")
        return None
    if "error" in response:
        print("[ERROR] Something went wrong while getting the connections:", response["message"])
        return None
    #print("[DEBUG] Connections:", response)
    #for temp in response["connection"]:
        #print(" --- " + str(temp))
        #print(" ---------------------------------------------------------------------------")
    return response

def getLiveboard(station):
    url = "http://api.irail.be/liveboard"
    params = {"station": station, "format": "json"}
    response = requests.get(url, params=params)
    response = response.json()
    if response is None:
        print("[ERROR] Something went wrong while getting the liveboard")
        return None
    if "error" in response:
        print("[ERROR] Something went wrong while getting the liveboard:", response["message"])
        return None
    return response


def getComposition(station, departure):
    liveboard = getLiveboard(station)
    from_id = liveboard["stationinfo"]["id"].split(".")[-1]
    to_id = departure["stationinfo"]["id"].split(".")[-1]
    vehicle = departure["vehicleinfo"]["number"]
    time = datetime.fromtimestamp(int(departure["time"]))
    print(
        "[DEBUG] Getting composition with " + from_id + " -> " + to_id + "; vehicle:" + vehicle + "; time:" + str(time))
    comp = composition.get_train_composition(from_id, to_id, vehicle, time)
    print(comp)
    composition_data = {
        "facilities": comp.facilities,
        "occupancy": comp.occupancy,
        "carriages_count": comp.carriages_count,
        "carriages": [
            {
                "carriage_type": carriage.carriage_type,
                "model": carriage.model,
                "classes": carriage.classes,
                "facilities": carriage.facilities,
                "carriage_size": carriage.carriage_size
            }
            for carriage in comp.carriages
        ]
    }
    return composition_data


"""
Sample departure: {'id': '28', 'delay': '0', 'station': 'Kortrijk', 'stationinfo': {'locationX': '3.264549', 'locationY': '50.824506', 'id': 'BE.NMBS.008896008', 'name': 'Kortrijk', '@id': 'http://irail.be/stations/NMBS/008896008', 'standardname': 'Kortrijk'}, 'time': '1711892340', 'vehicle': 'BE.NMBS.IC2338', 'vehicleinfo': {'name': 'BE.NMBS.IC2338', 'shortname': 'IC 2338', 'number': '2338', 'type': 'IC', 'locationX': '0', 'locationY': '0', '@id': 'http://irail.be/vehicle/IC2338'}, 'platform': '13', 'platforminfo': {'name': '13', 'normal': '1'}, 'canceled': '0', 'left': '0', 'isExtra': '0', 'departureConnection': 'http://irail.be/connections/8814001/20240331/IC 2338'}
"""


def getNextDeparture(station, platform):
    liveboard = getLiveboard(station)
    if liveboard is None:
        return None
    departures = liveboard["departures"]["departure"]
    for departure in departures:
        if departure["platform"] != "?" and int(departure["platform"]) == platform:
            print("[DEBUG] Departure: " + str(departure))
            return departure
    print("[ERROR] NO DEPARTURE FOUND")
    return None  # No departure found


"""
Returns some standard information about the next train departing from the given station and platform.

:param station: The station where the train departs
:param platform: The platform where the train departs
:return: A list with the destination, the vehicle name and the departure time in a readable format
"""


def getNextTrainInfo(station, platform):
    departure = getNextDeparture(station, platform)
    destination = departure["station"]
    vehicle_name = departure["vehicleinfo"]["shortname"]
    time = datetime.fromtimestamp(int(departure["time"]))
    readable_time = time.strftime("%H:%M")

    return [destination, vehicle_name, readable_time]


def getStandstillPositions(overpass_station_name):
    query = """
    [out:json][timeout:25];
    area(id:3600052411)->.searchArea;
    (
    nwr["railway"="station"][name=\"""" + overpass_station_name + """\"]["station"!="subway"]["tram"!="yes"](area.searchArea);
    );
    nwr["railway"="signal"](around: 100.00);
    out geom;
    """
    response = overpass_api.query(query)
    positions = []
    for node in response.nodes:
        position = {
            "track": node.tags.get("ref:track", ""),
            "ref": node.tags.get("ref", ""),
            "lat": node.lat,
            "lon": node.lon
        }
        positions.append(position)

    if (positions == []):
        print("[ERROR] No signal points found.")
    return positions


def getNodesWithTrack(nodes, track):
    result = []
    for node in nodes:
        if node["track"] == str(track):
            result.append(node)
    if len(result) == 0:
        print("[ERROR] Got empty list of nodes when looking for standstill positions for track " + str(track))
    return result


def getNodeWithRef(nodes, ref):
    for node in nodes:
        if node["ref"] == str(ref):
            return node
    print("[WARNING] No node found with ref " + str(ref))
    return None


def getZoneMarkers(overpass_station_name):
    query = """
    [out:json][timeout:25];
    area(id:3600052411)->.searchArea;
    (
    nwr["railway"="station"][name=\"""" + overpass_station_name + """\"]["station"!="subway"]["tram"!="yes"](area.searchArea);
    );
    nwr["railway"="platform_marker"](around: 100.00);
    out geom;
    """

    response = overpass_api.query(query)
    zone_markers = []
    for node in response.nodes:
        marker = {
            "track": node.tags.get("ref:track", ""),
            "ref": node.tags.get("ref", ""),
            "lat": node.lat,
            "lon": node.lon
        }
        zone_markers.append(marker)

    if (zone_markers == []):
        print("[ERROR] No zone markers found.")

    return zone_markers


def getNextNextDeparture(station, platform):
    liveboard = getLiveboard(station)
    if liveboard is None:
        return None
    departures = liveboard["departures"]["departure"]
    next_train_found = False
    for departure in departures:
        if next_train_found and departure["platform"] != "?" and int(departure["platform"]) == platform:
            return departure
        if departure["platform"] != "?" and int(departure["platform"]) == platform:
            next_train_found = True
    print("[ERROR] NO NEXT DEPARTURE FOUND")
    return None  # No departure found


def getStandstillPosition(station, overpass_station_name, platform):
    departure = getNextDeparture(station, platform)
    if departure is None:
        return None  # No standstill position found

    next_departure = getNextNextDeparture(station, platform)
    if next_departure is None:
        return None  # No next departure found

    train_id = departure["vehicle"].split(".")[-1]
    next_train_id = next_departure["vehicle"].split(".")[-1]

    composition_data = getComposition(station, departure)
    if composition_data is None:
        return None

    next_composition_data = getComposition(station, next_departure)
    if next_composition_data is None:
        return None

    position_data = getStandstillPositions(overpass_station_name)

    signals = getNodesWithTrack(position_data, platform)
    carriages_amount = int(composition_data["carriages_count"])
    temp_amount = carriages_amount
    if carriages_amount % 2 == 1:
        temp_amount -= 1
    standstill_position = getNodeWithRef(signals, str(temp_amount))
    if standstill_position is None:
        print("[WARNING] Was not able to find standstill position for " + str(carriages_amount) + " carriages.")

    all_zone_markers = getZoneMarkers(overpass_station_name)
    track_zone_markers = getNodesWithTrack(all_zone_markers, platform)
    if len(track_zone_markers) == 0:
        print("[WARNING] No zone markers found for track " + str(platform))

    output = {
        "station": departure["station"],
        "destination": departure["stationinfo"]["name"],
        "vehicle_name": departure["vehicleinfo"]["shortname"],
        "departure_time": datetime.fromtimestamp(int(departure["time"])).strftime("%H:%M"),
        "composition": composition_data,
        "next_destination": next_departure["stationinfo"]["name"],
        "next_vehicle_name": next_departure["vehicleinfo"]["shortname"],
        "next_departure_time": datetime.fromtimestamp(int(next_departure["time"])).strftime("%H:%M"),
        "next_composition": next_composition_data,
        "standstill_position": standstill_position,
        "zone_markers": track_zone_markers,
        "departure": departure
    }

    return output


@app.route("/", methods=['GET'])
def index():
    station = "Brussels North"
    station_overpass_name = "Bruxelles-Nord - Brussel-Noord"
    platform = 6
    standstill_position = getStandstillPosition(station, station_overpass_name, platform)

    # return(f"{standstill_position}")
    # standstill_position = None   #test with no standstill_position if standstill_position
    #standstill_position = {'station': 'Nivelles', 'destination': 'Nivelles', 'vehicle_name': 'S1 1989','departure_time': '19:10','composition': {'facilities': ['airconditioning', 'heating'], 'occupancy': 'low', 'carriages_count': 10, 'carriages': [ {'carriage_type': 'left-wagon', 'model': 'AM08P_c', 'classes': [1, 2],'facilities': ['accessible_toilet', 'toilet', 'bike'], 'carriage_size': 18.4}, {'carriage_type': '', 'model': 'AM08P_b', 'classes': [2], 'facilities': [], 'carriage_size': 18.4},{'carriage_type': 'middle-wagon', 'model': 'AM08P_a', 'classes': [1, 2], 'facilities': [], 'carriage_size': 18.4}]},'standstill_position': None}  # test with standstill_position if no standstill_position
    print(standstill_position)
    
    if standstill_position is None:
        return render_template('index.html', platform=f"{platform}",
                               error=f"No standstill position found for {station}.")

    destination = standstill_position["destination"]
    vehicle_name = standstill_position["vehicle_name"]
    departure_time = standstill_position["departure_time"]
    composition_data = standstill_position["composition"]
    standstill_position_data = standstill_position["standstill_position"]
    try:
        next_destination = standstill_position["next_destination"]
        next_departure_time = standstill_position["next_departure_time"]
    except KeyError:
        next_destination = "None"
        next_departure_time = "None"

    connections = getConnections(station, destination)
    (stops, first_stop) = formatConnections(connections, standstill_position["departure"])

    direction = getDirection(standstill_position["zone_markers"], first_stop)
    if first_stop is not None:
        print("[DEBUG] First stop: " + str(first_stop["station"]))
    print("[DEBUG] Zone markers: " + str(standstill_position["zone_markers"]))
    print("[DEBUG] Determined direction: " + direction)

    carriages_info = []
    for carriage in composition_data["carriages"]:
        carriage_type = carriage["carriage_type"]
        carriage_classes = carriage["classes"]
        model = carriage["model"]
        facilities = carriage["facilities"]
        carriages_icon = ""
        carriage_info = model
        if "bike" in facilities:
            carriage_info += " (Bike)"
        if "accessible_toilet" in facilities:
            carriage_info += " (Accessible toilet)"
        if "toilet" in facilities:
            carriage_info += " (Toilet)"
        if "luggage_lockers" in facilities:
            carriage_info += " (Luggage lockers)"

        carriage_info += f" - {carriage_classes}"
        carriages_info.append(carriage_info)

    carriages = ", ".join(carriages_info)

    facilities = composition_data["facilities"]

    if standstill_position_data:
        position_info = f"Position: Ref - {standstill_position_data['ref']}, Lat - {standstill_position_data['lat']}, Lon - {standstill_position_data['lon']}"
    else:
        position_info = "No standstill position data found."

    try:
        zone_markers = standstill_position["zone_markers"]
    except KeyError:
        zone_markers = "None"

    return render_template('index.html', error="No", platform=f"{platform}", destination=f"{destination}",
                           departure_time=f"{departure_time}",
                           facilities=facilities, composition_occupancy=f"{composition_data['occupancy']}",
                           carriages=carriages,
                           position_info=f"{position_info}", zone_markers=zone_markers,
                           next_destination=f"{next_destination}", next_departure_time=f"{next_departure_time}", 
                           stops=stops, direction=f"{direction}")
