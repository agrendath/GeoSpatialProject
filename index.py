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

@app.route("/", methods=['GET'])
def index():
    #print(getLiveboard("Brussels South"))
    #print(getComposition("S51507"))
    return (
    "<p><a href=/composition>Composition</a></p>"
    "<p><a href=/liveboard>liveboard</a></p>"
    "<p><a href=/liveboardSchema>liveboardSchema</a></p>"
    )
