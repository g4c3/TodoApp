from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    

from app import models, routes, mongodb, dtos