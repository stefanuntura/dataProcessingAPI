import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Events.Config import eventInsertSchemaLocation, eventInsertXmlSchemaLocation, eventInsertXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse

insertEvents = Blueprint('insertEvents', __name__)

#INSERT
@insertEvents.route('/events', methods=['POST'])
def insertEvent():
    from appRestApi import db, Events
    if (request.is_json):
        eventData = request.get_json()

        # Validates sent JSON before insert
        if validateJsonResponse(eventInsertSchemaLocation, eventData) == False:
            event = Events(date=eventData['date'], time=eventData['time'], title=eventData['title'],
                           account_id=eventData['account_id'])
            db.session.add(event)
            db.session.commit()
            db.session.close()
        else:
            return "Json input validation failed!"

    else:
        insertEventXml()

    return "Successfully added event!"


# INSERT WITH XML
def insertEventXml():
    from appRestApi import db, Events
    eventData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)
    tree.write(eventInsertXmlDataLocation)

    if validateXmlResponse(eventInsertXmlSchemaLocation, eventInsertXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
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
