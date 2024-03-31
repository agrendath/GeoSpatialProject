from __main__ import app
import requests
from datetime import datetime

def getLiveboard(station):
    url = "http://api.irail.be/liveboard"
    current_date = datetime.now().strftime("%d%m%y")
    current_time = datetime.now().strftime("%H%M")
    params = {"station": station, "date": current_date, "time": current_time, "format": "json"}
    response = requests.get(url, params=params)
    return response.json()

def getComposition(train_id):
    url = "http://api.irail.be/composition"
    params = {"id": train_id, "format": "json"}
    response = requests.get(url, params=params)
    return response.json()

"""
Sample departure: {'id': '28', 'delay': '0', 'station': 'Kortrijk', 'stationinfo': {'locationX': '3.264549', 'locationY': '50.824506', 'id': 'BE.NMBS.008896008', 'name': 'Kortrijk', '@id': 'http://irail.be/stations/NMBS/008896008', 'standardname': 'Kortrijk'}, 'time': '1711892340', 'vehicle': 'BE.NMBS.IC2338', 'vehicleinfo': {'name': 'BE.NMBS.IC2338', 'shortname': 'IC 2338', 'number': '2338', 'type': 'IC', 'locationX': '0', 'locationY': '0', '@id': 'http://irail.be/vehicle/IC2338'}, 'platform': '13', 'platforminfo': {'name': '13', 'normal': '1'}, 'canceled': '0', 'left': '0', 'isExtra': '0', 'departureConnection': 'http://irail.be/connections/8814001/20240331/IC 2338'}
"""
def getNextDeparture(station, platform):
    liveboard = getLiveboard(station)
    departures = liveboard["departures"]["departure"]
    for departure in departures:
        if int(departure["platform"]) == platform:
            return departure
    return None # No departure found


@app.route("/", methods=['GET'])
def index():
    #print(getLiveboard("Brussels South"))
    #print(getComposition("S51507"))
    #print(getNextDeparture("Brussels South", 13))
    return (
    "<p><a href=/composition>Composition</a></p>"
    "<p><a href=/liveboard>liveboard</a></p>"
    "<p><a href=/liveboardSchema>liveboardSchema</a></p>"
    )
