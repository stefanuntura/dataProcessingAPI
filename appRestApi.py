from io import StringIO
import json
from jsonschema import Draft7Validator
from sqlalchemy import false
import xmltodict
import xml.etree.ElementTree as ET
from lxml import etree
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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

#====================================================================swagger specific=======================================================================#
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

#==========================================================================Models===========================================================================

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

#=========================================================================================Api Home Page============================================================================

@app.route('/')
def index():
    return render_template("index.html")

#===========================================================================Account info methods===================================================================================
#Files locations
accountsGetJsonSchemaLocation = 'jsonSchemas/Account/accountsGetSchema.json'
accountGetJsonSchemaLocation = 'jsonSchemas/Account/accountGetSchema.json'
accountInsertSchemaLocation = 'jsonSchemas/Account/accountInsertSchema.json'
accountDeleteSchemaLocation = 'jsonSchemas/Account/accountDeleteSchema.json'
accountUpdateSchemaLocation = 'jsonSchemas/Account/accountUpdateSchema.json'

accountsReceivedJsonDataLocation = 'data/accountsReceived.json'
accountReceivedJsonDataLocation = 'data/accountReceived.json'

#GET
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
        
        #Validate and save json response
        if validateJsonResponse(accountsGetJsonSchemaLocation, output) == False:
            #Save received json data to "received" file
            saveJsonResponse(accountsReceivedJsonDataLocation, output)

            # #Convert received json data to XML
            # convertNotesJsonToXml(notesReceivedJsonDataLocation, notesXmlFileLocation, len(output))
        
            # #Convert XML data to a more structured JSON to "converted" file
            # convertFromXMLToJSON(notesXmlFileLocation, notesJsonDataConvertedFromXmlLocation)
        else:
            return "There were errors while validating the json data"

    else:
        account = Account.query.filter_by(email=getAccountEmail).first()
        currAccount = {}
        currAccount['id'] = account.id
        currAccount['email'] = account.email
        output.append(currAccount)

        #Validate and save json response
        if validateJsonResponse(accountGetJsonSchemaLocation, output) == False:
            #Save received json data to "received" file
            saveJsonResponse(accountReceivedJsonDataLocation, output)

        #     #Convert received json data to XML
        #     convertNotesJsonToXml(notesReceivedJsonDataLocation, notesXmlFileLocation, len(output))
        
        #     #Convert XML data to a more structured JSON to "converted" file
        #     convertFromXMLToJSON(notesXmlFileLocation, notesJsonDataConvertedFromXmlLocation)
        # else:
        #     return "There were errors while validating the json data"

    return jsonify(output)

#=================================================================================================================================================================================
#INSERT
#Checks if account already exists
#If entry already exists, returns string "Account already exists!"
#If entry does not exist, inserts sent entry in database
@app.route('/accounts', methods=['POST'])
def insertAccount():
    if(request.is_json):
        accountData = request.get_json()

        #Validates sent JSON
        if validateJsonResponse(accountInsertSchemaLocation, accountData) == False:
            exists = bool(db.session.query(Account).filter_by(email=accountData['email']).first())

            if(exists):
                return "Account already exists!"
            else:
                insertAccountJson(accountData)
                return "Successfully inserted account using json!"
        else: 
            return "Json input validation failed!"
    else:
        accountData = request.get_data()

        #Transforms data received into a non-flat xml file
        info = ET.fromstring(accountData)
        tree = ET.ElementTree(info)

        # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
        #     print("Successfuly validated xml!")

        #Iterates over xml and finds necessarry data belonging to tags
        for item in tree.iter('account'):
            accountEmail = item.find('email').text
        
            exists = bool(db.session.query(Account).filter_by(email=accountEmail).first())

            if(exists):
                return "Account already exists!"
            else:
                insertAccountXml(accountData)
                return "Successfuly inserted account using xml!"

    return jsonify(accountData)

def insertAccountJson(accountData):
    #Validates sent JSON before insert
    if validateJsonResponse(accountInsertSchemaLocation, accountData) == False:
        account = Account(email=accountData['email'])
        db.session.add(account)
        db.session.commit()
        db.session.close()

    else: 
        return "Json input validation failed!"

def insertAccountXml(accountData):
    #Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('account'):
        newAccountEmail = item.find('email').text
    
    account = Account(email=newAccountEmail)
    db.session.add(account)
    db.session.commit()
    db.session.close()

#UPDATE
@app.route('/accountUpdate', methods=['POST'])
def updateAccount():
    if(request.is_json):
        accountData = request.get_json()
    
        # Validates sent JSON before update
        if validateJsonResponse(accountUpdateSchemaLocation, accountData) == False:
            Account.query.filter_by(id=accountData['id']).update(dict(email=accountData['email']))
            db.session.commit()
            db.session.close()

    else:
        updateAccountXml()

    return "Successfuly updated account!"

#UPDATE WITH XML
def updateAccountXml():
    accountData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('account'):
        updatedAccountID = item.find('id').text
        updatedAccountContent = item.find('email').text

    Account.query.filter_by(id=updatedAccountID).update(dict(email=updatedAccountContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated account!"


#DELETE
@app.route('/accountDelete', methods=['POST'])
def deleteAccount():
    if(request.is_json):
        accountData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(accountDeleteSchemaLocation, accountData) == False:
            accountToDelete = Account.query.get(accountData['id'])
            db.session.delete(accountToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteAccountXml()

    return "Successfuly deleted account!"

#DELETE BY XML POST
def deleteAccountXml():
    accountID = ''
    accountData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('account'):
        print(item)
        accountID = item.find('id').text
    
    #Deletes note based on id specified in xml sent
    accountToDelete = Account.query.get(accountID)
    db.session.delete(accountToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted account!"

#==========================================================================Quotes Info Methods=======================================================================
quoteGetSchemaLocation = 'jsonSchemas/Quote/quoteGetSchema.json'
quoteInsertSchemaLocation = 'jsonSchemas/Quote/quoteInsertSchema.json'
quoteUpdateJsonSchemaLocation = 'jsonSchemas/Quote/quoteUpdateSchema.json'
quoteDeleteJsonSchemaLocation = 'jsonSchemas/Quote/quoteDeleteSchema.json'

quoteReceivedJsonDataLocation = 'data/quoteReceived.json'

#GET
@app.route('/quotes', methods=['GET'])
def getQuotes():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
    else:
        quotes = Quotes.query.filter_by(account_id=getUserID).all()
        for quote in quotes:
            currQuote = {}
            currQuote['id'] = quote.id
            currQuote['content'] = quote.content
            currQuote['account_id'] = quote.account_id
            output.append(currQuote)

        if validateJsonResponse(quoteGetSchemaLocation, output) == False:
            #Save received json data to "received" file
            saveJsonResponse(quoteReceivedJsonDataLocation, output)
        
        else:
            return "There were errors while validating the json data"
        
    return jsonify(output)

#INSERT
@app.route('/quotes', methods=['POST'])
def insertQuote():
    if(request.is_json):
        quoteData = request.get_json()

        #Validates sent JSON before insert
        if validateJsonResponse(quoteInsertSchemaLocation, quoteData) == False:
            quote = Quotes(content=quoteData['content'], account_id=quoteData['account_id'])
            db.session.add(quote)
            db.session.commit()
            db.session.close()
        
        else: 
            return "Json input validation failed!"

    else:
        insertQuoteXml()

    return "Successfuly inserted quote!"

def insertQuoteXml():
    quoteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        newQuoteContent = item.find('content').text
        newQuoteAccountID = item.find('accountID').text
    
    quote = Quotes(content=newQuoteContent, account_id=newQuoteAccountID)
    db.session.add(quote)
    db.session.commit()
    db.session.close()

    return "Successfully inserted quote!"

#UPDATE
@app.route('/quoteUpdate', methods=['POST'])
def updateQuote():
    if(request.is_json):
        quoteData = request.get_json()
    
        # Validates sent JSON before update
        if validateJsonResponse(quoteUpdateJsonSchemaLocation, quoteData) == False:
            Quotes.query.filter_by(id=quoteData['id']).update(dict(content=quoteData['content']))
            db.session.commit()
            db.session.close()

    else:
        updateQuoteXml()

    return "Successfuly updated quote!"

#UPDATE WITH XML
def updateQuoteXml():
    quoteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        updatedQuoteID = item.find('id').text
        updatedQuoteContent = item.find('content').text

    Quotes.query.filter_by(id=updatedQuoteID).update(dict(content=updatedQuoteContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated quote!"

#DELETE
@app.route('/quoteDelete', methods=['POST'])
def deleteQuote():
    if(request.is_json):
        quoteData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(quoteDeleteJsonSchemaLocation, quoteData) == False:
            quoteToDelete = Quotes.query.get(quoteData['id'])
            db.session.delete(quoteToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteQuoteXml()

    return "Successfuly deleted quote!"

#DELETE BY XML POST
def deleteQuoteXml():
    updatedQuoteID = ''
    quoteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        updatedQuoteID = item.find('id').text
    
    #Deletes note based on id specified in xml sent
    quoteToDelete = Quotes.query.get(updatedQuoteID)
    db.session.delete(quoteToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted quote!"

#==========================================================================Notes Info Methods=======================================================================
#Files locations
notesGetJsonSchemaLocation = 'jsonSchemas/Note/notesGetSchema.json'
notesInsertJsonSchemaLocation = 'jsonSchemas/Note/notesInsertSchema.json'
notesUpdateJsonSchemaLocation = 'jsonSchemas/Note/notesUpdateSchema.json'
notesDeleteJsonSchemaLocation = 'jsonSchemas/Note/notesDeleteSchema.json'

notesReceivedJsonDataLocation = 'data/notesReceived.json'
notesXmlFileLocation = 'xml/notes.xml'
notesJsonDataConvertedFromXmlLocation = 'data/convertedReceivedNotes.json'

notesUpdateReceivedXmlInfoLocation = 'xml/noteUpdate.xml'
notesUpdateInformationFromReceivedXmlJsonFileLocation = 'data/updateNoteInformation.json'

#GET
@app.route('/notes', methods=['GET'])
def getNotes():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
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

        #Validate and save json response
        if validateJsonResponse(notesGetJsonSchemaLocation, output) == False:
            #Save received json data to "received" file
            saveJsonResponse(notesReceivedJsonDataLocation, output)

            #Convert received json data to XML
            convertNotesJsonToXml(notesReceivedJsonDataLocation, notesXmlFileLocation, len(output))
        
            #Convert XML data to a more structured JSON to "converted" file
            convertFromXMLToJSON(notesXmlFileLocation, notesJsonDataConvertedFromXmlLocation)
        else:
            return "There were errors while validating the json data"
        
    return jsonify(output)

#=================================================================================================================================================================================
#INSERT
@app.route('/notes', methods=['POST'])
def insertNote():
    if(request.is_json):
        noteData = request.get_json()

        #Validates sent JSON before insert
        if validateJsonResponse(notesInsertJsonSchemaLocation, noteData) == False:
            note = Notes(subject=noteData['subject'], title=noteData['title'], content=noteData['content'], account_id=noteData['account_id'])
            db.session.add(note)
            db.session.commit()
            db.session.close()
        else: 
            return "Json input validation failed!"

    else:
        insertNoteXml()
    
    return "Successfully added note!"

#INSERT WITH XML
def insertNoteXml():
    noteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)
    tree.write('xml/noteInsertXml.xml')

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        newNoteSubject = item.find('subject').text
        newNoteTitle = item.find('title').text
        newNoteContent = item.find('content').text
        newNoteAccountID = item.find('accountID').text
    
    note = Notes(subject=newNoteSubject, title=newNoteTitle, content=newNoteContent, account_id=newNoteAccountID)
    db.session.add(note)
    db.session.commit()
    db.session.close()

    return "Successfully added note!"

#=================================================================================================================================================================================
#UPDATE
@app.route('/noteUpdate', methods=['POST'])
def updateNotes():
    if(request.is_json):
        noteData = request.get_json()
    
        # Validates sent JSON before update
        if validateJsonResponse(notesUpdateJsonSchemaLocation, noteData) == False:
            Notes.query.filter_by(id=noteData['id']).update(dict(content=noteData['content']))
            db.session.commit()
            db.session.close()

    else:
        updateNotesXml()

    return "Successfuly updated note!"

#UPDATE WITH XML
def updateNotesXml():
    noteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)
    tree.write(notesUpdateReceivedXmlInfoLocation)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        updatedNoteID = item.find('id').text
        updatedNoteContent = item.find('content').text

    Notes.query.filter_by(id=updatedNoteID).update(dict(content=updatedNoteContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated note!"


#=================================================================================================================================================================================
#DELETE
@app.route('/noteDelete', methods=['POST'])
def deleteNotes():
    if(request.is_json):
        noteData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(notesDeleteJsonSchemaLocation, noteData) == False:
            noteToDelete = Notes.query.get(noteData['id'])
            db.session.delete(noteToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteNotesXml()

    return "Successfuly deleted note!"

#DELETE BY XML POST
def deleteNotesXml():
    noteToDeleteID = ''
    noteData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        noteToDeleteID = item.find('id').text
    
    #Deletes note based on id specified in xml sent
    noteToDelete = Notes.query.get(noteToDeleteID)
    db.session.delete(noteToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted note!"


#========================================================================================Schedule Info Methods=====================================================================
eventsGetSchemaLocation = 'jsonSchemas/Event/eventsGetSchema.json'
eventInsertSchemaLocation = 'jsonSchemas/Event/eventInsertSchema.json'
eventDeleteJsonSchemaLocation = 'jsonSchemas/Event/eventDeleteSchema.json'
eventUpdateSchemaLocation = 'jsonSchemas/Event/eventUpdateSchema.json'

eventsReceivedJsonDataLocation = 'data/eventsReceived.json'

#GET
@app.route('/events', methods=['GET'])
def getEvents():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
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

        if validateJsonResponse(eventsGetSchemaLocation, output) == False:
            #Save received json data to "received" file
            saveJsonResponse(eventsReceivedJsonDataLocation, output)
        
        else:
            return "There were errors while validating the json data"

    return jsonify(output)

#INSERT
@app.route('/events', methods=['POST'])
def insertEvent():
    if(request.is_json):
        eventData = request.get_json()

        #Validates sent JSON before insert
        if validateJsonResponse(eventInsertSchemaLocation, eventData) == False:
            event = Events(date=eventData['date'], time=eventData['time'], title=eventData['title'], account_id=eventData['account_id'])
            db.session.add(event)
            db.session.commit()
            db.session.close()
        else: 
            return "Json input validation failed!"
    
    else:
        insertEventXml()

    return "Successfully added event!"

#INSERT WITH XML
def insertEventXml():
    eventData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('event'):
        newEventDate = item.find('date').text
        newEventTime = item.find('time').text
        newEventTitle = item.find('title').text
        newEventAccountID = item.find('accountID').text
    
    event = Events(date=newEventDate, time=newEventTime, title=newEventTitle, account_id=newEventAccountID)
    db.session.add(event)
    db.session.commit()
    db.session.close()

    return "Successfully added event!"

#UPDATE
@app.route('/eventUpdate', methods=['POST'])
def updateEvent():
    if(request.is_json):
        eventData = request.get_json()
    
        # Validates sent JSON before update
        if validateJsonResponse(eventUpdateSchemaLocation, eventData) == False:
            Events.query.filter_by(id=eventData['id']).update(dict(date=eventData['date']))
            Events.query.filter_by(id=eventData['id']).update(dict(time=eventData['time']))
            Events.query.filter_by(id=eventData['id']).update(dict(title=eventData['title']))
            db.session.commit()
            db.session.close()

        else:
            return "There were errors while validating the json data"

    else:
        updateEventXml()

    return "Successfuly updated event!"

#UPDATE WITH XML
def updateEventXml():
    eventData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('event'):
        updatedEventID = item.find('id').text
        updatedEventDate = item.find('date').text
        updatedEventTime = item.find('time').text
        updatedEventTitle = item.find('title').text

    Events.query.filter_by(id=updatedEventID).update(dict(date=updatedEventDate))
    Events.query.filter_by(id=updatedEventID).update(dict(time=updatedEventTime))
    Events.query.filter_by(id=updatedEventID).update(dict(title=updatedEventTitle))
    db.session.commit()
    db.session.close()

    return "Successfuly updated event!"

#DELETE
@app.route('/eventDelete', methods=['POST'])
def deleteEvent():
    if(request.is_json):
        eventData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(eventDeleteJsonSchemaLocation, eventData) == False:
            eventToDelete = Events.query.get(eventData['id'])
            db.session.delete(eventToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteEventXml()

    return "Successfuly deleted event!"

#DELETE BY XML POST
def deleteEventXml():
    eventToDeleteID = ''
    eventData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('event'):
        eventToDeleteID = item.find('id').text
    
    #Deletes note based on id specified in xml sent
    eventToDelete = Events.query.get(eventToDeleteID)
    db.session.delete(eventToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted note!"

#=========================================================================Sessions Info Methods=====================================================================
sessionsGetSchemaLocation = 'jsonSchemas/Session/sessionsGetSchema.json'
sessionInsertSchemaLocation = 'jsonSchemas/Session/sessionInsertSchema.json'
sessionUpdateSchemaLocation = 'jsonSchemas/Session/sessionUpdateSchema.json'
sessionDeleteJsonSchemaLocation = 'jsonSchemas/Session/sessionDeleteSchema.json'

sessionsReceivedJsonDataLocation = 'data/sessionsReceived.json'

#GET
@app.route('/sessions', methods=['GET'])
def getSessions():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
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

            if validateJsonResponse(sessionsGetSchemaLocation, output) == False:
                #Save received json data to "received" file
                saveJsonResponse(sessionsReceivedJsonDataLocation, output)
                
            else:
                return "There were errors while validating the json data"

    return jsonify(output)

#INSERT
@app.route('/sessions', methods=['POST'])
def insertSession():
    if(request.is_json):
        sessionData = request.get_json()

        #Validates sent JSON before insert
        if validateJsonResponse(sessionInsertSchemaLocation, sessionData) == False:
            session = Sessions(date=sessionData['date'], time=sessionData['time'], duration=sessionData['duration'], account_id=sessionData['account_id'])
            db.session.add(session)
            db.session.commit()
            db.session.close()
        else: 
            return "Json input validation failed!"
    
    else:
        insertSessionXml()
    
    return "Successfully added session!"

#INSERT WITH XML
def insertSessionXml():
    sessionData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('session'):
        newSessionDate = item.find('date').text
        newSessionTime = item.find('time').text
        newSessionDuration = item.find('duration').text
        newSessionAccountID = item.find('accountID').text
    
    session = Sessions(date=newSessionDate, time=newSessionTime, duration=newSessionDuration, account_id=newSessionAccountID)
    db.session.add(session)
    db.session.commit()
    db.session.close()

    return "Successfully added session!"

#UPDATE
@app.route('/sessionUpdate', methods=['POST'])
def updateSession():
    if(request.is_json):
        sessionData = request.get_json()
    
        # Validates sent JSON before update
        if validateJsonResponse(sessionUpdateSchemaLocation, sessionData) == False:
            Sessions.query.filter_by(id=sessionData['id']).update(dict(date=sessionData['date']))
            Sessions.query.filter_by(id=sessionData['id']).update(dict(time=sessionData['time']))
            Sessions.query.filter_by(id=sessionData['id']).update(dict(duration=sessionData['duration']))
            db.session.commit()
            db.session.close()
        
        else:
            return "There were errors while validating the json data"

    else:
        updateSessionXml()

    return "Successfuly updated session!"

#UPDATE WITH XML
def updateSessionXml():
    sessionData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('session'):
        updatedSessionID = item.find('id').text
        updatedSessionDate = item.find('date').text
        updatedSessionTime = item.find('time').text
        updatedSessionDuration = item.find('duration').text

    Sessions.query.filter_by(id=updatedSessionID).update(dict(date=updatedSessionDate))
    Sessions.query.filter_by(id=updatedSessionID).update(dict(time=updatedSessionTime))
    Sessions.query.filter_by(id=updatedSessionID).update(dict(duration=updatedSessionDuration))
    db.session.commit()
    db.session.close()

    return "Successfuly updated session!"

#DELETE
@app.route('/sessionDelete', methods=['POST'])
def deleteSession():
    if(request.is_json):
        sessionData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(sessionDeleteJsonSchemaLocation, sessionData) == False:
            sessionToDelete = Sessions.query.get(sessionData['id'])
            db.session.delete(sessionToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteSessionXml()

    return "Successfuly deleted session!"

#DELETE BY XML POST
def deleteSessionXml():
    sessionToDeleteID = ''
    sessionData = request.get_data()

    #Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)

    #Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('session'):
        sessionToDeleteID = item.find('id').text
    
    #Deletes note based on id specified in xml sent
    sessionToDelete = Sessions.query.get(sessionToDeleteID)
    db.session.delete(sessionToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted session!"

#=================================================================================Utility functions=====================================================================

# Validate JSON response
# Returns False if error list was empty, meaning validation was successful
# Returns True if error lsit is not empty, meaning there were errors while validating the data

def validateJsonResponse(schemaLocation, dataReceived):
    #Validate schema
    with open(schemaLocation) as schemaFile:
        schema = json.load(schemaFile)
    schemaFile.close()

    validator = Draft7Validator(schema)

    listOfValidationErrors = list(validator.iter_errors(dataReceived))

    if(bool(listOfValidationErrors)):
        print("There were errors while validating the data!")
    else:
        print("Validated successfuly!")

    print("Errors while validating json:", listOfValidationErrors)

    return bool(listOfValidationErrors)

# Validate XML reponse using XSD
def validateXmlResponse(schemaLocation, xmlToValidate):
    #Get schema as string
    schemaFile = open(schemaLocation, 'r')
    fileContent = schemaFile.read()
    schemaFile.close()
    
    #Create schema from string
    xmlschema_doc = etree.fromstring(fileContent)
    xmlschema = etree.XMLSchema(file=schemaLocation)

    xmlschema.validate(xmlschema_doc)

    print("Errors while validating xml:", xmlschema.error_log)
    
    return xmlschema.validate(xmlschema_doc)

# Save JSON response to file

def saveJsonResponse(outputLocation, dataReceived):
    #Create and write response to json file
    with open(outputLocation, 'w') as outfile:
        json.dump(dataReceived, outfile)
    outfile.close()


# Convert Notes from JSON to XML

def convertNotesJsonToXml(jsonFile, xmlFile, volume):
    #Loading json file data to variable data
    with open(jsonFile, "r") as json_file:
        data = json.load(json_file)
    json_file.close()
    
    #Building the root element of the xml file
    root = ET.Element("Notes")

    for i in range(0, volume):
        note = ET.SubElement(root, "Note")
        #Building the subroot elements of the xml file
        ET.SubElement(note, "NoteID").text = str(data[i]["id"])

        accountInfo = ET.SubElement(note, "AccountInfo")
        #Building subelements of account info
        ET.SubElement(accountInfo, "AccountID").text = str(data[i]["account_id"])

        #Building the subroot elements of the xml file
        ET.SubElement(note, "Content").text = str(data[i]["content"])
        ET.SubElement(note, "Subject").text = str(data[i]["subject"])
        ET.SubElement(note, "Title").text = str(data[i]["title"])
    

    #Building the tree of XML elements using the root element
    tree = ET.ElementTree(root)

    #Writing the XML to output file
    tree.write(xmlFile)


#Convert from XML to JSON

def convertFromXMLToJSON(xmlFile, jsonFile):
    with open(xmlFile) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_data = json.dumps(data_dict)

    with open(jsonFile, "w") as json_file:
        json_file.write(json_data)
    json_file.close()
#==============================================================================Start the application=====================================================================


if __name__ == "__main__":
    app.run()
