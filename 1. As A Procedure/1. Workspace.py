from flask import Flask, redirect, Response
from Readers import ReaderWorkspaceCSV as CSV
from Readers import ReaderDialogCSV as Dialog
import requests
import datetime
import time

app = Flask(__name__)
__APPNAME__ = "Watson Chatbot Automator"


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return redirect('/response')


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
        theDate = "{}{}{}".format(str(datetime.date.today().year), str(datetime.date.today().month),
                                  str(datetime.date.today().day))
        theTime = str(time.time())
        theTemportalTimeStamp = "{}{}".format(theTime, theDate)
        theTimeStamp = theTemportalTimeStamp.replace(".", "")
        theDirectory = "../Data Files/"
        theFile = open(theDirectory + "workspace" + str(theTimeStamp) + ".json", "w", encoding='utf-8')
        theFile.write(theResponse)
        theFile.close()
    except FileExistsError:
        print("Something went wrong.")
        returnTheWorkspace()

    return Response(theResponse, mimetype='application/json')


class Workspace:
    """
    Workspace class.
    """

    def __init__(self):
        self.readTheCSV = CSV.CSVReader().theFinalCSVData
        self.readTheDialog = Dialog.DialogReader().theFinalCSVData
        self.theCounter = 0

    def getSynonyms(self, word):
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

        return theFinalSynonymsArray

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
        theWorkspaceName = self.readTheCSV['WorkspaceName'].get_value(0)

        """
        ########################################################################################
        This block of code will generate a custom iso formatted date./////////////////////////// 
        ########################################################################################
        """

        theCreatedDay = datetime.date.today().day
        theCreatedMonth = datetime.date.today().month
        theCreatedYear = datetime.date.today().year
        theCreatedHour = datetime.datetime.today().hour
        theCreatedMinute = datetime.datetime.today().minute
        theCreatedSecond = datetime.datetime.today().second
        theCreatedMicrosecond = datetime.datetime.today().microsecond
        theCurrentCreatedDate = datetime.datetime(theCreatedYear, theCreatedMonth, theCreatedDay,
                                                  theCreatedHour, theCreatedMinute, theCreatedSecond,
                                                  theCreatedMicrosecond)
        theCreatedDate = theUpdatedDate = theCurrentCreatedDate.isoformat() + 'Z'

        # TODO: AGREGAR QUE, COMO Y CUANDO
        theIntentColumn = self.readTheCSV['Intents']
        theIntentsArray = []
        theCounter = 0

        for each in theIntentColumn:
            queFlag = self.readTheCSV['queFlag'].get(theCounter)
            comoFlag = self.readTheCSV['queFlag'].get(theCounter)
            cuandoFlag = self.readTheCSV['queFlag'].get(theCounter)

            theIntentExamplesArray = []

            theIntentName = self.readTheCSV['Entity'].get(theCounter)

            if queFlag == True:
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

            if comoFlag == True:
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
                    "text": "¿Cómo es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example4 = {
                    "text": "¿Como es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example5 = {
                    "text": "Cómo es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example6 = {
                    "text": "Como es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example7 = {
                    "text": theIntentName + ", ¿cómo es?",
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

            if cuandoFlag == True:
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
                    "text": "¿Cuándo es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example4 = {
                    "text": "¿Cuando es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example5 = {
                    "text": "Cuándo es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example6 = {
                    "text": "Cuando es un " + theIntentName + "?",
                    "created": theCreatedDate,
                    "updated": theUpdatedDate
                }

                example7 = {
                    "text": theIntentName + ", ¿cuándo es?",
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

            theClientExamples = self.readTheCSV['Examples']
            if theClientExamples.count() > 0:
                theCustomExamples = theClientExamples.get_value(theCounter)
                each_custom_intent = str(theCustomExamples)
                if not each_custom_intent == "nan":
                    theQuestionsArray = each_custom_intent.split(";")
                    for each_example in theQuestionsArray:
                        theCustomExampleIntent = {
                            "text": each_example,
                            "created": theCreatedDate,
                            "updated": theUpdatedDate
                        }
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

        theEntityColumn = self.readTheCSV['Entity']
        theEntitiesArray = []
        # TODO: CUSTOM ENTITIES
        for each in theEntityColumn:
            theValuesArray = []
            each = str(each)
            theValues = {
                "type": "synonyms",
                "value": each,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "synonyms": self.getSynonyms(each)
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

        theLanguage = self.readTheCSV['Language'].get_value(0)

        theFormattedYear = datetime.date.today().year
        theYearAsNumber = str(theFormattedYear)
        theFormattedMonth = datetime.date.today().month
        theMonthAsNumber = str(theFormattedMonth)
        theFormattedDay = datetime.date.today().day
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

        theWorkspaceDescription = self.readTheCSV['Description'].get_value(0)

        # TODO: DECOMPOSE INTO SMALLER PARTS.
        # TODO: INVESTIGATE: http://mydevbits.blogspot.com/2016/08/automating-creation-of-chatbot-dialog.html
        theDialogNodesArray = [
            {
                "title": self.readTheDialog['Title'].get_value(0),
                "output": {
                    "text": {
                        "values": [
                            self.readTheDialog['Response'].get_value(0)
                        ],
                        "selection_policy": self.readTheDialog['Selection policy'].get_value(0)
                    }
                },
                "parent": self.readTheDialog['Parent'].get_value(0),
                "context": self.readTheDialog['Context'].get_value(0),
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "metadata": None,
                "next_step": self.readTheDialog['Next Step'].get_value(0),
                "conditions": self.readTheDialog['Conditions'].get_value(0),
                "description": self.readTheDialog['Description'].get_value(0),
                "dialog_node": self.readTheDialog['Dialog Node #'].get_value(0),
                "previous_sibling": self.readTheDialog['Previous Sibling'].get_value(0)
            }
        ]

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
    Supervisor_Approval = True

    # TODO: TERMINAR DE COSTRUIR EL CSV
    # TODO: PASO FINAL ==> CREAR INTERFAZ


if __name__ == '__main__':
    print("Welcome to {}".format(__APPNAME__))
    app.run(host='0.0.0.0', port=3000)  # ACCESIBLE POR TODOS Y NO DEBUG
    # app.run(debug=True)  # LOCAL HOST Y DEBUG
