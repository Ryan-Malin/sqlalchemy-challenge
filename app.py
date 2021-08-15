# Imports
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy import extract

# Engines and Database
engine = create_engine("sqlite:///SQAlchemy_Instructions/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

# Set up Flask
app = Flask(__name__)

@app.route("/")

# List all routes that are available
def home():
    return(
        f"Select from the following routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>")

# Create the 'precipitation' route        

@app.route("/api/v1.0/precipitation")

# Convert the query results to a dictionary using
# date as the key and prcp as the value
def precipitation():
    last_yr = dt.date(2017,8,23) - dt.timedelta(days = 365)
    last_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > last_yr).order_by(Measurement.date).all()

    precipitation_data = []
    for i in precipitation:
        data = {}
        data['date'] = precipitation[0]
        data['prcp'] = precipitation[1]
        precipitation_data.append(data)
 # Return the JSON representation of your dictionary       
    return jsonify(precipitation_data)

@app.route("/api.v1.0/stations")
def stations():
    station_results = session.query(Station.station).all()
    station_all = list(np.ravel(station_results))
    return jsonify(station_all)

@app.route("/api/v1.0/tobs")
def tobs():
# Query the dates and temperature observations of the most active
# station for the last year of data.
    most_active = session.query(Station.station, func.count(Station.station)).group_by(Station.station).all()
    #session.query(Table.column, func.count(Table.column)).group_by(Table.column).all
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >='2016-08-23', Station.station=='USC00519397').all()
    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def get_start(start):
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
# or start-end range    

    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    start_list = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        start_list.append(tobs_dict)

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def get_start_end(start, end):
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
# or start-end range    

    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()

    start_end = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        start_end.append(tobs_dict)

    return jsonify(start_end)

# Bonus
@app.route("/api/v1.0/bonus")
def bonus():
    december_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).filter(extract('month', Measurement.date) == 12).all()

    
    december_list = []
    for min,avg,max in december_temp:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        december_list.append(december_temp)


    june_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),
        func.max(Measurement.tobs)).filter(extract('month', Measurement.date) == 6).all()

    
    june_list = []
    for min,avg,max in june_temp:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        june_list.append(june_temp)
    
    return jsonify(december_list, june_list) 
                                 
if __name__ == '__main__':
     app.run(debug=True)   
