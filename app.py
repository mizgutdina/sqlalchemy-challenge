import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# @app.route("/")
# def welcome():
    #"""List all available api routes."""
    #return (f"Available Routes:<br/>" f"/api/v1.0/precipitation <br/>" f"/api/v1.0/stations <br/>" f"/api/v1.0/tobs")
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def prcps():
    # Create session (link) from Python to the DB
    session = Session(engine)

    
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_prcps = list(np.ravel(results))
    
    # Return the JSON representation of your dictionary.
    return jsonify(all_prcps)

@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    
    # Return a JSON list of stations from the dataset.
    just_station_names = session.query(Station.id, Station.station, Station.name).all()


    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(just_station_names))
    
    # Return the JSON representation of your dictionary.
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    
    # Return a JSON list of stations from the dataset.
    temp_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').all()


    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(temp_data))
    
    # Return the JSON representation of your dictionary.
    return jsonify(all_tobs)


@app.route("/api/v1.0/temp/start/end")
def temps():
    # Create session (link) from Python to the DB
    session = Session(engine)

    start_date = input('Please enter vacation start date:') 
    end_date = input('Please enter vacation end date:') 
    
    # # Return Tmin, Tmax, Tavg
    if end_date == 'NULL': 
        start_only_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start_date).all()
        
        session.close()

        
        all_start_only_results = []
        for func.min, func.max, func.avg in all_start_only_results:
            start_only_dict = {}
            start_only_dict["TMIN"] = func.min
            start_only_dict["TMAX"] = func.max
            start_only_dict["TAVG"] = func.avg
            all_start_only_results.append(start_only_dict)

        return jsonify(all_start_only_results)

    else:
        end_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        
        session.close()

        
        all_end_results = []
        for func.min, func.max, func.avg in all_end_results:
            end_dict = {}
            end_dict["TMIN"] = func.min
            end_dict["TMAX"] = func.max
            end_dict["TAVG"] = func.avg
            all_end_results.append(end_dict)

        return jsonify(all_end_results)




if __name__ == '__main__':
    app.run(debug=True)
