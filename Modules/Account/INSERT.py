import xml.etree.ElementTree as ET
from flask import Blueprint, request, jsonify
from Modules.Account.Config import accountInsertSchemaLocation, accountsInsertXmlSchemaLocation, accountInsertXmlDataLocation
from Modules.Util import validateJsonResponse, validateXmlResponse


insertAccounts = Blueprint('insertAccounts', __name__)


# INSERT
# Checks if account already exists
# If entry already exists, returns string "Account already exists!"
# If entry does not exist, inserts sent entry in database

@insertAccounts.route('/accounts', methods=['POST'])
def insertAccount():
    from appRestApi import Account, db
    if (request.is_json):
        accountData = request.get_json()

        # Validates sent JSON
        if validateJsonResponse(accountInsertSchemaLocation, accountData) == False:
            exists = bool(db.session.query(Account).filter_by(email=accountData['email']).first())

            if (exists):
                return "Account already exists!"
            else:
                insertAccountJson(accountData)
                return "Successfully inserted account using json!"
        else:
            return "Json input validation failed!"
    else:
        accountData = request.get_data()

        # Transforms data received into a non-flat xml file
        info = ET.fromstring(accountData)
        tree = ET.ElementTree(info)
        tree.write(accountInsertXmlDataLocation)

        if validateXmlResponse(accountsInsertXmlSchemaLocation, accountInsertXmlDataLocation) == True:
            print("Successfuly validated xml!")

            # Iterates over xml and finds necessarry data belonging to tags
            for item in tree.iter('account'):
                accountEmail = item.find('email').text

                exists = bool(db.session.query(Account).filter_by(email=accountEmail).first())

                if (exists):
                    return "Account already exists!"
                else:
                    insertAccountXml(accountData)
                    return "Successfuly inserted account using xml!"

    return jsonify(accountData)


def insertAccountJson(accountData):
    from appRestApi import Account, db
    # Validates sent JSON before insert
    if validateJsonResponse(accountInsertSchemaLocation, accountData) == False:
        account = Account(email=accountData['email'])
        db.session.add(account)
        db.session.commit()
        db.session.close()

    else:
        return "Json input validation failed!"


def insertAccountXml(accountData):
    from appRestApi import Account, db
    # Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)
    tree.write(accountInsertXmlDataLocation)

    if validateXmlResponse(accountsInsertXmlSchemaLocation, accountInsertXmlDataLocation) == True:
        print("Successfuly validated xml!")

        # Iterates over xml and finds necessarry data belonging to tags
        for item in tree.iter('account'):
            newAccountEmail = item.find('email').text

        account = Account(email=newAccountEmail)
        db.session.add(account)
        db.session.commit()
        db.session.close()