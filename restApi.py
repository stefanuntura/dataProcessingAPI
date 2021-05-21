import flask
import MySQLdb
import re
from MySQLdb import _mysql
from MySQLdb.constants import FIELD_TYPE
from flask import request, jsonify, json

app = flask.Flask(__name__);
app.config["DEBUG"] = True

homePageText = "<h1><center>FokusApp Rest Api</center></h1> <h3>Options:</h3> <ul> <li>/api/loginInfo/all - <i>Fetches all login data from database</i></li> </ul>"

loginInfoQuery = """SELECT * FROM accountinfo"""

def preparingResultedQueryString(queryResult):

    global modifiedQueryResult

    queryResultWithNoStart = queryResult[2:]
    queryResultWithNoEnd = queryResultWithNoStart[:-3]
    shortenedQueryResult = re.sub('b', '', queryResultWithNoEnd)
    print("Successfully substringed the fetched result")

    modifiedQueryResult = re.split(',', shortenedQueryResult)

    return modifiedQueryResult

#Home page of the API

@app.route('/', methods=['GET'])
def home():
    return homePageText

#Requesting LoginInfo from the API

@app.route('/api/loginInfo/all', methods=['GET'])
def loginInfo_all():
    db = _mysql.connect(host ='localhost', db = 'fokusapp', user = 'root', passwd = '')
    print("Successfully Connected To Database")

    db.query(loginInfoQuery)
    print("Successfully executed login info query")

    loginCredentials = db.store_result()
    print("Successfully stored login data")

    tempResult = str(loginCredentials.fetch_row())
    print("Successfully fetched login data")

    preparingResultedQueryString(tempResult)

    userID = modifiedQueryResult[0]
    userName = modifiedQueryResult[1]
    userPassword = modifiedQueryResult[2]

    loginData = {
        "AccountID": userID,
        "AccountName": userName,
        "AccountPassword": userPassword
    }

    loginInfoJsonObject = jsonify(loginData)
    print("Successfully jsonifed the substringed result")

    print("Closing database connection")
    db.close()

    return loginInfoJsonObject

app.run()
