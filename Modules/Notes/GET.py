from flask import Flask, render_template, jsonify, request
from Modules.Notes.Config import notesGetJsonSchemaLocation, notesReceivedJsonDataLocation, notesXmlFileLocation, \
    notesJsonDataConvertedFromXmlLocation
from Modules.Util import validateJsonResponse, saveJsonResponse, convertNotesJsonToXml, convertFromXMLToJSON
from appRestApi import app, db, Notes


# GET
@app.route('/notes', methods=['GET'])
def getNotes():
    getUserID = request.args.get("id")
    output = []

    if getUserID is None:
        return "no user id specified"
    else:
        notes = Notes.query.filter_by(account_id=getUserID).all()
        for note in notes:
            currNote = {}
            currNote['id'] = note.id
            currNote['subject'] = note.subject
            currNote['title'] = note.title
            currNote['content'] = note.content
            currNote['account_id'] = note.account_id
            output.append(currNote)

        # Validate and save json response
        if validateJsonResponse(notesGetJsonSchemaLocation, output) == False:
            # Save received json data to "received" file
            saveJsonResponse(notesReceivedJsonDataLocation, output)

            # Convert received json data to XML
            convertNotesJsonToXml(notesReceivedJsonDataLocation, notesXmlFileLocation, len(output))

            # Convert XML data to a more structured JSON to "converted" file
            convertFromXMLToJSON(notesXmlFileLocation, notesJsonDataConvertedFromXmlLocation)
        else:
            return "There were errors while validating the json data"

    return jsonify(output)
