import json


class JSONReader:
    def __init__(self, theDirectory):
        with open(theDirectory) as JSONData:
            self.theFinalJSONData = json.load(JSONData)
