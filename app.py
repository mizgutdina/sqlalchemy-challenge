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


# @app.route("/api/v1.0/temp/start/end")
# def temps():
#     # Create session (link) from Python to the DB
#     session = Session(engine)

    
#     # Return a JSON list of stations from the dataset.
#     start_only = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.station=='USC00519281').filter(Measurement.date == ?????????????).all()


#     session.close()

#     # Convert list of tuples into normal list
#     all_temps = list(np.ravel(start_only))
    
#     # Return the JSON representation of your dictionary.
#     return jsonify(all_temps)




# @app.route("/api/v1.0/passengers")
# def passengers():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of passenger data including the name, age, and sex of each passenger"""
#     # Query all passengers
#     results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
