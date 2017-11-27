#!/usr/bin/python
# coding=utf-8

import json
import watson_developer_cloud


class Watson:
    """
    DOCSTRING
    """

    def __init__(self, username=None, password=None, version=None):
        self.conversation = watson_developer_cloud.ConversationV1(
            username=username,  # '46b3dba5-3f3e-4b04-b8f2-38e65eaefe1a',
            password=password,  # "7Q3xmUgDqYxM",
            version=version  # "2017-05-26"
        )

    def getAllWorkspaces(self):
        response = self.conversation.list_workspaces()
        print(json.dumps(response, indent=2))

    def createWorkspace(self):
        response = self.conversation.create_workspace(
            name='Test Workspace From Python',
            description='This is a test workspace, trying out the Watson Python SDK.',
            language='en'
                     """
                     FOLLOWING PARAMETERS WILL BE ADDED LATER
                     intents
                     entities
                     dialog_nodes
                     counterexamples
                     metadata
                     """
        )
        print(json.dumps(response, indent=2))

    # THIS METHODS RETURNS NO VALUE AT ALL, NOT EVEN A JSON RESPONSE
    def deleteWorkspace(self, workspace_id):
        self.conversation.delete_workspace(
            workspace_id=workspace_id
        )

    def getWorkspace(self, workspace_id):
        response = self.conversation.get_workspace(
            workspace_id=workspace_id,
            export=False or False
        )
        print(json.dumps(response, indent=2))

    def updateWorkspace(self, workspace_id, name, description):
        response = self.conversation.update_workspace(
            workspace_id=workspace_id,
            name=name,
            description=description
        )
        print(json.dumps(response, indent=2))

# updateWorkspace('d8502ff0-977d-4e7f-af3f-3b7bb899ed18', 'New Test Car From Python',
#                 'New Description from the Python SDK')
# getWorkspace('d8502ff0-977d-4e7f-af3f-3b7bb899ed18')
# deleteWorkspace('671d1af6-9030-4561-968f-54b2fe6450ab')
# createWorkspace()
# getWorkspaces()