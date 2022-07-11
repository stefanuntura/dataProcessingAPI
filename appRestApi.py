import json
from jsonschema import Draft7Validator
from sqlalchemy import false
import xmltodict
import xml.etree.ElementTree as ET
from lxml import etree
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import Modules.Util
from Modules.Account import GET, INSERT, UPDATE, DELETE
from Modules.Events import GET, INSERT, UPDATE, DELETE
from Modules.Notes import GET, INSERT, UPDATE, DELETE
from Modules.Quotes import GET, INSERT, UPDATE, DELETE
from Modules.Sessions import GET, INSERT, UPDATE, DELETE

app = Flask(__name__)
# Set to false before turning in
app.config["DEBUG"] = True

# uri = "postgres://postgres:Admin123@localhost:5432/fokusdatabase"
uri = "postgresql+psycopg2://jcrmzxcrgqnria:9e5ddac9f8d1d2b5cd2fc9621d3748ae4f18d4ae9a14c695a8282ef93c446709@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com:5432/ddj8mm4n4oaccb"
if uri.startswith("postgres+psycopg2://"):
    uri = uri.replace("postgres+psycopg2://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_URL'] = uri
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)


# ====================================================================swagger specific=======================================================================#
# generator = Generator.of(SwaggerVersion.VERSION_THREE)

# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Stix-Database-API-Assignment"
#     }
# )

# @generator.security(SecurityType.BEARER_AUTH)
# @generator.response(status_code=200, schema={'id': 10, 'name': 'test_object'})
# @generator.request_body({'id': 10, 'name': 'test_object'})
# @SWAGGERUI_BLUEPRINT.route('/objects/<int:object_id>', methods=['PUT'])
# def update_object(object_id):
#     return jsonify({'id': 1, 'name': 'test_object_name'}), 201

# swagger_destination_path = '/static/swagger.yaml'
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# #generator.generate_swagger(app, destination_path=swagger_destination_path)

# ==========================================================================Models===========================================================================

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    notes = db.relationship('Notes', backref='account')
    quotes = db.relationship('Quotes', backref='account')
    events = db.relationship('Events', backref='account')
    sessions = db.relationship('Sessions', backref='account')


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), unique=False)
    title = db.Column(db.String(120), unique=True)
    content = db.Column(db.String(500), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('id'))


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('id'))


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    title = db.Column(db.String(50), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('id'))


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    duration = db.Column(db.Integer, unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('id'))


# =========================================================================================Api Home Page============================================================================

@app.route('/')
def index():
    return render_template("index.html")


# ===========================================================================Account methods===================================================================================

# GET
@app.route('/accounts', methods=['GET'])
def getAccount():
    return GET.getAccounts()


# INSERT
@app.route('/accounts', methods=['POST'])
def insertAccount():
    return INSERT.insertAccount()


# UPDATE
@app.route('/accountUpdate', methods=['POST'])
def updateAccount():
    return UPDATE.updateAccount()


# DELETE
@app.route('/accountDelete', methods=['POST'])
def deleteAccount():
    return DELETE.deleteAccount()


# ===========================================================================Event methods===================================================================================

# GET
@app.route('/events', methods=['GET'])
def getEvent():
    return GET.getEvents()


# INSERT
@app.route('/events', methods=['POST'])
def insertEvent():
    return INSERT.insertEvent()


# UPDATE
@app.route('/eventUpdate', methods=['POST'])
def updateEvent():
    return UPDATE.updateEvent()


# DELETE
@app.route('/eventDelete', methods=['POST'])
def deleteEvent():
    return DELETE.deleteEvent()


# ===========================================================================Notes methods===================================================================================
# GET
@app.route('/notes', methods=['GET'])
def getNote():
    return GET.getNotes()


# INSERT
@app.route('/notes', methods=['POST'])
def insertNote():
    return INSERT.insertNote()


# UPDATE
@app.route('/noteUpdate', methods=['POST'])
def updateNote():
    return UPDATE.updateNotes()


# DELETE
@app.route('/noteDelete', methods=['POST'])
def deleteNote():
    return DELETE.deleteNotes()


# ===========================================================================Quotes methods===================================================================================
# GET
@app.route('/quotes', methods=['GET'])
def getQuotes():
    return GET.getQuotes()


# INSERT
@app.route('/quotes', methods=['POST'])
def insertQuotes():
    return INSERT.insertQuote()


# UPDATE
@app.route('/quoteUpdate', methods=['POST'])
def updateQuotes():
    return UPDATE.updateQuote()


# DELETE
@app.route('/quoteDelete', methods=['POST'])
def deleteQuotes():
    return DELETE.deleteQuote()


# ===========================================================================Sessions methods===================================================================================
# GET
@app.route('/sessions', methods=['GET'])
def getSessions():
    return GET.getSessions()


# INSERT
@app.route('/sessions', methods=['POST'])
def insertSessions():
    return INSERT.insertSession()


# UPDATE
@app.route('/sessionUpdate', methods=['POST'])
def updateSessions():
    return UPDATE.updateSession()


# DELETE
@app.route('/sessionDelete', methods=['POST'])
def deleteSessions():
    return DELETE.deleteSession()


# ==============================================================================Start the application=====================================================================


if __name__ == "__main__":
    app.run()
