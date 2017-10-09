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
        theFile = open(theDirectory + "workspace" + str(theTimeStamp) + ".json", "w", encoding='utf-8')
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

        theIntentColumn = self.readThe['Intents']
        theIntentsArray = []
        theCounter = 0
        for each in theIntentColumn:
            theIntentExamplesArray = []
            theIntentName = self.readThe['Entity'].get(theCounter)

            example1 = {
                "text": "¿" + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theCreatedDate
            }

            example2 = {
                "text": "" + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }
            example3 = {
                "text": "¿Qué es un " + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }
            example4 = {
                "text": "¿Que es un " + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }
            example5 = {
                "text": "Qué es un " + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }
            example6 = {
                "text": "Que es un " + theIntentName + "?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }

            example7 = {
                "text": theIntentName + ", ¿qué es?",
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }

            theIntentExamplesArray.append(example1)
            theIntentExamplesArray.append(example2)
            theIntentExamplesArray.append(example3)
            theIntentExamplesArray.append(example4)
            theIntentExamplesArray.append(example5)
            theIntentExamplesArray.append(example6)
            theIntentExamplesArray.append(example7)

            theClientExamples = self.readThe['Examples']
            if theClientExamples.count() > 0:
                theCustomExamples = theClientExamples.get_value(theCounter)
                each_custom_intent = str(theCustomExamples)
                print(each_custom_intent)
                if not each_custom_intent == "nan":
                    theQuestionsArray = each_custom_intent.split(";")
                    for each_example in theQuestionsArray:
                        theCustomExampleIntent = {
                            "text": each_example,
                            "created": theCreatedDate,
                            "updated": theUpdatedDate
                        }
                        print(theCustomExampleIntent)
                        theIntentExamplesArray.append(theCustomExampleIntent)
                else:
                    print("There are NO client custom examples for this intent {}.".format(theIntentName))
            else:
                print("Well, there are some that have, others don't.")
            theIntents = {
                "intent": each,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "examples": theIntentExamplesArray,
                "description": None
            }

            theIntentsArray.append(theIntents)
            theCounter += 1

        theEntityColumn = self.readThe['Entity']
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
    app.run(debug=True)  # LOCAL HOST
