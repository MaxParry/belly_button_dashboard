import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect, create_engine, func

from flask import Flask, render_template, jsonify

# Database Setup
engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

# Reflecting existing database into new model
Base = automap_base()
# Reflicting the tables
Base.prepare(engine, reflect=True)

# Save reference to each table in database (3)
Otu = Base.classes.otu
Samples = Base.classes.samples
Samples_metadata = Base.classes.samples_metadata

# Create link from Python to database
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def index():
    # testing query of database and rendering result
    # this page will eventually return dashboard homepage
    getback = session.query(Samples_metadata.ETHNICITY).all()
    response = list(np.ravel(getback))
    return render_template('index.html', test=response)

@app.route("/names")
def names():
    namedata = session.query(Samples_metadata.SAMPLEID).all()
    namelist = list(np.ravel(namedata))
    return jsonify(results=namelist.tolist())
    # START HERE
    # working on this app route, looks like flask
    # doesn't want to return a pure list. Works fine
    # if putting the list into a template and rendering,
    # but not alone.

    # also, the data appears to be in int64 type, which
    # may require flask's JSONEncoder to interpret

    # look in chapter 15 for how to return jsons

if __name__ == '__main__':
    app.run(debug=True)
