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
    return KEY.close()


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
    """
    Class Workspace. This object will be the brain, to control and coordinate all other objects and their functionalities
    in order to create the workspace.
    """

    def __init__(self):
        self.readThe = CSV.reader().theFinalCSVData
        self.theCounter = 0

    def generateTheWorkspace(self):
        """
        This is a coordinator method that will eventually return theFinalWorkspace
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
        theCreatedDate, theUpdatedDate = self.returnTheISODate(theCurrentCreatedDate)

        """
        ########################################################################################
        This block of code will all the Intent Examples found in the CSV file provided by the/// 
        customer./////////////////////////////////////////////////////////////////////////////// 
        ########################################################################################
        """
        theIntentExamplesData = self.readThe['Examples']
        theIntenExamplesArray = self.getTheIntentExamples(theCreatedDate, theIntentExamplesData, theUpdatedDate)

        """
        ########################################################################################
        This block of code will all the Intents found in the CSV and apply the procedures found/
        in the corresponding functions.///////////////////////////////////////////////////////// 
        ########################################################################################
        """
        theIntentNameData = self.readThe['Intents']
        theIntentsArray = self.getTheIntentNames(theCreatedDate, theIntenExamplesArray, theIntentNameData,
                                                 theUpdatedDate)

        """
        ########################################################################################
        This piece of code will get all the entities found in the CSV file and then create the// 
        JSON pieces that will be needed to create the final workspace. This will generate an////
        array with all the values for each entity found.////////////////////////////////////////  
        ########################################################################################
        """
        theEntityData = self.readThe['Entity']
        theEntityValuesArray = self.getTheEntityValues(theCreatedDate, theEntityData, theUpdatedDate)
        theEntitiesArray = self.getTheEntities(theCreatedDate, theEntityData, theEntityValuesArray,
                                               theUpdatedDate)  # TODO: CHECK SECOND PARAMETER. IT MAY NEED A CHANGE.

        """
        ########################################################################################
        This method will ask the user for an input regarding the workspace native language./////
        ////////////////////////////////////////////////////////////////////////////////////////
        The options are:
        - en
        - es
        ////////////////////////////////////////////////////////////////////////////////////////
        This will return the user input and set it as the workspace language in the JSON output/
        file./////////////////////////////////////////////////////////////////////////////////// 
        ########################################################################################
        """
        theLanguage = self.getTheLanguage()

        """
        ########################################################################################
        This block of code will generate a custom date format for the METADATA Minor Version./// 
        ########################################################################################
        """
        theYearAsString = self.getTheFormattedYear()
        theMonthAsString = self.getTheFormattedMonth()
        theDayAsString = self.getTheFormattedDay()
        theCreatedDateFormatted = self.getTheFormattedDate(theDayAsString, theMonthAsString, theYearAsString)
        theMetaDataMinorVersion = self.returnTheMetaDataMinorVersion(theCreatedDateFormatted)

        """
        ########################################################################################
        This will return the current version of the API, which is 'v1'./////////////////////////
        ########################################################################################
        """
        theMetaDataMajorVersion = self.getTheMetaDataMajorVersion()

        """
        ########################################################################################
        This just gets all the little parts and assembles them into the METADATA JSON key:value. 
        ########################################################################################
        """
        theWorkspaceMetaDataAPI_VERSION = self.getTheMetaDataAPI_Version(theMetaDataMajorVersion,
                                                                         theMetaDataMinorVersion)
        theWorkspaceMetaData = self.getTheWorkspaceMetaData(theWorkspaceMetaDataAPI_VERSION)

        """
        ########################################################################################
        This gets the description for the workspace being generated from the CSV file.////////// 
        ########################################################################################
        """
        theWorkspaceDescription = self.getTheWorkspaceDescription()

        """
        ########################################################################################
        TODO: INVESTIGATE: 
        http://mydevbits.blogspot.com/2016/08/automating-creation-of-chatbot-dialog.html 
        ########################################################################################
        """
        theDialogNodesArray = []

        """
        ########################################################################################
        This generates a custom made workspace id, just for the sake of doing it, because Watson
        actually assigns a new one when you upload the entire workspace JSON file.////////////// 
        ########################################################################################
        """
        theWorkspaceID = self.getTheWorkspaceID()

        """
        ########################################################################################
        Some settings. Will be explained and investigated later on.///////////////////////////// 
        ########################################################################################
        """
        theWorkspaceCounterExamples = []
        theWorkspaceLearningOptOut = False
        """
        ########################################################################################
        THE WORKSPACE GENERATED BY THE BACKEND. RETURN THIS WORKSPACE AS A .JSON FILE. 
        ########################################################################################
        """
        theFinalWorkspace = self.getTheFinalWorkspace(theCreatedDate, theDialogNodesArray, theEntitiesArray,
                                                      theIntentsArray, theLanguage, theUpdatedDate,
                                                      theWorkspaceCounterExamples, theWorkspaceDescription,
                                                      theWorkspaceID, theWorkspaceLearningOptOut, theWorkspaceMetaData,
                                                      theWorkspaceName)

        return self.returnTheFinalWorkspace(theFinalWorkspace)

    def getTheIntentExamples(self, theCreatedDate, theIntentExamplesData, theUpdatedDate):
        theIntenExamplesArray = []
        theExamplesCounter = 0
        for _ in theIntentExamplesData:
            theIntentExampleText = self.readThe['Examples'].get_value(theExamplesCounter)
            theIntentExamples = {
                "text": theIntentExampleText,
                "created": theCreatedDate,
                "updated": theUpdatedDate
            }
            theIntenExamplesArray.append(theIntentExamples)
            theExamplesCounter += 1
        return theIntenExamplesArray

    def getTheIntentNames(self, theCreatedDate, theIntenExamplesArray, theIntentNameData, theUpdatedDate):
        theIntentsArray = []
        theNamesCounter = 0
        for _ in theIntentNameData:
            theIntentName = self.readThe['Intents'].get_value(theNamesCounter)
            theIntents = {
                "intent": theIntentName,
                "created": theCreatedDate,
                "updated": theUpdatedDate,
                "examples": theIntenExamplesArray,
                "description": None
            }
            theIntentsArray.append(theIntents)
            theNamesCounter += 1
        return theIntentsArray

    def getTheEntityValues(self, theCreatedDate, theEntityData, theUpdatedDate):
        theEntityValuesArray = []
        theValuesCounter = 0
        for _ in theEntityData:
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
        return theEntityValuesArray

    def getTheEntities(self, theCreatedDate, theEntityData, theEntityValuesArray, theUpdatedDate):
        theEntitiesArray = []
        theEntitiesCounter = 0
        for _ in theEntityData:
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
        return theEntitiesArray

    def getTheDay(self):
        return self.obtainTheDay()

    def obtainTheDay(self):
        return int(datetime.today().day)

    def getTheMonth(self):
        return self.obtainTheMonth()

    def obtainTheMonth(self):
        return int(datetime.today().month)

    def getTheYear(self):
        return self.obtainTheYear()

    def obtainTheYear(self):
        return int(datetime.today().year)

    def getTheHour(self):
        return self.obtainTheHour()

    def obtainTheHour(self):
        return int(datetime.today().hour)

    def getTheMinutes(self):
        return self.obtainTheMinutes()

    def obtainTheMinutes(self):
        return int(datetime.today().minute)

    def getTheSeconds(self):
        return self.obtainTheSeconds()

    def obtainTheSeconds(self):
        return int(datetime.today().second)

    def getTheMicroseconds(self):
        return self.obtainTheMicroseconds()

    def obtainTheMicroseconds(self):
        return int(datetime.today().microsecond)

    def returnTheISODate(self, theCurrentCreatedDate):
        return theCurrentCreatedDate.isoformat() + 'Z'

    def getTheLanguage(self):
        return input("The options are:\n"
                     "en\n"
                     "es\n")

    def getTheFormattedYear(self):
        return self.obtainTheFormattedYear()

    def obtainTheFormattedYear(self):
        return str(datetime.today().year)

    def getTheFormattedMonth(self):
        return self.obtainTheFormattedMonth()

    def obtainTheFormattedMonth(self):
        return str(datetime.today().month)

    def getTheFormattedDay(self):
        return self.obtainTheFormattedDay()

    def obtainTheFormattedDay(self):
        return str(datetime.today().day)

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
