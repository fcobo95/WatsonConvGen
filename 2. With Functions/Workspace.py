from datetime import datetime
from flask import Flask, json, jsonify, redirect, render_template
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
    KEY.close()


def readTheKey(KEY):
    return KEY.read()


def getTheDirectory():
    return "../Data Files/"


def openTheKey(theDirectory):
    return open(theDirectory + "key.txt", "r")


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

        theCreatedCurrentDay = self.getTheDay()
        theCreatedCurrentMonth = self.getTheMonth()
        theCreatedCurrentYear = self.getTheYear()
        theCreatedCurrentHour = self.getTheHour()
        theCreatedCurrentMinute = self.getTheMinutes()
        theCreatedCurrentSecond = self.getTheSeconds()
        theCreatedCurrentMicrosecond = self.getTheMicroseconds()
        theCurrentCreatedDate = datetime(theCreatedCurrentYear, theCreatedCurrentMonth, theCreatedCurrentDay,
                                         theCreatedCurrentHour, theCreatedCurrentMinute, theCreatedCurrentSecond,
                                         theCreatedCurrentMicrosecond)
        theCreatedDate = theUpdatedDate = self.returnTheISODate(theCurrentCreatedDate)

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

        theLanguage = self.getTheLanguage()
        theYearAsNumber = self.getTheFormattedYear()
        theMonthAsNumber = self.getTheFormattedMonth()
        theDayAsNumber = self.getTheFormattedDay()
        theCreatedDateFormatted = self.getTheFormattedDate(theDayAsNumber, theMonthAsNumber, theYearAsNumber)
        theMetaDataMajorVersion = self.getTheMetaDataMajorVersion()
        theMetaDataMinorVersion = self.returnTheMetaDataMinorVersion(theCreatedDateFormatted)
        theWorkspaceMetaDataAPI_VERSION = self.getTheMetaDataAPI_Version(theMetaDataMajorVersion,
                                                                         theMetaDataMinorVersion)
        theWorkspaceMetaData = self.getTheWorkspaceMetaData(theWorkspaceMetaDataAPI_VERSION)
        theWorkspaceDescription = self.getTheWorkspaceDescription()
        # TODO: INVESTIGATE: http://mydevbits.blogspot.com/2016/08/automating-creation-of-chatbot-dialog.html
        theDialogNodesArray = []
        theWorkspaceID = self.getTheWorkspaceID()
        theWorkspaceCounterExamples = []
        theWorkspaceLearningOptOut = False
        # THE WORKSPACE GENERATED BY THE BACKEND. RETURN THIS WORKSPACE AS A .JSON FILE.
        theFinalWorkspace = self.getTheFinalWorkspace(theCreatedDate, theDialogNodesArray, theEntitiesArray,
                                                      theIntentsArray, theLanguage, theUpdatedDate,
                                                      theWorkspaceCounterExamples, theWorkspaceDescription,
                                                      theWorkspaceID, theWorkspaceLearningOptOut, theWorkspaceMetaData,
                                                      theWorkspaceName)

        return self.returnTheFinalWorkspace(theFinalWorkspace)

    def getTheDay(self):
        theCreatedDay = datetime.today().day
        return int(theCreatedDay)

    def getTheMonth(self):
        theCreatedMonth = datetime.today().month
        return int(theCreatedMonth)

    def getTheYear(self):
        theCreatedYear = datetime.today().year
        return int(theCreatedYear)

    def getTheHour(self):
        theCreatedHour = datetime.today().hour
        return int(theCreatedHour)

    def getTheMinutes(self):
        theCreatedMinute = datetime.today().minute
        return int(theCreatedMinute)

    def getTheSeconds(self):
        theCreatedSecond = datetime.today().second
        return int(theCreatedSecond)

    def getTheMicroseconds(self):
        theCreatedMicrosecond = datetime.today().microsecond
        return int(theCreatedMicrosecond)

    def returnTheISODate(self, theCurrentCreatedDate):
        return theCurrentCreatedDate.isoformat() + 'Z'

    def getTheLanguage(self):
        return input("The options are:\n"
                     "en\n"
                     "es\n")

    def getTheFormattedYear(self):
        theFormattedYear = datetime.today().year
        return str(theFormattedYear)

    def getTheFormattedMonth(self):
        theFormattedMonth = datetime.today().month
        return str(theFormattedMonth)

    def getTheFormattedDay(self):
        theFormattedDay = datetime.today().day
        return str(theFormattedDay)

    def getTheFormattedDate(self, theDayAsString, theMonthAsString, theYearAsString):
        return "{}-{}-{}".format(theYearAsString, theMonthAsString, theDayAsString)

    def getTheMetaDataMajorVersion(self):
        return 'v1'

    def returnTheMetaDataMinorVersion(self, theCreatedDateFormatted):
        return theCreatedDateFormatted

    def getTheMetaDataAPI_Version(self, theMetaDataMajorVersion, theMetaDataMinorVersion):
        return {
            "major_version": theMetaDataMajorVersion,
            "minor_version": theMetaDataMinorVersion
        }

    def getTheWorkspaceMetaData(self, theWorkspaceMetaDataAPI_VERSION):
        return {
            "api_version": theWorkspaceMetaDataAPI_VERSION
        }

    def getTheWorkspaceDescription(self):
        return self.readThe['Description'].get_value(0)

    def getTheWorkspaceID(self):
        return '1234'

    def getTheFinalWorkspace(self, theCreatedDate, theDialogNodesArray, theEntitiesArray, theIntentsArray, theLanguage,
                             theUpdatedDate, theWorkspaceCounterExamples, theWorkspaceDescription, theWorkspaceID,
                             theWorkspaceLearningOptOut, theWorkspaceMetaData, theWorkspaceName):
        return {
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

    def returnTheFinalWorkspace(self, theFinalWorkspace):
        return str(dict(theFinalWorkspace))


if __name__ == '__main__':
    app.run(debug=True)
