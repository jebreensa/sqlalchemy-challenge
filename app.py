import numpy as np
import os

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station= Base.classes.station 

# Setup a flask
app = Flask(__name__)

@app.route("/")
def mainpage():
    """List all available api routes."""
    return (f"Available Routes:<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end>")

@app.route("/api/v1.0/prcp")
def prcpdata():
    """Return a list of prcp by date"""
    
    session = Session(engine)
    results = session.query(measurement.prcp, measurement.date).all()
    session.close()
    prcp_results = {val:key for (key,val) in results}
    return jsonify(prcp_results)
@app.route('/api/v1.0/stations')
def stationdata():
    """Return a list of all stations"""
    session = Session(engine)
    results = session.query(station.station).all()
    session.close()
    station_results = list(np.ravel(results))
    return jsonify(station_results)
@app.route("/api/v1.0/tobs")
def active_station():
    """Return information of most active station"""
 
    session = Session(engine)
    end_date = dt.date(2015, 8, 18)
    last_year = end_date - dt.timedelta(365)
    high_activity = 'USC00511918'
    
    
    highactivestation_yrtemp = session.query(measurement.date, measurement.tobs).filter(and_(measurement.date<=end_date, measurement.date>=last_year),measurement.station ==high_activity).all()
    session.close()
    act_results = list(np.ravel(highactivestation_yrtemp))
    return jsonify(act_results)
@app.route("/api/v1.0/<start>")
def start_date(start):    
    session = Session(engine)
    print(f"\n\n\nincoming start: {start}")
    print(f"type: {type(start)}\n\n\n")
    starttemp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify(starttemp_data)
@app.route("/api/v1.0/<start>/<end>")
def range_date(start,end):
    session = Session(engine)
    endtemp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(and_(measurement.date >= start, measurement.date <= end)).all()
    session.close()
    return jsonify(endtemp_data)


if __name__ == "__main__":
    app.run(debug=True)


