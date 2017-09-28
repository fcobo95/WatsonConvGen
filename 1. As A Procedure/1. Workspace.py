from datetime import datetime
from flask import Flask, redirect, Response
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

    return Response(theResponse, mimetype='application/json')


class Workspace:
    def __init__(self):
        self.readThe = CSV.Reader().theFinalCSVData
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

        theEntityColumn = self.readThe['Entity']
        theCounter = 0
        theEntitiesArray = []

        for each in theEntityColumn:
            theValuesArray = []
            each = str(each)
            theValues = {
                "type": "synonyms",
                "value": each,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "synonyms": getSynonyms(each)
            }
            theValuesArray.append(theValues)

            theEntities = {
                "entity": each,
                "values": theValuesArray,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "description": None
            }
            theCounter += 1
            theEntitiesArray.append(theEntities)

        theLanguage = self.readThe['Language'].get_value(0)

        theFormattedYear = datetime.today().year
        theYearAsNumber = str(theFormattedYear)
        theFormattedMonth = datetime.today().month
        theMonthAsNumber = str(theFormattedMonth)
        theFormattedDay = datetime.today().day
        theDayAsNumber = str(theFormattedDay)
        theCreatedDateFormatted = "{}-{}-{}".format(theYearAsNumber, theMonthAsNumber, theDayAsNumber)

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
        theDialogNodesArray = []

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

    # CHANGE THIS LINE OF CODE AFTER SUPERVISOR APPROVAL OR FEEDBACK.
    # FALSE FOR NOT FINISHED OR TRUE FOR FINISHED.
    Supervisor_Approval = False


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3000, debug=True) #ACCESIBLE POR TODOS
    app.run(debug=True) # LOCAL HOST
