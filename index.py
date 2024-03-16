from __main__ import app

@app.route("/", methods=['GET'])
def index():
    return (
    "<p><a href=/composition>Composition</a></p>"
    "<p><a href=/liveboard>liveboard</a></p>"
    "<p><a href=/liveboardSchema>liveboardSchema</a></p>"
    )
