import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
print(engine)
Base = automap_base()
print(Base)
Base.prepare(autoload_with=engine)
print(Base.classes.keys())
