import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import TemperatureMeasurement, Base


sensors = {
    'red': '/sys/bus/w1/devices/28-800000282522/w1_slave',
}

# Set up the DB
engine = create_engine('sqlite:///test.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
# Create the tables if they don't exist
Base.metadata.create_all(engine)


while 1:
    for name, path in sensors.items():
        with open(path) as device:
            reading = device.read()
        data = reading.split('\n')[1].split(" ")[9]
        temperature = float(data[2:]) / 1000
        print(name, temperature)
        measurement = TemperatureMeasurement(
            device=name,
            moment=datetime.now(),
            value=temperature)
        # Add to DB session
        session.add(measurement)
    session.commit()

    time.sleep(1)
