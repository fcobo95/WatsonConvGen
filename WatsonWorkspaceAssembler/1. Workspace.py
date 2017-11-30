from flask import Flask, redirect, Response
import datetime
import time
from WatsonWorkspaceAssembler import WorkspaceAssembler

app = Flask(__name__)
__APPNAME__ = "Watson Chatbot Automator"


# DEFAULT ROUTE
@app.route('/')
def hello_world():
    return redirect('/response')


@app.route('/response')
def returnTheWorkspace():
    theWorkspace = WorkspaceAssembler()
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


if __name__ == '__main__':
    print("Welcome to {}".format(__APPNAME__))
    app.run(host='0.0.0.0', port=3000, debug=None)
