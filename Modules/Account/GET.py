from flask import jsonify, request, Blueprint
from Modules.Account.Config import accountsGetJsonSchemaLocation, accountsReceivedJsonDataLocation, \
    accountGetJsonSchemaLocation, accountReceivedJsonDataLocation
from Modules.Util import validateJsonResponse, saveJsonResponse


getAccount = Blueprint('getAccount', __name__)


# GET
@getAccount.route('/accounts', methods=['GET'])
def getAccounts():
    from appRestApi import Account
    getAccountEmail = request.args.get("email")
    output = []

    if getAccountEmail is None:
        allAccounts = Account.query.all()
        for account in allAccounts:
            currAccount = {}
            currAccount['id'] = account.id
            currAccount['email'] = account.email
            output.append(currAccount)

        # Validate and save json response
        if validateJsonResponse(accountsGetJsonSchemaLocation, output) == False:
            # Save received json data to "received" file
            saveJsonResponse(accountsReceivedJsonDataLocation, output)

            # #Convert received json data to XML
            # convertNotesJsonToXml(notesReceivedJsonDataLocation, notesXmlFileLocation, len(output))

            # #Convert XML data to a more structured JSON to "converted" file
            # convertFromXMLToJSON(notesXmlFileLocation, notesJsonDataConvertedFromXmlLocation)
        else:
            return "There were errors while validating the json data"

    else:
        account = Account.query.filter_by(email=getAccountEmail).first()
        currAccount = {}
        currAccount['id'] = account.id
        currAccount['email'] = account.email
        output.append(currAccount)

        # Validate and save json response
        if validateJsonResponse(accountGetJsonSchemaLocation, output) == False:
            # Save received json data to "received" file
            saveJsonResponse(accountReceivedJsonDataLocation, output)

    return jsonify(output)
