# Import the dependencies.
import numpy as np
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

Precipitation = Base.classes.measurements
Stations= Base.classes.stations
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
def hawaii():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all measurements
    one_year_back=dt.date(2017,8,23)-dt.timedelta(days=365)
    prcp_scores = session.query(Precipitation.date,Precipitation.prcp).filter(Precipitation.date >=one_year_back).all()

    session.close()

    # Convert list of tuples into normal list
    all_rain_dict = []
    for date, prcp in prcp_scores:
        all_rain_dict["date"] = date
        all_rain_dict["prcp"] = prcp
        
        all_rain_dict.append(all_rain_dict)

    return jsonify(all_rain_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all passengers
    stations = session.query(Stations).all()

    session.close()

    all_stations = list(np.ravel(stations))
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all measurements
    temp_freq= session.query(Precipitation.tobs,func.count(Precipitation.tobs)).\
              filter((Precipitation.station) == "USC00519281").\
              group_by(Precipitation.tobs).\
              order_by(Precipitation.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temp_freq))
    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all measurements after start date
    temp_min= session.query(Precipitation.tobs,func.min(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start'])).all()
    temp_max= session.query(Precipitation.tobs,func.max(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start'])).all()
    temp_avg= session.query(Precipitation.tobs,func.avg(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start'])).all()
    
    
    session.close()

    # Convert list of tuples into normal list
    temp_stats = list(np.ravel(temp_min,temp_max, temp_avg))
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all measurements after start date
    temp_min= session.query(Precipitation.tobs,func.min(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start']) and (Precipitation.date<=['end'])).all()
    temp_max= session.query(Precipitation.tobs,func.max(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start'])and (Precipitation.date<=['end'])).all()
    temp_avg= session.query(Precipitation.tobs,func.avg(Precipitation.tobs)).\
                filter((Precipitation.date >= ['start'])and (Precipitation.date<=['end'])).all()

    session.close()

    # Convert list of tuples into normal list
    all_temps = list(np.ravel(temp_min,temp_max, temp_avg))
    return jsonify(all_temps)


if __name__ == '__main__':
    app.run(debug=True)