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
    theDirectory = getTheDirectory()
    KEY = openTheKey(theDirectory)
    theKey = readTheKey(KEY)
    theSynonyms = getTheRequest(theKey, word)
    closeTheKey(KEY)
    theJSON = formatTheSynonymsToJSON(theSynonyms)
    theSynonymsArray = readTheSynonymsJSONArray(theJSON)
    theFinalSynonymsArray = formatTheSynonyms(theSynonymsArray)

    return returnTheSynonyms(theFinalSynonymsArray)


def closeTheKey(KEY):
    return KEY.close()


def readTheKey(KEY):
    return KEY.read()


def getTheDirectory():
    return "../Data Files/"


def openTheKey(theDirectory):
    return open(theDirectory + "key.txt")


def getTheRequest(theKey, word):
    return requests.get(
        "http://words.bighugelabs.com/api/2/" + str(theKey) + "/" + word + "/json")


def formatTheSynonymsToJSON(theSynonyms):
    return theSynonyms.json()


def readTheSynonymsJSONArray(theJSON):
    return theJSON['noun']['syn']


def formatTheSynonyms(theSynonymsArray):
    theFinalSynonymsArray = []
    for eachWord in theSynonymsArray:
        theWords = convertToString(eachWord)
        if theWords.__contains__("'"):
            theWords = replaceQuotes(theWords)
        theFinalSynonymsArray.append(theWords)
    return theFinalSynonymsArray


def convertToString(eachWord):
    return str(eachWord)


def replaceQuotes(theWords):
    return theWords.replace("'", "")


def returnTheSynonyms(theFinalSynonymsArray):
    return theFinalSynonymsArray


@app.route('/response')
def returnTheWorkspace():
    theWorkspace = workspace()
    theResponse = theWorkspace.generateTheEntities()

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
        theTime = str(time.time())
        theDate = datetime.today().year + datetime.today().month + datetime.today().day
        theTemportalTimeStamp = "{}{}".format(theTime, theDate)
        theTimeStamp = theTemportalTimeStamp.replace(".", "")
        theDirectory = "../Data Files/"
        theFile = open(theDirectory + "workspace" + str(theTimeStamp) + ".json", "w")
        theFile.write(theResponse)
        theFile.close()
    except FileExistsError:
        print("Something went wrong.")
        returnTheWorkspace()

    return Response(theResponse, mimetype='application/json')


class workspace:
    def __init__(self):
        self.readThe = CSV.Reader().theFinalCSVData

    def generateTheEntities(self):
        theData = self.readThe['Entity']
        theEntitiesArray = []

        for each in theData:
            theValuesArray = []
            each = str(each)
            theValues = {
                "type": "synonyms",
                "value": each,
                "created": "2017-09-25T15:32:02.119Z",
                "updated": "2017-09-25T15:32:46.730Z",
                "metadata": None,
                "synonyms": getSynonyms(each)
            }
            theValuesArray.append(theValues)

            theEntities = {
                "entity": each,
                "values": theValuesArray,
                "created": "2017-09-25T15:33:20.156Z",
                "updated": "2017-09-25T15:33:42.078Z",
                "metadata": None,
                "description": None
            }
            theEntitiesArray.append(theEntities)

        theWorkspace = {
            "entities": theEntitiesArray
        }

        return str(dict(theWorkspace))

    def generateTheIntents(self):
        theIntentColumn = self.readThe['Intents']
        theIntentsArray = []
        theIntentExamples = []

        theIntentValues = {
            "intent": "gato_que_es",
            "created": "2017-09-30T03:34:12.676Z",
            "updated": "2017-09-30T03:34:32.192Z",
            "examples": [
                {
                    "text": "¿Gato?",
                    "created": "2017-09-30T03:34:19.140Z",
                    "updated": "2017-09-30T03:34:19.140Z"
                },
                {
                    "text": "¿Qué es un gato?",
                    "created": "2017-09-30T03:34:25.680Z",
                    "updated": "2017-09-30T03:34:25.680Z"
                },
                {
                    "text": "Gato, ¿qué es?",
                    "created": "2017-09-30T03:34:32.192Z",
                    "updated": "2017-09-30T03:34:32.192Z"
                }
            ],
            "description": None
        }

        theIntents = {
            "intents": theIntentsArray
        }


if __name__ == '__main__':
    app.run(debug=True)
