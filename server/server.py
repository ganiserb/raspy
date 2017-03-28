# coding=utf-8
import config
from flask import Flask, render_template, send_from_directory, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TemperatureMeasurement

app = Flask(__name__)

# Set up the DB
engine = create_engine(config.DB_STRING, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
def start():
    return render_template('index.html')


@app.route('/get_data')
def get_data():
    # a = request.args.get('a', 0, type=int)
    # b = request.args.get('b', 0, type=int)
    q = session.query(TemperatureMeasurement).all()
    data = [i.as_dict() for i in q]
    return jsonify(items=data)
    # return "asd"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('/home/pi/raspy/server/js/', path)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
