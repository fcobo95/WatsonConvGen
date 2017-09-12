"""
BACKUP CODE
"""

"""
########################################################################################################################
THIS IS AS A PROCEDURE
########################################################################################################################
"""
from datetime import datetime
import requests
from flask import Flask, redirect, jsonify
from Readers import ReaderCSV as CSV
import time

app = Flask(__name__)


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return redirect('/response')


@app.route('/get-synonyms')
def givemesynonyms(word):
    theDirectory = "../Data Files/"
    KEY = open(theDirectory + "key.txt", "r")
    theKey = KEY.read()
    theSynonyms = requests.get(
        "http://words.bighugelabs.com/api/2/" + str(theKey) + "/" + word + "/json")
    KEY.close()
    theJSON = theSynonyms.json()
    theSynonymsArray = theJSON['noun']['syn']
    theFinalSynonymsArray = []
    for each in theSynonymsArray:
        theWords = str(each)
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
        theResponse = theResponse.replace("None", "None")

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
        theCurrentCreatedDate = datetime(
            theCreatedCurrentYear,
            theCreatedCurrentMonth,
            theCreatedCurrentDay,
            theCreatedCurrentHour,
            theCreatedCurrentMinute,
            theCreatedCurrentSecond,
            theCreatedCurrentMicrosecond
        )

        """
        ########################################################################################
        The variables 'theCreatedDate' and 'theUpdatedDate' will be assigned the same value,they 
        will call the same method.//////////////////////////////////////////////////////////////
        ########################################################################################
        """
        theCreatedDate = theUpdatedDate = theCurrentCreatedDate.isoformat() + 'Z'

        theIntentName = "Something to read from"
        theIntents = [
            {
                "intent": theIntentName,
                "created": "2017-09-11T16:36:43.590Z",
                "updated": "2017-09-11T16:37:01.199Z",
                "examples": [
                    {
                        "text": "Prueba1.2",
                        "created": "2017-09-11T16:36:51.571Z",
                        "updated": "2017-09-11T16:36:51.571Z"
                    },
                    {
                        "text": "Prueba1.1",
                        "created": "2017-09-11T16:36:57.211Z",
                        "updated": "2017-09-11T16:36:57.211Z"
                    },
                    {
                        "text": "prueba1.3",
                        "created": "2017-09-11T16:37:01.199Z",
                        "updated": "2017-09-11T16:37:01.199Z"
                    }
                ],
                "description": None
            },
            {
                "intent": "Prueba2",
                "created": "2017-09-11T16:37:11.922Z",
                "updated": "2017-09-11T16:37:22.092Z",
                "examples": [
                    {
                        "text": "Prueba2.1",
                        "created": "2017-09-11T16:37:16.954Z",
                        "updated": "2017-09-11T16:37:16.954Z"
                    },
                    {
                        "text": "Prueba2.2",
                        "created": "2017-09-11T16:37:19.447Z",
                        "updated": "2017-09-11T16:37:19.447Z"
                    },
                    {
                        "text": "Prueba2.3",
                        "created": "2017-09-11T16:37:22.092Z",
                        "updated": "2017-09-11T16:37:22.092Z"
                    }
                ],
                "description": None
            }
        ]
        theEntityValues = []
        theEntities = []
        theEntityName = self.readThe['Entity'].get_value(self.theCounter)
        if self.theCounter is None:
            pass
        else:
            theEntityName = self.readThe['Entity'].get_value(self.theCounter)
            eachEntity = None
            for each in theEntityName:
                theEntityName = self.readThe['Entity'].get_value(self.theCounter)
                theEntityValueSynonyms = givemesynonyms(theEntityName)
                eachEntitySynonym = {
                    "value": theEntityName,
                    "created": theCreatedDate,
                    "updated": theUpdatedDate,
                    "metadata": None,
                    "synonyms": theEntityValueSynonyms
                }
                theEntityValues.append(eachEntitySynonym)
                print(theEntityValues)

                self.theCounter = self.theCounter + 1
        eachEntity = {
            "entity": theEntityName,
            "values": theEntityValues,
            "created": theCreatedDate,
            "updated": theUpdatedDate,
            "metadata": None,
            "description": None
        }
        theEntities.append(eachEntity)

        theLanguage = 'en'

        """
        ########################################################################################
        This block of code will generate a specifically formatted date for the metadata key.////
        Format = YYYY-M-D | ==> Example: 2017-8-9.//////////////////////////////////////////////
        ########################################################################################
        """

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
        theDialogNodes = []
        theWorkspaceID = '1234'
        theWorkspaceCounterExamples = []
        theWorkspaceLearningOptOut = False

        # THE WORKSPACE GENERATED BY THE BACKEND. RETURN THIS WORKSPACE AS A .JSON FILE.
        theFinalWorkspace = {
            "name": theWorkspaceName,
            "created": theCreatedDate,
            "intents": theIntents,
            "updated": theUpdatedDate,
            "entities": theEntities,
            "language": theLanguage,
            "metadata": theWorkspaceMetaData,
            "description": theWorkspaceDescription,
            "dialog_nodes": theDialogNodes,
            "workspace_id": theWorkspaceID,
            "counterexamples": theWorkspaceCounterExamples,
            "learning_opt_out": theWorkspaceLearningOptOut
        }

        return str(dict(theFinalWorkspace))


if __name__ == '__main__':
    app.run(debug=True)

"""
########################################################################################################################
THIS IS AS A PROCEDURE
########################################################################################################################
"""

"""
########################################################################################################################
THIS IS WITH FUNCTIONS
########################################################################################################################
"""
from datetime import datetime
from flask import Flask
from Readers import ReaderCSV as CSV
import requests
import time

app = Flask(__name__)


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return 'Hello World!'


def getSynonyms(word):
    theDirectory = "../Data Files/"
    KEY = open(theDirectory + "key.txt", "r")
    theKey = KEY.read()
    theSynonyms = requests.get(
        "http://words.bighugelabs.com/api/2/" + str(theKey) + "/" + word + "/json")
    KEY.close()
    theJSON = theSynonyms.json()
    theSynonymsArray = theJSON['noun']['syn']
    theFinalSynonymsArray = []
    for each in theSynonymsArray:
        theWords = str(each)
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
        theResponse = theResponse.replace("None", "None")

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


class WorkspaceWithFunctions:
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
        theCurrentCreatedDate = datetime(
            theCreatedCurrentYear,
            theCreatedCurrentMonth,
            theCreatedCurrentDay,
            theCreatedCurrentHour,
            theCreatedCurrentMinute,
            theCreatedCurrentSecond,
            theCreatedCurrentMicrosecond
        )
        theCreatedDate = theUpdatedDate = theCurrentCreatedDate.isoformat() + 'Z'

        theIntentExampleText = ''
        theIntenExamplesArray = []
        theIntentExamples = {
            "text": theIntentExampleText,
            "created": theCreatedDate,
            "updated": theUpdatedDate
        }
        theIntentName = ''
        theIntentsArray = []
        theIntents = {
            "intent": theIntentName,
            "created": theCreatedDate,
            "updated": theUpdatedDate,
            "examples": theIntenExamplesArray,
            "description": None
        }

        theEntityValueName = ''
        theEntityValueSynonyms = getSynonyms("fuckme")  # just words. Like a regular array. ['a','b','c','d','e']
        theEntityValuesArray = []
        theEntityValues = {
            "value": theEntityValueName,
            "created": theCreatedDate,
            "updated": theUpdatedDate,
            "metadata": None,
            "synonyms": theEntityValueSynonyms
        }
        theEntityValuesArray.append(theEntityValues)

        theEntityName = ''
        theEntitiesArray = []
        theEntities = {
            "entity": theEntityName,
            "values": theEntityValuesArray,
            "created": theCreatedDate,
            "updated": theUpdatedDate,
            "metadata": None,
            "description": None
        }
        theEntityValuesArray.append(theEntities)

        theLanguage = ''  # TODO: LANGUAGE

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

        theWorkspaceDescription = ''

        theDialogNodesArray = [
            {
                "title": "prueba",
                "output": {
                    "text": {
                        "values": [
                            "Prueba 1"
                        ],
                        "selection_policy": "sequential"
                    }
                },
                "parent": None,
                "context": None,
                "created": "2017-09-11T16:55:42.021Z",
                "updated": "2017-09-11T16:56:20.851Z",
                "metadata": None,
                "next_step": None,
                "conditions": "#Prueba1 && @Prueba1",
                "description": None,
                "dialog_node": "node_1_1505145345622",
                "previous_sibling": "Welcome"
            },
            {
                "title": None,
                "output": {
                    "text": {
                        "values": [
                            "I didn't understand. You can try rephrasing.",
                            "Can you reword your statement? I'm not understanding.",
                            "I didn't get your meaning."
                        ],
                        "selection_policy": "sequential"
                    }
                },
                "parent": None,
                "context": None,
                "created": "2017-09-11T16:55:38.611Z",
                "updated": "2017-09-11T16:55:38.611Z",
                "metadata": None,
                "next_step": None,
                "conditions": "anything_else",
                "description": None,
                "dialog_node": "Anything else",
                "previous_sibling": "node_1_1505145345622"
            },
            {
                "title": None,
                "output": {
                    "text": {
                        "values": [
                            "Hello. How can I help you?"
                        ],
                        "selection_policy": "sequential"
                    }
                },
                "parent": None,
                "context": None,
                "created": "2017-09-11T16:55:38.611Z",
                "updated": "2017-09-11T16:55:38.611Z",
                "metadata": None,
                "next_step": None,
                "conditions": "welcome",
                "description": None,
                "dialog_node": "Welcome",
                "previous_sibling": None
            }
        ]

        theWorkspaceID = ''

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

        return theFinalWorkspace


if __name__ == '__main__':
    app.run()

"""
########################################################################################################################
THIS IS WITH FUNCTIONS
########################################################################################################################
"""
