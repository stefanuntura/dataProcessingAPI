import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Sessions.Config import sessionDeleteJsonSchemaLocation, sessionDeleteXmlSchemaLocation, sessionDeleteXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse

deleteSessions = Blueprint('deleteSessions', __name__)


# DELETE
@deleteSessions.route('/sessionDelete', methods=['POST'])
def deleteSession():
    from appRestApi import db, Sessions
    if (request.is_json):
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


# DELETE BY XML POST
def deleteSessionXml():
    from appRestApi import db, Sessions
    sessionToDeleteID = ''
    sessionData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(sessionData)
    tree = ET.ElementTree(info)
    tree.write(sessionDeleteXmlDataLocation)

    if validateXmlResponse(sessionDeleteXmlSchemaLocation, sessionDeleteXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
        for item in tree.iter('session'):
            sessionToDeleteID = item.find('id').text

        # Deletes note based on id specified in xml sent
        sessionToDelete = Sessions.query.get(sessionToDeleteID)
        db.session.delete(sessionToDelete)
        db.session.commit()
        db.session.close()

    return "Successfuly deleted session!"
