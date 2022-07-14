from flask import jsonify, request, Blueprint
from Modules.Sessions.Config import sessionsGetSchemaLocation, sessionsReceivedJsonDataLocation
from Modules.Util import validateJsonResponse, saveJsonResponse

getSession = Blueprint('getSession', __name__)


# GET
@getSession.route('/sessions', methods=['GET'])
def getSessions():
    from appRestApi import Sessions
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
    else:
        sessions = Sessions.query.filter_by(account_id=getUserID).all()
        for session in sessions:
            currSession = {}
            currSession['id'] = session.id
            currSession['date'] = session.date
            currSession['time'] = session.time
            currSession['duration'] = session.duration
            currSession['account_id'] = session.account_id
            output.append(currSession)

            if validateJsonResponse(sessionsGetSchemaLocation, output) == False:
                # Save received json data to "received" file
                saveJsonResponse(sessionsReceivedJsonDataLocation, output)

            else:
                return "There were errors while validating the json data"

    return jsonify(output)
