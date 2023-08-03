# Import the dependencies.
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

yearAgo = dt.date(2017, 8, 23) - dt.timedelta(days=365)



#################################################
# Flask Routes
#################################################
#Homepage with list of all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


#Convert query results from precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
    p_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= yearAgo).\
        group_by(Measurement.date).all()
    
    session.close()

    year_prcp = []
    for date, prcp in p_scores:
       dict = {}
       dict["date"] = date
       dict["prcp"] = prcp
       year_prcp.append(dict)
    
    return jsonify(year_prcp)


#Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    station_info = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()
    stations = []
    for station in station_info:
        dict = {}
        dict["Station"] = station[0]
        dict["Count"] = station[1]
        stations.append(dict)
    return jsonify(stations)


#Query the dates and temperature observations of the most-active station 
@app.route("/api/v1.0/tobs")
def tobs():
    temp_data = session.query(Measurement.station, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= yearAgo).all()
    session.close()
    temps = []
    for temp in temp_data:
        dict = {}
        dict["Station"] = temp[0]
        dict["Temperature"] = temp[1]
        temps.append(dict)
    return jsonify(temps)


#Return a JSON list of the min temp, the avg temp, and max temp 
@app.route("/api/v1.0/<start>")
def temps_start(start):
    temperature = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    temps = []
    for min, max, avg in temperature:
        dict= {}
        dict["TMIN"] = min
        dict["TMAX"] = max
        dict["TAVG"] = avg
        #from the bin to each dict   
        temps.append(dict)
        
        
    return jsonify(temps)
##Return a JSON list of the min temp, the avg temp, and max temp 
@app.route("/api/v1.0/<start>/<end>")
def temps_start_end(start,end):
    temperature = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = []
    for min, max, avg in temperature:
        dict = {}
        dict["TMIN"] = min
        dict["TMAX"] = max
        dict["TAVG"] = avg
        #from the bin to each dict   
        temps.append(dict)
        
        
    return jsonify(temps)

if __name__ == '__main__':
   app.run(debug=True)    