# !/usr/bin/env python
import json


class JSONReader:
    """
    DOCSTRING
    """

    def __init__(self, theDirectory=None):
        with open(theDirectory) as JSONData:
            self.theFinalJSONData = json.load(JSONData)
