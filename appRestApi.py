from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from Modules.Account.GET import getAccount
from Modules.Account.INSERT import insertAccounts
from Modules.Account.UPDATE import updateAccounts
from Modules.Account.DELETE import deleteAccounts
from Modules.Events.GET import getEvent
from Modules.Events.INSERT import insertEvents
from Modules.Events.UPDATE import updateEvents
from Modules.Events.DELETE import deleteEvents
from Modules.Notes.GET import getNote
from Modules.Notes.INSERT import insertNotes
from Modules.Notes.UPDATE import updateNote
from Modules.Notes.DELETE import deleteNote
from Modules.Quotes.GET import getQuote
from Modules.Quotes.INSERT import insertQuotes
from Modules.Quotes.UPDATE import updateQuotes
from Modules.Quotes.DELETE import deleteQuotes
from Modules.Sessions.GET import getSession
from Modules.Sessions.INSERT import insertSessions
from Modules.Sessions.UPDATE import updateSessions
from Modules.Sessions.DELETE import deleteSessions

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
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))


class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    title = db.Column(db.String(50), unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), unique=False)
    time = db.Column(db.String(50), unique=False)
    duration = db.Column(db.Integer, unique=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))


# =========================================================================================Api Home Page============================================================================

@app.route('/')
def index():
    return render_template("index.html")

#Account Blueprints
app.register_blueprint(getAccount)
app.register_blueprint(insertAccounts)
app.register_blueprint(updateAccounts)
app.register_blueprint(deleteAccounts)

#Event Blueprints
app.register_blueprint(getEvent)
app.register_blueprint(insertEvents)
app.register_blueprint(updateEvents)
app.register_blueprint(deleteEvents)

#Notes Blueprints
app.register_blueprint(getNote)
app.register_blueprint(insertNotes)
app.register_blueprint(updateNote)
app.register_blueprint(deleteNote)

#Quotes Blueprints
app.register_blueprint(getQuote)
app.register_blueprint(insertQuotes)
app.register_blueprint(updateQuotes)
app.register_blueprint(deleteQuotes)

#Sessions Blueprints
app.register_blueprint(getSession)
app.register_blueprint(insertSessions)
app.register_blueprint(updateSessions)
app.register_blueprint(deleteSessions)

if __name__ == "__main__":
    app.run()
