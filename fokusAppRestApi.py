import os
import re
import click
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

app = Flask(__name__)
app.config["DEBUG"] = True

uri = "postgresql+psycopg2://jcrmzxcrgqnria:9e5ddac9f8d1d2b5cd2fc9621d3748ae4f18d4ae9a14c695a8282ef93c446709@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com:5432/ddj8mm4n4oaccb"
if uri.startswith("postgres+psycopg2://"):
    uri = uri.replace("postgres+psycopg2://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_URL'] = uri
db = SQLAlchemy(app)

#==========================================================================Creating Tables===========================================================================

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    notes = db.relationship('Notes', backref='account')
    quotes = db.relationship('Quotes', backref='account')
    events = db.relationship('Events', backref='account')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120), unique=True)
    content=db.Column(db.String(500), unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timedate = db.Column(db.String(50), unique=False)
    title = db.Column(db.String(50), unique=False)
    status = db.Column(db.Boolean, unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

#============================================================================Api Home Page============================================================================

@app.route('/')
def index():
    return render_template("index.html")

#==========================================================================Account Info Methods=======================================================================

@app.route('/accounts', methods=['GET'])
def getAccounts():
    getAccountID = request.args.get("id")
    output = []

    if getAccountID is None:
        allAccounts = Account.query.all()
        for account in allAccounts:
            currAccount = {}
            currAccount['id'] = account.id
            currAccount['email'] = account.email
            output.append(currAccount)
    else:
        account = Account.query.get(getAccountID)
        currAccount = {}
        currAccount['id'] = account.id
        currAccount['email'] = account.email
        output.append(currAccount)

    return jsonify(output)

@app.route('/accounts', methods=['POST'])
def postAccounts():
    accountData = request.get_json()
    account = Account(email=accountData['email'])
    db.session.add(account)
    db.session.commit()
    db.session.close()

    return jsonify(accountData)

#==========================================================================Quotes Info Methods=======================================================================

@app.route('/quotes', methods=['GET'])
def getQuotes():
    getQuoteID = request.args.get("id")
    output = []

    if getQuoteID is None:
        allQuotes = Quotes.query.all()
        for quote in allQuotes:
            currQuote = {}
            currQuote['id'] = quote.id
            currQuote['content'] = quote.content
            currQuote['account_id'] = quote.account_id
            output.append(currQuote)
    else:
        quote = Quotes.query.get(getQuoteID)
        currQuote = {}
        currQuote['id'] = quote.id
        currQuote['content'] = quote.content
        currQuote['account_id'] = quote.account_id
        output.append(currQuote)

    return jsonify(output)

@app.route('/quotes', methods=['POST'])
def postQuotes():
    quoteData = request.get_json()
    quote = Quotes(id=quoteData['id'], content=quoteData['content'], account_id=quoteData['account_id'])
    db.session.add(quote)
    db.session.commit()
    db.session.close()
    return jsonify(quoteData)

#==========================================================================Notes Info Methods=======================================================================

@app.route('/notes', methods=['GET'])
def getNotes():
    getNotesID = request.args.get("id")
    output = []

    if getNotesID is None:
        allNotes = Notes.query.all()
        for note in allNotes:
            currNote = {}
            currNote['id'] = note.id
            currNote['title'] = note.title
            currNote['content'] = note.content
            currNote['account_id'] = note.account_id
            output.append(currNote)
    else:
        note = Notes.query.get(getNotesID)
        currNote = {}
        currNote['id'] = note.id
        currNote['title'] = note.title
        currNote['content'] = note.content
        currNote['account_id'] = note.account_id
        output.append(currNote)

    return jsonify(output)

@app.route('/notes', methods=['POST'])
def postNotes():
    noteData = request.get_json()
    note = Notes(id=noteData['id'], title=noteData['title'], content=noteData['content'], account_id=noteData['account_id'])
    db.session.add(note)
    db.session.commit()
    db.session.close()
    return jsonify(noteData)

#=========================================================================Schedule Info Methods=====================================================================

@app.route('/events', methods=['GET'])
def getEvents():
    getEventsID = request.args.get("id")
    output = []

    if getEventsID is None:
        allEvents = Events.query.all()
        for event in allEvents:
            currEvent = {}
            currEvent['id'] = event.id
            currEvent['timedate'] = event.timedate
            currEvent['title'] = event.title
            currEvent['status'] = event.status
            currEvent['account_id'] = event.account_id
            output.append(currEvent)
    else:
        event = Events.query.get(getEventsID)
        currEvent = {}
        currEvent['id'] = event.id
        currEvent['timedate'] = event.timedate
        currEvent['title'] = event.title
        currEvent['status'] = event.status
        currEvent['account_id'] = event.account_id
        output.append(currEvent)

    return jsonify(output)

@app.route('/events', methods=['POST'])
def postEvents():
    eventData = request.get_json()
    event = Events(id=eventData['id'], timedate=eventData['timedate'], title=eventData['title'], status=eventData['status'], account_id=eventData['account_id'])
    db.session.add(event)
    db.session.commit()
    db.session.close()
    return jsonify(eventData)



if __name__ == "__main__":
    app.run()
