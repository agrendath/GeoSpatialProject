from __main__ import app
import requests
from datetime import datetime
import overpy

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

def getComposition(train_id):
    url = "http://api.irail.be/composition"
    params = {"id": train_id, "format": "json"}
    response = requests.get(url, params=params)
    response = response.json()
    if response is None:
        print("[ERROR] Something went wrong while getting the train's composition")
        return None
    if "error" in response:
        print("[ERROR] Something went wrong while getting the train's composition:", response["message"])
        return None
    return response

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

def getStandstillPosition(station, platform):
    departure = getNextDeparture(station, platform)
    if departure is None:
        return None  # No standstill position found
    train_id = departure["vehicle"].split(".")[-1]
    composition = getComposition(train_id)
    if composition is None:
        return None
    #print(composition)
    # TODO: now that we have the composition, get static data and derive standstill position


@app.route("/", methods=['GET'])
def index():
    #print(getLiveboard("Brussels South"))
    #print(getComposition("S51507"))
    #print(getNextDeparture("Brussels South", 13))
    getStandstillPosition("Brussels North", 7)
    return (
    "<p><a href=/composition>Composition</a></p>"
    "<p><a href=/liveboard>liveboard</a></p>"
    "<p><a href=/liveboardSchema>liveboardSchema</a></p>"
    )
