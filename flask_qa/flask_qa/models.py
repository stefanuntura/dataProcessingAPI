from .extensions import db

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
