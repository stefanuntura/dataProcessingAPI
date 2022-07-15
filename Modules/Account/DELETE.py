from flask import request, Blueprint
from Modules.Account.Config import accountDeleteSchemaLocation, accountsDeleteXmlSchemaLocation, accountDeleteXmlDataLocation
from Modules.Util import *

deleteAccounts = Blueprint('deleteAccounts', __name__)


# DELETE
@deleteAccounts.route('/accountDelete', methods=['POST'])
def deleteAccount():
    from appRestApi import Account, db
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
    from appRestApi import Account, db
    accountID = ''
    accountData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)
    tree.write(accountDeleteXmlDataLocation)

    if validateXmlResponse(accountsDeleteXmlSchemaLocation, accountDeleteXmlDataLocation) == True:
        print("Successfuly validated xml!")

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
