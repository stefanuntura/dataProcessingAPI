import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Sessions.Config import sessionUpdateSchemaLocation
from Modules.Util import validateJsonResponse

updateSessions = Blueprint('updateSessions', __name__)


#UPDATE WITH XML
@updateSessions.route('/sessionUpdate', methods=['POST'])
def updateSession():
    from appRestApi import db, Sessions
    if (request.is_json):
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


# UPDATE WITH XML
def updateSessionXml():
    from appRestApi import db, Sessions
    sessionData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
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

