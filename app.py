import os
from flask import Flask
from component.prediction import prediction_routes

app = Flask(__name__)

app.register_blueprint(prediction_routes)

if __name__ == '__main__':
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
