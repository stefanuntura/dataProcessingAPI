import flask
import MySQLdb
import re
from MySQLdb import _mysql
from MySQLdb.constants import FIELD_TYPE
from flask import request, jsonify, json
from flask import make_response

app = flask.Flask(__name__);
app.config["DEBUG"] = True

homePageText = "<h1><center>FokusApp Rest Api</center></h1> <h3>Options:</h3> <ul> <li>/api/loginInfo/all - <i>Fetches all login data from database</i></li> </ul>"

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
    return homePageText

#=============================================================================#Requesting QuoteInfo from the API========================================================================
@app.route('/quoteInfo', methods=['GET'])

def quoteInfo():
    connect_db()

    quoteInfoQuery = """SELECT * FROM quoteoftheday"""

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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

app.run()
