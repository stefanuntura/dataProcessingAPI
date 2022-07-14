from flask import jsonify, request, Blueprint
from Modules.Events.Config import eventsGetSchemaLocation, eventsReceivedJsonDataLocation
from Modules.Util import validateJsonResponse, saveJsonResponse

getEvent = Blueprint('getEvent', __name__)


# GET
@getEvent.route('/events', methods=['GET'])
def getEvents():
    from appRestApi import Events
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
    else:
        events = Events.query.filter_by(account_id=getUserID).all()
        for event in events:
            currEvent = {}
            currEvent['id'] = event.id
            currEvent['time'] = event.time
            currEvent['date'] = event.date
            currEvent['title'] = event.title
            currEvent['account_id'] = event.account_id
            output.append(currEvent)

        if validateJsonResponse(eventsGetSchemaLocation, output) == False:
            # Save received json data to "received" file
            saveJsonResponse(eventsReceivedJsonDataLocation, output)

        else:
            return "There were errors while validating the json data"

    return jsonify(output)
