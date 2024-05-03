from flask import Flask, render_template

app = Flask(__name__,  static_url_path='/static') 

import index
import composition

if __name__ == "__main__":
    app.run(debug=True) 
