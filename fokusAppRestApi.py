import os
import re
import click
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext

app = Flask(__name__)
app.config["DEBUG"] = True

#uri = "postgres://postgres:Admin123@localhost:5432/fokusdatabase"
uri = "postgresql+psycopg2://jcrmzxcrgqnria:9e5ddac9f8d1d2b5cd2fc9621d3748ae4f18d4ae9a14c695a8282ef93c446709@ec2-34-255-134-200.eu-west-1.compute.amazonaws.com:5432/ddj8mm4n4oaccb"
if uri.startswith("postgres+psycopg2://"):
    uri = uri.replace("postgres+psycopg2://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_URL'] = uri
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db = SQLAlchemy(app)

#==========================================================================Creating Tables===========================================================================

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    notes = db.relationship('Notes', backref='account')
    quotes = db.relationship('Quotes', backref='account')
    events = db.relationship('Events', backref='account')
    sessions = db.relationship('Sessions', backref='account')

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject=db.Column(db.String(255), unique=False)
    title=db.Column(db.String(120), unique=True)
    content=db.Column(db.String(500), unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    title = db.Column(db.String(50), unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    duration = db.Column(db.Integer, unique=False)
    account_id=db.Column(db.Integer, db.ForeignKey('account.id'))

#============================================================================Api Home Page============================================================================

@app.route('/')
def index():
    return render_template("index.html")

#==========================================================================Account Info Methods=======================================================================

@app.route('/accounts', methods=['GET'])
def getAccounts():
    getAccountEmail = request.args.get("email")
    output = []

    if getAccountEmail is None:
        allAccounts = Account.query.all()
        for account in allAccounts:
            currAccount = {}
            currAccount['id'] = account.id
            currAccount['email'] = account.email
            output.append(currAccount)
    else:
        account = Account.query.filter_by(email=getAccountEmail).first()
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
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no id specified"
    else:
        quotes = Quotes.query.filter_by(account_id=getUserID).all()
        for quote in quotes:
            currQuote = {}
            currQuote['id'] = quote.id
            currQuote['content'] = quote.content
            currQuote['account_id'] = quote.account_id
            output.append(currQuote)

    return jsonify(output)

@app.route('/quotes', methods=['POST'])
def postQuotes():
    quoteData = request.get_json()
    quote = Quotes(content=quoteData['content'], account_id=quoteData['account_id'])
    db.session.add(quote)
    db.session.commit()
    db.session.close()
    return jsonify(quoteData)

#==========================================================================Notes Info Methods=======================================================================

@app.route('/notes', methods=['GET'])
def getNotes():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no id specified"
    else:
        notes = Notes.query.filter_by(account_id=getUserID).all()
        for note in notes:
            currNote = {}
            currNote['id'] = note.id
            currNote['subject'] = note.subject
            currNote['title'] = note.title
            currNote['content'] = note.content
            currNote['account_id'] = note.account_id
            output.append(currNote)

    return jsonify(output)

@app.route('/notes', methods=['POST'])
def postNotes():
    noteData = request.get_json()
    note = Notes(subject=noteData['subject'], title=noteData['title'], content=noteData['content'], account_id=noteData['account_id'])
    db.session.add(note)
    db.session.commit()
    db.session.close()
    return jsonify(noteData)

@app.route('/notesUpdate', methods=['POST'])
def updateNotes():
    noteData = request.get_json()
    updatedNote = Notes.query.filter_by(id=noteData['id']).update(dict(content=noteData['content']))
    db.session.commit()
    db.session.close()

    return jsonify(noteData)

@app.route('/notesDelete', methods=['GET'])
def deleteNotes():
    getNotesDeleteID = request.args.get("id")
    noteToDelete = Notes.query.get(getNotesDeleteID)
    db.session.delete(noteToDelete)
    db.session.commit()
    db.session.close()

    return "deleted note"


#=========================================================================Schedule Info Methods=====================================================================

@app.route('/events', methods=['GET'])
def getEvents():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no id specified"
    else:
        events = Events.query.filter_by(account_id=getUserID).all()
        for event in events:
            currEvent = {}
            currEvent['id'] = event.id
            currEvent['time'] = event.time
            currEvent['date'] = event.date
            currEvent['title'] = event.title
            currEvent['account_id'] = event.account_id
            output.append(currEvent)

    return jsonify(output)

@app.route('/events', methods=['POST'])
def postEvents():
    eventData = request.get_json()
    event = Events(date=eventData['date'], time=eventData['time'], title=eventData['title'], account_id=eventData['account_id'])
    db.session.add(event)
    db.session.commit()
    db.session.close()
    return jsonify(eventData)

@app.route('/eventsDelete', methods=['GET'])
def deleteEvents():
    getEventsDeleteID = request.args.get("id")
    eventToDelete = Events.query.get(getEventsDeleteID)
    db.session.delete(eventToDelete)
    db.session.commit()
    db.session.close()

    return "deleted event"

#=========================================================================Sessions Info Methods=====================================================================

@app.route('/sessions', methods=['GET'])
def getSessions():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no id specified"
    else:
        sessions = Sessions.query.filter_by(account_id=getUserID).all()
        for session in sessions:
            currSession = {}
            currSession['id'] = session.id
            currSession['date'] = session.date
            currSession['time'] = session.time
            currSession['duration'] = session.duration
            currSession['account_id'] = session.account_id
            output.append(currSession)

    return jsonify(output)

@app.route('/sessions', methods=['POST'])
def postSessions():
    sessionData = request.get_json()
    session = Sessions(date=sessionData['date'], time=sessionData['time'], duration=sessionData['duration'], account_id=sessionData['account_id'])
    db.session.add(session)
    db.session.commit()
    db.session.close()
    return jsonify(sessionData)

if __name__ == "__main__":
    app.run()
