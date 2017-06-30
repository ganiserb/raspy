#!/usr/bin/env python3
import time
import config
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TemperatureMeasurement, Base


sensors = [
    {
        'name': 'red',
        'path': '/sys/bus/w1/devices/28-800000282522/w1_slave',
        'last_measurement': None,
        'last_measurement_moment': None,
    },
]

# Set up the DB
engine = create_engine(config.DB_STRING, echo=True)
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

# Discard the first reading
for sensor in sensors:
    get_temperature(sensor['path'])

iteration = 0
while 1:
    iteration += 1
    for sensor in sensors:
        temperature = get_temperature(sensor['path'])

        temperature_changed = sensor['last_measurement'] != temperature

        time_passed = False
        last_time = sensor['last_measurement_moment']
        if last_time:
            time_passed = (last_time + timedelta(minutes=1)) > datetime.now()

        if temperature_changed and time_passed:
            # Only record changes in measurements
            # after certain time has passed

            sensor['last_measurement'] = temperature  # Update values
            sensor['last_measurement_moment'] = datetime.now()

            measurement = TemperatureMeasurement(
                device=sensor['name'],
                moment=datetime.now(timezone.utc),
                value=temperature)
            # Add to DB session
            session.add(measurement)

    if iteration == 10:
        # Save to DB every X measurements
        iteration = 0
        session.commit()

    # Wait for a second before taking the next measurement
    time.sleep(1)
