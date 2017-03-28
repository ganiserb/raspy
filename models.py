from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()


class TemperatureMeasurement(Base):
    __tablename__ = 'temperature_measurement'
    id = Column(Integer, primary_key=True)
    device = Column(String)
    moment = Column(DateTime)
    value = Column(Float)

    def __repr__(self):
        return "TemperatureMeasurement(device={}, moment={}, value={})>".format(
            self.device, self.moment, self.value)

    def as_dict(self):
        return {'x': self.moment.isoformat(), 'y': self.value}
