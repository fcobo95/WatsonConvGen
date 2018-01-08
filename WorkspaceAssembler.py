from flask import Flask, redirect, Response
from Readers import ReaderWorkspaceCSV as CSV
from Readers import ReaderDialogCSV as Dialog
import requests
import time
import calendar

app = Flask(__name__)
__APPNAME__ = "Watson Chatbot Automator"


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    """
    DOCSTRING
    """
    return redirect('/response')


def atSynonyms(word):
    """
    DOCSTRING
    """
    theDirectory = "key.txt"
    KEY = open(theDirectory)
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


@app.route('/response')
def returnTheWorkspace():
    """
    DOCSTRING
    """
    theWorkspace = Workspace()
    theResponse = theWorkspace.generateTheWorkspace()

    """
    ########################################################################################
    These lines of code will format theResponse into a valid JSON response./////////////////
    ########################################################################################
    """
    if "'" in theResponse:
        theResponse = theResponse.replace("'", '"')
    if "nan" in theResponse:
        theResponse = theResponse.replace("nan", "null")

    if "None" in theResponse:
        theResponse = theResponse.replace("None", "null")

    if "False" in theResponse:
        theResponse = theResponse.replace("False", "false")

    if "True" in theResponse:
        theResponse = theResponse.replace("True", "true")

    try:
        theFile = open("workspace.json", "w", encoding='utf-8')
        theFile.write(theResponse)
        theFile.close()
    except FileExistsError:
        print("Something went wrong.")
        returnTheWorkspace()

    return Response(theResponse, mimetype='application/json')


class Workspace:
    """
    DOCSTRING
    """

    def __init__(self):
        self.readTheCSV = CSV.CSVReader().theFinalCSVData
        self.readTheDialog = Dialog.DialogReader().theFinalCSVData
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
        theWorkspaceName = self.readTheCSV['WorkspaceName'].iat[0]

        theIntentColumn = self.readTheCSV['Intents']
        theIntentsArray = []
        theCounter = 0

        for each in theIntentColumn:
            queFlag = self.readTheCSV['queFlag'].at[theCounter]
            comoFlag = self.readTheCSV['queFlag'].at[theCounter]
            cuandoFlag = self.readTheCSV['queFlag'].at[theCounter]

            theIntentExamplesArray = []

            theIntentName = self.readTheCSV['Entity'].at[theCounter]

            if queFlag:
                example3 = {
                    "text": "¿Qué es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example4 = {
                    "text": "¿Que es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example5 = {
                    "text": "Qué es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example6 = {
                    "text": "Que es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example7 = {
                    "text": theIntentName + ", ¿qué es?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                theIntentExamplesArray.append(example3)
                theIntentExamplesArray.append(example4)
                theIntentExamplesArray.append(example5)
                theIntentExamplesArray.append(example6)
                theIntentExamplesArray.append(example7)

            if comoFlag:
                example3 = {
                    "text": "¿Cómo es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example4 = {
                    "text": "¿Como es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example5 = {
                    "text": "Cómo es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example6 = {
                    "text": "Como es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example7 = {
                    "text": theIntentName + ", ¿cómo es?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                theIntentExamplesArray.append(example3)
                theIntentExamplesArray.append(example4)
                theIntentExamplesArray.append(example5)
                theIntentExamplesArray.append(example6)
                theIntentExamplesArray.append(example7)

            if cuandoFlag:
                example3 = {
                    "text": "¿Cuándo es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example4 = {
                    "text": "¿Cuando es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example5 = {
                    "text": "Cuándo es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example6 = {
                    "text": "Cuando es un " + theIntentName + "?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                example7 = {
                    "text": theIntentName + ", ¿cuándo es?",
                    "created": "2018-01-08T15:09:43.760Z",
                    "updated": "2018-01-08T15:09:43.760Z"
                }

                theIntentExamplesArray.append(example3)
                theIntentExamplesArray.append(example4)
                theIntentExamplesArray.append(example5)
                theIntentExamplesArray.append(example6)
                theIntentExamplesArray.append(example7)

            theClientExamples = self.readTheCSV['Examples']
            if theClientExamples.count() > 0:
                theCustomExamples = theClientExamples.iat[theCounter]
                each_custom_intent = str(theCustomExamples)
                if not each_custom_intent == "nan":
                    theQuestionsArray = each_custom_intent.split(";")
                    for each_example in theQuestionsArray:
                        theCustomExampleIntent = {
                            "text": each_example,
                            "created": "2018-01-08T15:09:43.760Z",
                            "updated": "2018-01-08T15:09:43.760Z"
                        }
                        theIntentExamplesArray.append(theCustomExampleIntent)
                else:
                    print("There are NO client custom examples for this intent {}.".format(theIntentName))
            else:
                print("Well, there are some that have, others don't.")

            theIntents = {
                "intent": each,
                "examples": theIntentExamplesArray,
                "description": None,
                "created": "2018-01-08T15:09:43.760Z",
                "updated": "2018-01-08T15:09:43.760Z"
            }

            theIntentsArray.append(theIntents)
            theCounter += 1

        theEntityColumn = self.readTheCSV['Entity']
        theEntitiesArray = []
        for each in theEntityColumn:
            theValuesArray = []
            each = str(each)
            theValues = {
                "type": "synonyms",
                "value": each,
                "metadata": None,
                "synonyms": atSynonyms(each),
                "created": "2018-01-08T15:09:43.760Z",
                "updated": "2018-01-08T15:09:43.760Z"
            }
            theValuesArray.append(theValues)

            theEntities = {
                "entity": each,
                "values": theValuesArray,
                "metadata": None,
                "description": None,
                "created": "2018-01-08T15:09:43.760Z",
                "updated": "2018-01-08T15:09:43.760Z"
            }
            theEntitiesArray.append(theEntities)

        theLanguage = self.readTheCSV['Language'].iat[0]

        theMetaDataMajorVersion = "v1"
        theMetaDataMinorVersion = "2017-05-26"
        theWorkspaceMetaDataAPI_VERSION = {
            "major_version": theMetaDataMajorVersion,
            "minor_version": theMetaDataMinorVersion
        }
        theWorkspaceMetaData = {
            "api_version": theWorkspaceMetaDataAPI_VERSION
        }

        theWorkspaceDescription = self.readTheCSV['Description'].iat[0]

        theDialogNodesArray = []
        theWelcomeNode = {
            "type": "standard",
            "title": "Welcome",
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
            "created": "2018-01-08T15:09:43.760Z",
            "updated": "2018-01-08T15:09:43.760Z",
            "metadata": {},
            "next_step": None,
            "conditions": "welcome",
            "description": None,
            "dialog_node": "Welcome",
            "previous_sibling": None
        }
        theDialogNodesArray.append(theWelcomeNode)
        theNodesCounter = 0
        for _ in self.readTheDialog['Row']:
            theResponses = self.readTheDialog['Response']
            theNodeType = 'standard'
            theNodeTitle = self.readTheDialog['Title'].at[theNodesCounter]
            theNodeValuesArray = []
            if theResponses.count() > 0:
                theNodeResponse = theResponses.iat[theNodesCounter]
                each_value = str(theNodeResponse)
                theNodeResponseArray = each_value.split('*')
                for each in theNodeResponseArray:
                    theNodeValuesArray.append(each)
            theNodeOutput = {
                "text": {
                    "values": theNodeValuesArray
                }
            }
            theNodeParent = self.readTheDialog['Parent'].at[theNodesCounter]
            if theNodeParent is None or theNodeParent is 'nan':
                theNodeParent = None
            theNodeContext = self.readTheDialog['Context'].at[theNodesCounter]
            theNodeMetaData = {}
            theNodeNextStep = self.readTheDialog['Next Step'].at[theNodesCounter]
            theNodeConditions = self.readTheDialog['Conditions'].at[theNodesCounter]
            theNodeDescription = self.readTheDialog['Description'].at[theNodesCounter]
            theNodeDialogNode = self.readTheDialog['Dialog Node #'].at[theNodesCounter]
            theNodePreviousSibling = self.readTheDialog['Previous Sibling'].at[theNodesCounter]
            theNode = {
                "type": theNodeType,
                "title": theNodeTitle,
                "output": theNodeOutput,
                "parent": theNodeParent,
                "context": theNodeContext,
                "created": "2017-12-26T23:12:52.230Z",
                "updated": "2017-12-26T23:13:29.850Z",
                "metadata": theNodeMetaData,
                "next_step": theNodeNextStep,
                "conditions": theNodeConditions,
                "description": theNodeDescription,
                "dialog_node": str(theNodeDialogNode),
                "previous_sibling": theNodePreviousSibling
            }
            theDialogNodesArray.append(theNode)
            theNodesCounter += 1

        theLastNodeNumber = theDialogNodesArray[-1]
        theLastDialogNodeNumber = theLastNodeNumber['dialog_node']
        theAnythingElseNode = {
            "type": "standard",
            "title": "Anything else",
            "output": {
                "text": {
                    "values": [
                        "I did not understand. You can try rephrasing.",
                        "Can you reword your statement? I am not understanding.",
                        "I did not get your meaning."
                    ],
                    "selection_policy": "sequential"
                }
            },
            "parent": None,
            "context": None,
            "created": "2018-01-08T15:09:43.760Z",
            "updated": "2018-01-08T15:09:43.760Z",
            "metadata": {},
            "next_step": None,
            "conditions": "anything_else",
            "description": None,
            "dialog_node": "Anything else",
            "previous_sibling": str(theLastDialogNodeNumber)
        }
        theDialogNodesArray.append(theAnythingElseNode)

        theWorkspaceID = '1234'

        theWorkspaceCounterExamples = []

        theWorkspaceLearningOptOut = False

        # THE WORKSPACE GENERATED BY THE BACKEND. RETURN THIS WORKSPACE AS A .JSON FILE.
        theFinalWorkspace = {
            "name": theWorkspaceName,
            "intents": theIntentsArray,
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
    print("Welcome to {}".format(__APPNAME__))
    app.run(host='0.0.0.0', port=3000)  # ACCESIBLE POR TODOS Y NO DEBUG
    # app.run(debug=True)  # LOCAL HOST Y DEBUG
