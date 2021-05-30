import flask
import MySQLdb
import re
from MySQLdb import _mysql
from MySQLdb.constants import FIELD_TYPE
from flask import request, jsonify, json, make_response, render_template

app = flask.Flask(__name__);
app.config["DEBUG"] = True

#=============================================================================#Global, frequently used functions========================================================================

def connect_db():

    global db

    db = _mysql.connect(host = 'localhost', db = 'fokusapp', user = 'root', passwd = '')
    print("Successfully Connected To Database")


def close_db():

    db.close()
    print("Closed database connection")


def fetchDatabaseInfo(infoQuery):

    global result
    global convertedResult

    db.query(infoQuery)
    print("Successfully executed login info query")

    result = db.store_result()
    print("Successfully stored login data")

    convertedResult= str(result.fetch_row())
    print("Successfully fetched login data")

    return convertedResult


def prepareResultedQueryString(queryResult):

    global modifiedQueryResult

    queryResultWithNoStart = queryResult[2:]
    queryResultWithNoEnd = queryResultWithNoStart[:-3]
    shortenedQueryResult = re.sub('b', '', queryResultWithNoEnd)
    print("Successfully substringed the fetched result")

    modifiedQueryResult = re.split(',', shortenedQueryResult)

    return modifiedQueryResult

#===================================================================================#Home page of the API===============================================================================

@app.route('/', methods=['GET'])

def home():
    return render_template("index.html")

#=============================================================================#Requesting QuoteInfo from the API========================================================================

@app.route('/quoteInfo', methods=['GET'])

def quoteInfo():
    quoteID = request.args.get("quoteID")

    connect_db()

    if quoteID is None:
        quoteInfoQuery = """SELECT * FROM quoteoftheday"""
        print("quoteID IS NONE")
    else:
        quoteInfoQuery = """SELECT * FROM quoteoftheday WHERE quoteDay_key = '{}' """.format(quoteID)
        print("quoteID HAS A VALUE")

    fetchDatabaseInfo(quoteInfoQuery)
    prepareResultedQueryString(convertedResult)

    quoteKey = modifiedQueryResult[0]
    quoteText = modifiedQueryResult[1]

    quoteData = {
        "QuoteKey": quoteKey,
        "QuoteText": quoteText
    }

    quoteInfoJsonObject = jsonify(quoteData)
    print("Successfully jsonifed the substringed result")

    close_db()

    return quoteInfoJsonObject
#============================================================================#Requesting QuoteInfo from the API=========================================================================

@app.route('/appInfo', methods=['GET'])

def appInfo():
    connect_db()

    appInfoQuery = """SELECT * FROM app"""

    fetchDatabaseInfo(appInfoQuery)
    prepareResultedQueryString(convertedResult)

    email = modifiedQueryResult[0]
    quoteKey = modifiedQueryResult[1]

    appData = {
        "Email": email,
        "QuoteKey": quoteKey
    }

    appInfoJsonObject = jsonify(appData)
    print("Successfully jsonified the substringed result")

    close_db()

    return appInfoJsonObject



#============================================================================#Requesting NotesInfo from the API=========================================================================

@app.route('/notesInfo', methods=['GET'])

def notesInfo():
    noteID = request.args.get("noteID")
    email = request.args.get("email")

    connect_db()

    if email is None or noteID is None:
        notesInfoQuery = """SELECT * FROM notes"""
        print("email or noteID IS NONE")
    else:
        notesInfoQuery = """SELECT * FROM notes WHERE email = '{}' AND note_id='{}' """.format(email, noteID)
        print("email and noteID HAVE A VALUE")



    fetchDatabaseInfo(notesInfoQuery)
    prepareResultedQueryString(convertedResult)

    note_id = modifiedQueryResult[0]
    email = modifiedQueryResult[1]
    title = modifiedQueryResult[2]

    notesData = {
        "Note_ID": note_id,
        "Email": email,
        "Title": title
    }

    notesInfoJsonObject = jsonify(notesData)
    print("Successfully jsonified the substringed result")

    close_db()

    return notesInfoJsonObject
#============================================================================#Requesting ScheduleInfo from the API=========================================================================

@app.route('/scheduleInfo', methods=['GET'])

def scheduleInfo():
    connect_db()

    scheduleInfoQuery = """SELECT * FROM schedule"""

    fetchDatabaseInfo(scheduleInfoQuery)
    prepareResultedQueryString(convertedResult)

    timedate = modifiedQueryResult[0]
    email = modifiedQueryResult[1]
    eventName = modifiedQueryResult[2]
    timerDuration = modifiedQueryResult[3]
    timerQuantity = modifiedQueryResult[4]
    eventStatus = modifiedQueryResult[5]

    scheduleData = {
        "Timedate": timedate,
        "Email": email,
        "Eventname": eventName,
        "TimerDuration": timerDuration,
        "TimerQuantity": timerQuantity,
        "EventStatus": eventStatus
    }

    scheduleInfoJsonObject = jsonify(scheduleData)
    print("Successfully jsonified the substringed result")

    close_db()

    return scheduleInfoJsonObject

#============================================================================#Upload .txt file to SQL=========================================================================

@app.route('/uploadNotes', methods=['GET'])
def upload():
    noteID = request.args.get("noteID")
    email = request.args.get("email")
    noteContent = request.args.get("content")

    connect_db()

    if email is None or noteID is None:
        flask.redirect(flask.url_for("home"))
        print("email or noteID IS NONE")
    else:
        insertNotesContentQuery = """UPDATE notes SET content = '{}' WHERE email = '{}' AND note_id='{}' """.format(noteContent, email, noteID)
        print("email and noteID HAVE A VALUE")
        print("notes content have been inserted")

    db.query(insertNotesContentQuery)
    print("Successfully inserted the notes")

    close_db()

    return flask.redirect(flask.url_for("home"))

#============================================================================#Update eventStatus column in schedule tableL=========================================================================

@app.route('/scheduleUpdate', methods=['GET'])
def scheduleUpdate():
    email = request.args.get("email")
    eventStatus = request.args.get("eventStatus")

    connect_db()

    updateEventStatusQuery = """UPDATE schedule SET eventStatus = '{}' WHERE email = '{}' """.format(eventStatus, email)

    db.query(updateEventStatusQuery)
    print("Successfully updated the eventStatus field")

    close_db()

    return flask.redirect(flask.url_for("home"))

#============================================================================#Update eventStatus column in schedule tableL=========================================================================

@app.route('/insertEmail', methods=['GET'])
def insertEmail():
    email = request.args.get("email")

    connect_db()

    if email is None:
        flask.redirect(flask.url_for("home"))
        print("Email was not specified")
    else:
        insertEmailQuery = """INSERT INTO app(email) VALUES('{}')""".format(email)

    db.query(insertEmailQuery)
    print("Successfully inserted the email")

    close_db()

    return flask.redirect(flask.url_for("home"))

#============================================================================#Errorhandlers=========================================================================

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

app.run()
