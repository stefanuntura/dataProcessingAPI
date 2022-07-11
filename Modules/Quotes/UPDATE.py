import xml.etree.ElementTree as ET
from flask import Flask, render_template, jsonify, request
from Modules.Quotes.Config import quoteUpdateJsonSchemaLocation
from Modules.Util import validateJsonResponse
from appRestApi import app, db, Quotes


# UPDATE
@app.route('/quoteUpdate', methods=['POST'])
def updateQuote():
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
