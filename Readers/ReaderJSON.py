import json


class reader:
    def __init__(self):
        with open('../Data Files/data.json') as JSONData:
            self.theFinalJSONData = json.load(JSONData)
