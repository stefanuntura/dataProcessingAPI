import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Events.Config import eventUpdateSchemaLocation, eventUpdateXmlSchemaLocation, eventUpdateXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse


updateEvents = Blueprint('updateEvents', __name__)


# UPDATE
@updateEvents.route('/eventUpdate', methods=['POST'])
def updateEvent():
    from appRestApi import db, Events
    if (request.is_json):
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


# UPDATE WITH XML
def updateEventXml():
    from appRestApi import db, Events
    eventData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)
    tree.write(eventUpdateXmlDataLocation)

    if validateXmlResponse(eventUpdateXmlSchemaLocation, eventUpdateXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
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
