from __main__ import app
import requests
from datetime import datetime
import overpy
from flask import render_template, request, redirect, url_for

import composition

overpass_api = overpy.Overpass()

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
    print("[DEBUG] Getting composition with " + from_id + " -> " + to_id + "; vehicle:" + vehicle + "; time:" + str(time))
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
        if int(departure["platform"]) == platform:
            return departure
    print("[ERROR] NO DEPARTURE FOUND")
    return None # No departure found

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
            "ref": node.tags.get("ref", ""),
            "lat": node.lat,
            "lon": node.lon
        }
        positions.append(position)
    return positions

def getStandstillPosition(station, overpass_station_name, platform):
    departure = getNextDeparture(station, platform)
    print(departure)
    if departure is None:
        return None  # No standstill position found
    train_id = departure["vehicle"].split(".")[-1]
    print(departure['vehicle'])
    composition_data = getComposition(station, departure)
    if composition_data is None:
        return None

    position_data = getStandstillPositions(overpass_station_name)

    # Find the standstill position based on the number of carriages
    carriages_count = composition_data["carriages_count"]
    if carriages_count <= len(position_data):
        standstill_position = position_data[carriages_count - 1]
    else:
        standstill_position = None

    # Create a clean output dictionary
    output = {
        "station": departure["station"],
        "destination": departure["stationinfo"]["name"],
        "vehicle_name": departure["vehicleinfo"]["shortname"],
        "departure_time": datetime.fromtimestamp(int(departure["time"])).strftime("%H:%M"),
        "composition": composition_data,
        "standstill_position": standstill_position
    }

    return output

@app.route("/", methods=['GET'])
def index():
    station = "Brussels North"
    platform = 8
    standstill_position = getStandstillPosition(station, "Bruxelles-Nord - Brussel-Noord", platform)

    if standstill_position is None:
        return "No standstill position found."

    destination = standstill_position["destination"]
    vehicle_name = standstill_position["vehicle_name"]
    departure_time = standstill_position["departure_time"]
    composition_data = standstill_position["composition"]
    standstill_position_data = standstill_position["standstill_position"]

    carriages_info = []
    for carriage in composition_data["carriages"]:
        carriage_type = carriage["carriage_type"]
        model = carriage["model"]
        facilities = carriage["facilities"]
        carriage_info = model
        if "bike" in facilities:
            carriage_info += " (Bike)"
        if "accessible_toilet" in facilities:
            carriage_info += " (Accessible toilet)"
        elif "toilet" in facilities:
            carriage_info += " (Toilet)"

        carriages_info.append(carriage_info)

    carriages = ", ".join(carriages_info)

    if standstill_position_data:
        position_info = f"Position: Ref - {standstill_position_data['ref']}, Lat - {standstill_position_data['lat']}, Lon - {standstill_position_data['lon']}"
    else:
        position_info = "No standstill position data found."

    #return(f"{destination}" f"{vehicle_name}" f"{departure_time}" f"{composition_data}")
    return render_template('index.html', destination = f"{destination}", vehicle_name = f"{vehicle_name}",departure_time = f"{departure_time}",facilities = f"{facilities}",composition_occupancy = f"{composition_data['occupancy']}",composition_carriages = f"{composition_data['carriages_count']}",carriages = f"{carriages}",position_info = f"{position_info}")
