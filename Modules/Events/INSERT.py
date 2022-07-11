import xml.etree.ElementTree as ET
from flask import request
from Modules.Events.Config import eventInsertSchemaLocation
from Modules.Util import validateJsonResponse
from appRestApi import app, db, Events

#INSERT
@app.route('/events', methods=['POST'])
def insertEvent():
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
    eventData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(eventData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

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
