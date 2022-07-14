import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Quotes.Config import quoteUpdateJsonSchemaLocation
from Modules.Util import validateJsonResponse

updateQuotes = Blueprint('updateQuotes', __name__)


# UPDATE
@updateQuotes.route('/quoteUpdate', methods=['POST'])
def updateQuote():
    from appRestApi import db, Quotes
    if (request.is_json):
        quoteData = request.get_json()

        # Validates sent JSON before update
        if validateJsonResponse(quoteUpdateJsonSchemaLocation, quoteData) == False:
            Quotes.query.filter_by(id=quoteData['id']).update(dict(content=quoteData['content']))
            db.session.commit()
            db.session.close()

    else:
        updateQuoteXml()

    return "Successfuly updated quote!"


# UPDATE WITH XML
def updateQuoteXml():
    from appRestApi import db, Quotes
    quoteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        updatedQuoteID = item.find('id').text
        updatedQuoteContent = item.find('content').text

    Quotes.query.filter_by(id=updatedQuoteID).update(dict(content=updatedQuoteContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated quote!"
