import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Quotes.Config import quoteInsertSchemaLocation
from Modules.Util import validateJsonResponse

insertQuotes = Blueprint('insertQuotes', __name__)


# INSERT
@insertQuotes.route('/quotes', methods=['POST'])
def insertQuote():
    from appRestApi import db, Quotes
    if (request.is_json):
        quoteData = request.get_json()

        # Validates sent JSON before insert
        if validateJsonResponse(quoteInsertSchemaLocation, quoteData) == False:
            quote = Quotes(content=quoteData['content'], account_id=quoteData['account_id'])
            db.session.add(quote)
            db.session.commit()
            db.session.close()

        else:
            return "Json input validation failed!"

    else:
        insertQuoteXml()

    return "Successfuly inserted quote!"


def insertQuoteXml():
    from appRestApi import db, Quotes
    quoteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(quoteData)
    tree = ET.ElementTree(info)

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('quote'):
        newQuoteContent = item.find('content').text
        newQuoteAccountID = item.find('accountID').text

    quote = Quotes(content=newQuoteContent, account_id=newQuoteAccountID)
    db.session.add(quote)
    db.session.commit()
    db.session.close()

    return "Successfully inserted quote!"
