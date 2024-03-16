from __main__ import app

@app.route("/liveboardSchema", methods=['GET'])
def liveboardSchema():
    return {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "version": {
      "type": "string"
    },
    "timestamp": {
      "type": "number"
    },
    "station": {
      "type": "string"
    },
    "stationinfo": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The (iRail) id of the station. The NMBS id can be deducted by removing the leading 'BE.NMBS.00'"
        },
        "@id": {
          "type": "string"
        },
        "locationX": {
          "type": "number",
          "description": "The longitude of the station"
        },
        "locationY": {
          "type": "number",
          "description": "The latitude of the station"
        },
        "standardname": {
          "type": "string",
          "description": "The consistent name of this station"
        },
        "name": {
          "type": "string",
          "description": "The default name of this station"
        }
      },
      "required": [
        "id",
        "@id",
        "locationX",
        "locationY",
        "standardname",
        "name"
      ]
    },
    "departures": {
      "type": "object",
      "properties": {
        "number": {
          "type": "number"
        },
        "departure": {
          "type": "array"
        }
      },
      "required": [
        "number"
      ]
    }
  },
  "required": [
    "version",
    "timestamp",
    "station",
    "departures"
  ]
}
