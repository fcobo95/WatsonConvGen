import json
import watson_developer_cloud
from WatsonWorkspaceAssembler import Entity, Examples, Intent
from Readers import ReaderJSON as JSONReader


class WorkspaceBuilder:
    """
    DOCSTRING
    """
    theDirectory = '../Data Files/app_settings'
    readThe = JSONReader.JSONReader(theDirectory).theFinalJSONData
    theConversation = watson_developer_cloud.ConversationV1(
        username=readThe['username'],
        password=readThe['password'],
        version=readThe['version']
    )

    theEntities = Entity.Entity()
    theIntents = Intent.Intents()
    theExamples = Examples.Examples()
