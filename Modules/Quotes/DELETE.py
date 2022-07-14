import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Quotes.Config import quoteDeleteJsonSchemaLocation
from Modules.Util import validateJsonResponse

deleteQuotes = Blueprint('deleteQuotes', __name__)


# DELETE
@deleteQuotes.route('/quoteDelete', methods=['POST'])
def deleteQuote():
    from appRestApi import db, Quotes
    if (request.is_json):
        quoteData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(quoteDeleteJsonSchemaLocation, quoteData) == False:
            quoteToDelete = Quotes.query.get(quoteData['id'])
            db.session.delete(quoteToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteQuoteXml()

    return "Successfuly deleted quote!"


# DELETE BY XML POST
def deleteQuoteXml():
    from appRestApi import db, Quotes
    updatedQuoteID = ''
    quoteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        updatedQuoteID = item.find('id').text

    # Deletes note based on id specified in xml sent
    quoteToDelete = Quotes.query.get(updatedQuoteID)
    db.session.delete(quoteToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted quote!"
