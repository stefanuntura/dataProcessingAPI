import xml.etree.ElementTree as ET
from flask import request
from Modules.Notes.Config import notesUpdateJsonSchemaLocation, notesUpdateReceivedXmlInfoLocation
from Modules.Util import validateJsonResponse
from appRestApi import app, db, Notes

# UPDATE
@app.route('/noteUpdate', methods=['POST'])
def updateNotes():
    if (request.is_json):
        noteData = request.get_json()

        # Validates sent JSON before update
        if validateJsonResponse(notesUpdateJsonSchemaLocation, noteData) == False:
            Notes.query.filter_by(id=noteData['id']).update(dict(content=noteData['content']))
            db.session.commit()
            db.session.close()

    else:
        updateNotesXml()

    return "Successfuly updated note!"


# UPDATE WITH XML
def updateNotesXml():
    noteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)
    tree.write(notesUpdateReceivedXmlInfoLocation)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        updatedNoteID = item.find('id').text
        updatedNoteContent = item.find('content').text

    Notes.query.filter_by(id=updatedNoteID).update(dict(content=updatedNoteContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated note!"
