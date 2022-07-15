import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Notes.Config import notesDeleteJsonSchemaLocation, notesDeleteXmlSchemaLocation, notesDeleteXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse

deleteNote = Blueprint('deleteNote', __name__)

# DELETE
@deleteNote.route('/noteDelete', methods=['POST'])
def deleteNotes():
    from appRestApi import db, Notes
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
    from appRestApi import db, Notes
    noteToDeleteID = ''
    noteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)
    tree.write(notesDeleteXmlDataLocation)

    if validateXmlResponse(notesDeleteXmlSchemaLocation, notesDeleteXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
        for item in tree.iter('note'):
            noteToDeleteID = item.find('id').text

        # Deletes note based on id specified in xml sent
        noteToDelete = Notes.query.get(noteToDeleteID)
        db.session.delete(noteToDelete)
        db.session.commit()
        db.session.close()

    return "Successfuly deleted note!"
