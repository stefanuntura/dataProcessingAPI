from flask import jsonify, request, Blueprint
from Modules.Quotes.Config import quoteGetSchemaLocation, quoteReceivedJsonDataLocation
from Modules.Util import validateJsonResponse, saveJsonResponse

getQuote = Blueprint('getQuote', __name__)

# GET
@getQuote.route('/quotes', methods=['GET'])
def getQuotes():
    from appRestApi import Quotes
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
    else:
        quotes = Quotes.query.filter_by(account_id=getUserID).all()
        for quote in quotes:
            currQuote = {}
            currQuote['id'] = quote.id
            currQuote['content'] = quote.content
            currQuote['account_id'] = quote.account_id
            output.append(currQuote)

        if validateJsonResponse(quoteGetSchemaLocation, output) == False:
            # Save received json data to "received" file
            saveJsonResponse(quoteReceivedJsonDataLocation, output)

        else:
            return "There were errors while validating the json data"

    return jsonify(output)
