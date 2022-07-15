import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Events.Config import eventDeleteJsonSchemaLocation, eventDeleteXmlSchemaLocation, eventDeleteXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse

deleteEvents = Blueprint('deleteEvents', __name__)


# DELETE
@deleteEvents.route('/eventDelete', methods=['POST'])
def deleteEvent():
    from appRestApi import db, Events
    if (request.is_json):
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


# DELETE BY XML POST
def deleteEventXml():
    from appRestApi import db, Events
    eventToDeleteID = ''
    eventData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)
    tree.write(eventDeleteXmlDataLocation)

    if validateXmlResponse(eventDeleteXmlSchemaLocation, eventDeleteXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
        for item in tree.iter('event'):
            eventToDeleteID = item.find('id').text

        # Deletes note based on id specified in xml sent
        eventToDelete = Events.query.get(eventToDeleteID)
        db.session.delete(eventToDelete)
        db.session.commit()
        db.session.close()

    return "Successfuly deleted note!"
