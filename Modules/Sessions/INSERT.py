import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Sessions.Config import sessionInsertSchemaLocation
from Modules.Util import validateJsonResponse

insertSessions = Blueprint('insertSessions', __name__)


# INSERT
@insertSessions.route('/sessions', methods=['POST'])
def insertSession():
    from appRestApi import db, Sessions
    if (request.is_json):
        sessionData = request.get_json()

        # Validates sent JSON before insert
        if validateJsonResponse(sessionInsertSchemaLocation, sessionData) == False:
            session = Sessions(date=sessionData['date'], time=sessionData['time'], duration=sessionData['duration'],
                               account_id=sessionData['account_id'])
            db.session.add(session)
            db.session.commit()
            db.session.close()
        else:
            return "Json input validation failed!"

    else:
        insertSessionXml()

    return "Successfully added session!"


# INSERT WITH XML
def insertSessionXml():
    from appRestApi import db, Sessions
    sessionData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('session'):
        newSessionDate = item.find('date').text
        newSessionTime = item.find('time').text
        newSessionDuration = item.find('duration').text
        newSessionAccountID = item.find('accountID').text

    session = Sessions(date=newSessionDate, time=newSessionTime, duration=newSessionDuration,
                       account_id=newSessionAccountID)
    db.session.add(session)
    db.session.commit()
    db.session.close()

    return "Successfully added session!"
