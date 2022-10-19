from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = True
app.config.from_object(__name__)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    

from app import models, routes, decorators