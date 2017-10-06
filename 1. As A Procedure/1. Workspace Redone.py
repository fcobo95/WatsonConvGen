from datetime import datetime
from flask import Flask, redirect, Response
from Readers import ReaderCSV as CSV
import time

app = Flask(__name__)


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return redirect('/response')


@app.route('/response')
def returnTheWorkspace():
    theWorkspace = workspace()
    theResponse = theWorkspace.generateTheIntents()

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

    def generateTheIntents(self):


        return str(dict(theWorkspace))


if __name__ == '__main__':
    app.run(debug=True)
