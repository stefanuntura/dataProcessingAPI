import xml.etree.ElementTree as ET
from flask import Flask, render_template, jsonify, request
from Modules.Account.Config import accountDeleteSchemaLocation
from Modules.Util import validateJsonResponse
from appRestApi import Account, db
from Modules.Util import *


# DELETE
def deleteAccount():
    if (request.is_json):
        accountData = request.get_json()

        # Validates sent JSON and performs deletion
        if validateJsonResponse(accountDeleteSchemaLocation, accountData) == False:
            accountToDelete = Account.query.get(accountData['id'])
            db.session.delete(accountToDelete)
            db.session.commit()
            db.session.close()
        else:
            return "There were errors while validating the json data!"

    else:
        deleteAccountXml()

    return "Successfuly deleted account!"


# DELETE BY XML POST
def deleteAccountXml():
    accountID = ''
    accountData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('account'):
        print(item)
        accountID = item.find('id').text

    # Deletes note based on id specified in xml sent
    accountToDelete = Account.query.get(accountID)
    db.session.delete(accountToDelete)
    db.session.commit()
    db.session.close()

    return "Successfuly deleted account!"
