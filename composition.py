from __main__ import app

@app.route("/composition", methods=['GET'])
def composition():
    return {
  "version": "1.1",
  "timestamp": "1581856899",
  "composition": {
    "segments": {
      "number": "1",
      "segment": [
        {
          "id": "0",
          "origin": {
            "locationX": "4.071825",
            "locationY": "50.891925",
            "id": "BE.NMBS.008895802",
            "name": "Denderleeuw",
            "@id": "http://irail.be/stations/NMBS/008895802",
            "standardname": "Denderleeuw"
          },
          "destination": {
            "locationX": "4.071825",
            "locationY": "50.891925",
            "id": "BE.NMBS.008895802",
            "name": "Denderleeuw",
            "@id": "http://irail.be/stations/NMBS/008895802",
            "standardname": "Denderleeuw"
          },
          "composition": {
            "source": "Itris",
            "units": {
              "number": "3",
              "unit": [
                {
                  "id": "0",
                  "materialType": {
                    "parent_type": "AM08M",
                    "sub_type": "c",
                    "orientation": "LEFT"
                  },
                  "hasToilets": "1",
                  "hasTables": "1",
                  "hasSecondClassOutlets": "1",
                  "hasFirstClassOutlets": "1",
                  "hasHeating": "1",
                  "hasAirco": "1",
                  "materialNumber": "8112",
                  "tractionType": "AM/MR",
                  "canPassToNextUnit": "0",
                  "standingPlacesSecondClass": "27",
                  "standingPlacesFirstClass": "9",
                  "seatsCoupeSecondClass": "0",
                  "seatsCoupeFirstClass": "0",
                  "seatsSecondClass": "76",
                  "seatsFirstClass": "16",
                  "lengthInMeter": "27",
                  "hasSemiAutomaticInteriorDoors": "1",
                  "hasLuggageSection": "0",
                  "materialSubTypeName": "AM08M_c",
                  "tractionPosition": "1",
                  "hasPrmSection": "1",
                  "hasPriorityPlaces": "1",
                  "hasBikeSection": "1"
                },
                {
                  "id": "1",
                  "materialType": {
                    "parent_type": "AM08M",
                    "sub_type": "b",
                    "orientation": "LEFT"
                  },
                  "hasToilets": "0",
                  "hasTables": "1",
                  "hasSecondClassOutlets": "1",
                  "hasFirstClassOutlets": "1",
                  "hasHeating": "1",
                  "hasAirco": "1",
                  "materialNumber": "8112",
                  "tractionType": "AM/MR",
                  "canPassToNextUnit": "0",
                  "standingPlacesSecondClass": "40",
                  "standingPlacesFirstClass": "0",
                  "seatsCoupeSecondClass": "0",
                  "seatsCoupeFirstClass": "0",
                  "seatsSecondClass": "104",
                  "seatsFirstClass": "0",
                  "lengthInMeter": "27",
                  "hasSemiAutomaticInteriorDoors": "1",
                  "hasLuggageSection": "0",
                  "materialSubTypeName": "AM08M_b",
                  "tractionPosition": "1",
                  "hasPrmSection": "0",
                  "hasPriorityPlaces": "1",
                  "hasBikeSection": "0"
                },
                {
                  "id": "2",
                  "materialType": {
                    "parent_type": "AM08M",
                    "sub_type": "a",
                    "orientation": "RIGHT"
                  },
                  "hasToilets": "0",
                  "hasTables": "1",
                  "hasSecondClassOutlets": "1",
                  "hasFirstClassOutlets": "1",
                  "hasHeating": "1",
                  "hasAirco": "1",
                  "materialNumber": "8112",
                  "tractionType": "AM/MR",
                  "canPassToNextUnit": "0",
                  "standingPlacesSecondClass": "37",
                  "standingPlacesFirstClass": "9",
                  "seatsCoupeSecondClass": "0",
                  "seatsCoupeFirstClass": "0",
                  "seatsSecondClass": "68",
                  "seatsFirstClass": "16",
                  "lengthInMeter": "27",
                  "hasSemiAutomaticInteriorDoors": "1",
                  "hasLuggageSection": "0",
                  "materialSubTypeName": "AM08M_a",
                  "tractionPosition": "1",
                  "hasPrmSection": "0",
                  "hasPriorityPlaces": "1",
                  "hasBikeSection": "0"
                }
              ]
            }
          }
        }
      ]
    }
  }
}