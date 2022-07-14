import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Notes.Config import notesInsertJsonSchemaLocation
from Modules.Util import validateJsonResponse

insertNotes = Blueprint('insertNotes', __name__)


# INSERT
@insertNotes.route('/notes', methods=['POST'])
def insertNote():
    from appRestApi import db, Notes
    if (request.is_json):
        noteData = request.get_json()

        # Validates sent JSON before insert
        if validateJsonResponse(notesInsertJsonSchemaLocation, noteData) == False:
            note = Notes(subject=noteData['subject'], title=noteData['title'], content=noteData['content'],
                         account_id=noteData['account_id'])
            db.session.add(note)
            db.session.commit()
            db.session.close()
        else:
            return "Json input validation failed!"

    else:
        insertNoteXml()

    return "Successfully added note!"


# INSERT WITH XML
def insertNoteXml():
    from appRestApi import db, Notes
    noteData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(noteData)
    tree = ET.ElementTree(info)
    tree.write('xml/noteInsertXml.xml')

    # if validateXmlResponse('xmlSchemas/noteInsertSchema.txt', info) == True:
    #     print("Successfuly validated xml!")

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('note'):
        newNoteSubject = item.find('subject').text
        newNoteTitle = item.find('title').text
        newNoteContent = item.find('content').text
        newNoteAccountID = item.find('accountID').text

    note = Notes(subject=newNoteSubject, title=newNoteTitle, content=newNoteContent, account_id=newNoteAccountID)
    db.session.add(note)
    db.session.commit()
    db.session.close()

    return "Successfully added note!"
