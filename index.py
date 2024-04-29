from __main__ import app
import requests
from datetime import datetime
import overpy
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
    #print(composition.get_train_composition)
    liveboard = getLiveboard(station)
    from_id = liveboard["stationinfo"]["id"].split(".")[-1]
    to_id = departure["stationinfo"]["id"].split(".")[-1]
    vehicle = departure["vehicle"].split(".")[-1]
    time = datetime.fromtimestamp(int(departure["time"]))
    print("[DEBUG] Getting composition with " + from_id + " -> " + to_id + "; vehicle:" + vehicle + "; time:" + str(time))
    print(composition.get_train_composition(from_id, to_id, vehicle, time))

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
    return overpass_api.query(query)

def getStandstillPosition(station, overpass_station_name, platform):
    departure = getNextDeparture(station, platform)
    print(departure)
    if departure is None:
        return None  # No standstill position found
    train_id = departure["vehicle"].split(".")[-1]
    print(departure['vehicle'])
    composition = getComposition(station, departure)
    if composition is None:
        return None
    # TODO: now that we have the composition, get static data and derive standstill position in function of train composition (# carriages)
    positions = getStandstillPositions(overpass_station_name).nodes


@app.route("/", methods=['GET'])
def index():
    #print(getLiveboard("Brussels South"))
    #print(getComposition("S51507"))
    #print(getNextDeparture("Brussels North", 7))
    #print(getStandstillPosition("Brussels North", 7))
    print(getStandstillPosition("Brussels North", "Bruxelles-Nord - Brussel-Noord", 7))
    #print(getNextTrainInfo("Brussels North", 7))
    return (
    "<p><a href=/composition>Composition</a></p>"
    "<p><a href=/liveboard>liveboard</a></p>"
    "<p><a href=/liveboardSchema>liveboardSchema</a></p>"
    )
