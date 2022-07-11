import xml.etree.ElementTree as ET
from flask import request
from Modules.Notes.Config import notesDeleteJsonSchemaLocation
from Modules.Util import validateJsonResponse
from appRestApi import app, db, Notes


# DELETE
@app.route('/noteDelete', methods=['POST'])
def deleteNotes():
    if (request.is_json):
        noteData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(notesDeleteJsonSchemaLocation, noteData) == False:
            noteToDelete = Notes.query.get(noteData['id'])
            db.session.delete(noteToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteNotesXml()

    return "Successfuly deleted note!"


# DELETE BY XML POST
def deleteNotesXml():
    noteToDeleteID = ''
    noteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        noteToDeleteID = item.find('id').text

    # Deletes note based on id specified in xml sent
    noteToDelete = Notes.query.get(noteToDeleteID)
    db.session.delete(noteToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted note!"
