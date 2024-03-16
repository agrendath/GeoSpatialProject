from __main__ import app

@app.route("/liveboard", methods=['GET'])
def liveboard():
    return {
      "version": "1.1",
  "timestamp": 1489614297,
  "station": "Ghent-Sint-Pieters",
  "stationinfo": {
    "id": "BE.NMBS.008821006",
    "@id": "http://irail.be/stations/NMBS/008821006",
    "locationX": 4.421101,
    "locationY": 51.2172,
    "standardname": "Antwerpen-Centraal",
    "name": "Antwerp-Central"
  },
  "departures": {
    "number": 32,
    "departure": [
      {
        "id": 0,
        "delay": 0,
        "station": "Antwerp-Central",
        "stationinfo": {
          "id": "BE.NMBS.008821006",
          "@id": "http://irail.be/stations/NMBS/008821006",
          "locationX": 4.421101,
          "locationY": 51.2172,
          "standardname": "Antwerpen-Centraal",
          "name": "Antwerp-Central"
        },
        "time": 1489575600,
        "vehicle": "BE.NMBS.IC3033",
        "vehicleinfo": {
          "name": "BE.NMBS.IC3033",
          "shortname": "IC3033",
          "@id": "http://irail.be/vehicle/IC3033"
        },
        "platform": 4,
        "platforminfo": {
          "name": "4",
          "normal": "1"
        },
        "canceled": 0,
        "left": 0,
        "departureConnection": "http://irail.be/connections/8821006/20170316/IC1832",
        "occupancy": {
          "@id": "http://api.irail.be/terms/unknown",
          "name": "unknown"
        }
      }
    ]
  }
}
