from flask import Flask

app = Flask(__name__) 

import index
import composition
import liveboard
import liveboardSchema

if __name__ == "__main__":
    app.run(debug=True) 
