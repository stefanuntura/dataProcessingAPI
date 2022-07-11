# Validate JSON response
# Returns False if error list was empty, meaning validation was successful
# Returns True if error lsit is not empty, meaning there were errors while validating the data
from io import StringIO
import json
from jsonschema import Draft7Validator
import xmltodict
import xml.etree.ElementTree as ET
from lxml import etree


def validateJsonResponse(schemaLocation, dataReceived):
    # Validate schema
    with open(schemaLocation) as schemaFile:
        schema = json.load(schemaFile)
    schemaFile.close()

    validator = Draft7Validator(schema)

    listOfValidationErrors = list(validator.iter_errors(dataReceived))

    if (bool(listOfValidationErrors)):
        print("There were errors while validating the data!")
    else:
        print("Validated successfuly!")

    print("Errors while validating json:", listOfValidationErrors)

    return bool(listOfValidationErrors)


# Validate XML reponse using XSD
def validateXmlResponse(schemaLocation, xmlToValidate):
    # Get schema as string
    schemaFile = open(schemaLocation, 'r')
    fileContent = schemaFile.read()
    schemaFile.close()

    # Create schema from string
    xmlschema_doc = etree.fromstring(fileContent)
    xmlschema = etree.XMLSchema(file=schemaLocation)

    xmlschema.validate(xmlschema_doc)

    print("Errors while validating xml:", xmlschema.error_log)

    return xmlschema.validate(xmlschema_doc)


# Save JSON response to file

def saveJsonResponse(outputLocation, dataReceived):
    # Create and write response to json file
    with open(outputLocation, 'w') as outfile:
        json.dump(dataReceived, outfile)
    outfile.close()


# Convert Notes from JSON to XML

def convertNotesJsonToXml(jsonFile, xmlFile, volume):
    # Loading json file data to variable data
    with open(jsonFile, "r") as json_file:
        data = json.load(json_file)
    json_file.close()

    # Building the root element of the xml file
    root = ET.Element("Notes")

    for i in range(0, volume):
        note = ET.SubElement(root, "Note")
        # Building the subroot elements of the xml file
        ET.SubElement(note, "NoteID").text = str(data[i]["id"])

        accountInfo = ET.SubElement(note, "AccountInfo")
        # Building subelements of account info
        ET.SubElement(accountInfo, "AccountID").text = str(data[i]["account_id"])

        # Building the subroot elements of the xml file
        ET.SubElement(note, "Content").text = str(data[i]["content"])
        ET.SubElement(note, "Subject").text = str(data[i]["subject"])
        ET.SubElement(note, "Title").text = str(data[i]["title"])

    # Building the tree of XML elements using the root element
    tree = ET.ElementTree(root)

    # Writing the XML to output file
    tree.write(xmlFile)


# Convert from XML to JSON

def convertFromXMLToJSON(xmlFile, jsonFile):
    with open(xmlFile) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    xml_file.close()

    json_data = json.dumps(data_dict)

    with open(jsonFile, "w") as json_file:
        json_file.write(json_data)
    json_file.close()