import xml.etree.ElementTree as ET
from flask import request, Blueprint
from Modules.Account.Config import accountUpdateSchemaLocation
from Modules.Util import validateJsonResponse

updateAccounts = Blueprint('updateAccounts', __name__)


# UPDATE
@updateAccounts.route('/accountUpdate', methods=['POST'])
def updateAccount():
    from appRestApi import Account, db
    if (request.is_json):
        accountData = request.get_json()

        # Validates sent JSON before update
        if validateJsonResponse(accountUpdateSchemaLocation, accountData) == False:
            Account.query.filter_by(id=accountData['id']).update(dict(email=accountData['email']))
            db.session.commit()
            db.session.close()

    else:
        updateAccountXml()

    return "Successfuly updated account!"


# UPDATE WITH XML
def updateAccountXml():
    from appRestApi import Account, db
    accountData = request.get_data()

    # Transforms data received into a non-flat xml file
    info = ET.fromstring(accountData)
    tree = ET.ElementTree(info)

    # Iterates over xml and finds necessarry data belonging to tags
    for item in tree.iter('account'):
        updatedAccountID = item.find('id').text
        updatedAccountContent = item.find('email').text

    Account.query.filter_by(id=updatedAccountID).update(dict(email=updatedAccountContent))
    db.session.commit()
    db.session.close()

    return "Successfuly updated account!"
