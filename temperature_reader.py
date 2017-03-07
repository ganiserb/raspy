#!/usr/bin/env python3
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TemperatureMeasurement, Base


sensors = [
    {
        'name': 'red',
        'path': '/sys/bus/w1/devices/28-800000282522/w1_slave',
        'last_measurement': None,
    },
]

# Set up the DB
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables if they don't exist
Base.metadata.create_all(engine)


def get_temperature(path):
    # Returns the temperature given the path of the device
    with open(path) as device:
        reading = device.read()
    data = reading.split('\n')[1].split(" ")[9]
    return float(data[2:]) / 1000

iteration = 0
while 1:
    iteration += 1
    for sensor in sensors:
        temperature = get_temperature(sensor['path'])

        if sensor['last_measurement'] != temperature:
            sensor['last_measurement'] = temperature  # Update value
            # Only record changes in measurements
            measurement = TemperatureMeasurement(
                device=sensor['name'],
                moment=datetime.now(),
                value=temperature)
            # Add to DB session
            session.add(measurement)

    if iteration == 60:
        # Save to DB every 60 measurements
        iteration = 0
        session.commit()

    # Wait for a second before taking the next measurement
    time.sleep(1)
