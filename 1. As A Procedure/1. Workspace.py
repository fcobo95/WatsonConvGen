from datetime import datetime
from flask import Flask, json, jsonify, redirect
from Readers import ReaderCSV as CSV
import requests
import time

app = Flask(__name__)


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return redirect('/response')


def getSynonyms(word):
    theDirectory = "../Data Files/"
    KEY = open(theDirectory + "key.txt")
    theKey = KEY.read()
    theSynonyms = requests.get(
        "http://words.bighugelabs.com/api/2/" + str(theKey) + "/" + word + "/json")
    KEY.close()
    theJSON = theSynonyms.json()
    theSynonymsArray = theJSON['noun']['syn']
    theFinalSynonymsArray = []
    for eachWord in theSynonymsArray:
        theWords = str(eachWord)
        if theWords.__contains__("'"):
            theWords = theWords.replace("'", "")
        theFinalSynonymsArray.append(theWords)
    print(theFinalSynonymsArray)

    return theFinalSynonymsArray


@app.route('/response')
def returnTheWorkspace():
    theWorkspace = Workspace()
    theResponse = theWorkspace.generateTheWorkspace()

    """
    ########################################################################################
    These lines of code will format theResponse into a valid JSON response./////////////////
    ########################################################################################
    """
    if "'" in theResponse:
        theResponse = theResponse.replace("'", '"')

    if "None" in theResponse:
        theResponse = theResponse.replace("None", "null")

    if "False" in theResponse:
        theResponse = theResponse.replace("False", "false")

    if "True" in theResponse:
        theResponse = theResponse.replace("True", "true")

    try:
        theDate = datetime.today().year + datetime.today().month + datetime.today().day
        theTime = str(time.time())
        theTemportalTimeStamp = "{}{}".format(theTime, theDate)
        theTimeStamp = theTemportalTimeStamp.replace(".", "")
        print(theTimeStamp)
        theDirectory = "../Data Files/"
        theFile = open(theDirectory + "workspace" + str(theTimeStamp) + ".json", "w")
        theFile.write(theResponse)
        theFile.close()
    except FileExistsError:
        print("Something went wrong.")
        returnTheWorkspace()

    return theResponse


class Workspace:
    def __init__(self):
        self.readThe = CSV.reader().theFinalCSVData
        self.theCounter = 0

    def generateTheWorkspace(self):
        """
        GENERATE THE WORKSPACE FUNCTION
        :return: theFinalWorkspace
        """
        """
        ########################################################################################
        This line of code will obtain the name of the Workspace.////////////////////////////////
        ########################################################################################
        """
        theWorkspaceName = self.readThe['WorkspaceName'].get_value(0)

        """
        ########################################################################################
        This block of code will generate a custom iso formatted date./////////////////////////// 
        ########################################################################################
        """

        theCreatedDay = datetime.today().day
        theCreatedCurrentDay = int(theCreatedDay)
        theCreatedMonth = datetime.today().month
        theCreatedCurrentMonth = int(theCreatedMonth)
        theCreatedYear = datetime.today().year
        theCreatedCurrentYear = int(theCreatedYear)
        theCreatedHour = datetime.today().hour
        theCreatedCurrentHour = int(theCreatedHour)
        theCreatedMinute = datetime.today().minute
        theCreatedCurrentMinute = int(theCreatedMinute)
        theCreatedSecond = datetime.today().second
        theCreatedCurrentSecond = int(theCreatedSecond)
        theCreatedMicrosecond = datetime.today().microsecond
        theCreatedCurrentMicrosecond = int(theCreatedMicrosecond)
        theCurrentCreatedDate = datetime(theCreatedCurrentYear, theCreatedCurrentMonth, theCreatedCurrentDay,
                                         theCreatedCurrentHour, theCreatedCurrentMinute, theCreatedCurrentSecond,
                                         theCreatedCurrentMicrosecond)
        theCreatedDate = theUpdatedDate = theCurrentCreatedDate.isoformat() + 'Z'

        theIntentExampleText = self.readThe['Examples'].get_value(0)
        theIntenExamplesArray = []
        theIntentExamples = {
            "text": theIntentExampleText,
            "created": theCreatedDate,
            "updated": theUpdatedDate
        }
        theIntenExamplesArray.append(theIntentExamples)

        theIntentName = self.readThe['Intents'].get_value(0)
        theIntentsArray = []
        theIntents = {
            "intent": theIntentName,
            "created": theCreatedDate,
            "updated": theUpdatedDate,
            "examples": theIntenExamplesArray,
            "description": None
        }
        theIntentsArray.append(theIntents)

        theEntityData = self.readThe['Entity']
        theEntityValuesArray = []
        theValuesCounter = 0
        for each in theEntityData:
            theEntityValueName = self.readThe['Entity'].get_value(theValuesCounter)
            theEntityValueSynonyms = getSynonyms(theEntityValueName)
            theEntityValues = {
                "value": theEntityValueName,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "synonyms": theEntityValueSynonyms
            }
            theEntityValuesArray.append(theEntityValues)
            theValuesCounter += 1

        theEntitiesArray = []
        theEntitiesCounter = 0
        for each in theEntityData:
            theEntityName = self.readThe['Entity'].get_value(theEntitiesCounter)
            theEntities = {
                "entity": theEntityName,
                "values": theEntityValuesArray,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "description": None
            }
            theEntitiesArray.append(theEntities)
            theEntitiesCounter += 1

        theLanguage = input("The options are:\n"
                            "en\n"
                            "es\n")

        theFormattedYear = datetime.today().year
        theYearAsNumber = int(theFormattedYear)
        theFormattedMonth = datetime.today().month
        theMonthAsNumber = int(theFormattedMonth)
        theFormattedDay = datetime.today().day
        theDayAsNumber = int(theFormattedDay)
        theCreatedDateFormatted = str("{}-{}-{}").format(theYearAsNumber, theMonthAsNumber, theDayAsNumber)

        theMetaDataMajorVersion = 'v1'
        theMetaDataMinorVersion = theCreatedDateFormatted
        theWorkspaceMetaDataAPI_VERSION = {
            "major_version": theMetaDataMajorVersion,
            "minor_version": theMetaDataMinorVersion
        }
        theWorkspaceMetaData = {
            "api_version": theWorkspaceMetaDataAPI_VERSION
        }

        theWorkspaceDescription = self.readThe['Description'].get_value(0)

        # TODO: DECOMPOSE INTO SMALLER PARTS.
        # TODO: INVESTIGATE: http://mydevbits.blogspot.com/2016/08/automating-creation-of-chatbot-dialog.html
        theDialogNodesArray = [
            # """
            #     {
            #         "title": "prueba",
            #         "output": {
            #             "text": {
            #                 "values": [
            #                     "Prueba 1"
            #                 ],
            #                 "selection_policy": "sequential"
            #             }
            #         },
            #         "parent": None,
            #         "context": None,
            #         "created": "2017-09-11T16:55:42.021Z",
            #         "updated": "2017-09-11T16:56:20.851Z",
            #         "metadata": None,
            #         "next_step": None,
            #         "conditions": "#Prueba1 && @Prueba1",
            #         "description": None,
            #         "dialog_node": "node_1_1505145345622",
            #         "previous_sibling": "Welcome"
            #     },
            #     {
            #         "title": None,
            #         "output": {
            #             "text": {
            #                 "values": [
            #                     "I didn't understand. You can try rephrasing.",
            #                     "Can you reword your statement? I'm not understanding.",
            #                     "I didn't get your meaning."
            #                 ],
            #                 "selection_policy": "sequential"
            #             }
            #         },
            #         "parent": None,
            #         "context": None,
            #         "created": "2017-09-11T16:55:38.611Z",
            #         "updated": "2017-09-11T16:55:38.611Z",
            #         "metadata": None,
            #         "next_step": None,
            #         "conditions": "anything_else",
            #         "description": None,
            #         "dialog_node": "Anything else",
            #         "previous_sibling": "node_1_1505145345622"
            #     },
            #     {
            #         "title": None,
            #         "output": {
            #             "text": {
            #                 "values": [
            #                     "Hello. How can I help you?"
            #                 ],
            #                 "selection_policy": "sequential"
            #             }
            #         },
            #         "parent": None,
            #         "context": None,
            #         "created": "2017-09-11T16:55:38.611Z",
            #         "updated": "2017-09-11T16:55:38.611Z",
            #         "metadata": None,
            #         "next_step": None,
            #         "conditions": "welcome",
            #         "description": None,
            #         "dialog_node": "Welcome",
            #         "previous_sibling": None
            #     }
            # """
        ]

        # SALT = open('../Data Files/SALT.txt', 'r')

        theWorkspaceID = '1234'

        theWorkspaceCounterExamples = []  # TODO: CHECK PURPOSE

        theWorkspaceLearningOptOut = False  # TODO: CHECK PURPOSE

        # THE WORKSPACE GENERATED BY THE BACKEND. RETURN THIS WORKSPACE AS A .JSON FILE.
        theFinalWorkspace = {
            "name": theWorkspaceName,
            "created": theCreatedDate,
            "intents": theIntentsArray,
            "updated": theUpdatedDate,
            "entities": theEntitiesArray,
            "language": theLanguage,
            "metadata": theWorkspaceMetaData,
            "description": theWorkspaceDescription,
            "dialog_nodes": theDialogNodesArray,
            "workspace_id": theWorkspaceID,
            "counterexamples": theWorkspaceCounterExamples,
            "learning_opt_out": theWorkspaceLearningOptOut
        }

        return str(dict(theFinalWorkspace))


if __name__ == '__main__':
    app.run(debug=True)
