# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect = True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():

    #Query results from last 12 months
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    x = session.query(measurement.prcp, measurement.date).filter(measurement.date >= one_year).all()

    session.close()

    #Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in x:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['precipitation'] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    #Query all station
    x = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_station = list(np.ravel(x))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tob():

    # Query of the most active station
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    x = session.query(measurement.tobs, measurement.date).filter(measurement.station == 'USC00519281')\
        .filter(measurement.date >= one_year).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_tob = list(np.ravel(x))

    return jsonify(all_tob)

@app.route("/api/v1.0/<start>")
def start(start):

    # Query of the start date
    x = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_start = list(np.ravel(x))

    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    # Query of the start and end date
    x = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date < end).all()

    # Convert list of tuples into normal list
    all_start_end = list(np.ravel(x))

    return jsonify(all_start_end)

if __name__ == "__main__":
    app.run(debug=True)
