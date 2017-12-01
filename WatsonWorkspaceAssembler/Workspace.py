# !/usr/bin/python
# coding=utf-8
import json
import watson_developer_cloud


class Workspace:
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

    def createWorkspace(self, name=None, description=None, language=None, intents=None, entities=None,
                        dialog_nodes=None, counterexamples=None, metadata=None):
        response = self.conversation.create_workspace(
            name=name,
            description=description,
            language=language,
            intents=intents,
            entities=entities,
            dialog_nodes=dialog_nodes,
            counterexamples=counterexamples,
            metadata=metadata
        )
        print(json.dumps(response, indent=2))

    def deleteWorkspace(self, workspace_id=None):
        self.conversation.delete_workspace(
            workspace_id=workspace_id
        )
        print("[!]Deleted workspace {}[!]".format(workspace_id))

    def getWorkspace(self, workspace_id=None):
        response = self.conversation.get_workspace(
            workspace_id=workspace_id,
            export=False or False
        )
        print(json.dumps(response, indent=2))

    def updateWorkspace(self, workspace_id=None, name=None, description=None, language=None, intents=None, entities=None
                        , dialog_nodes=None, counterexamples=None, metadata=None
                        ):
        response = self.conversation.update_workspace(
            workspace_id=workspace_id,
            name=name,
            description=description,
            language=language,
            intents=intents,
            entities=entities,
            dialog_nodes=dialog_nodes,
            counterexamples=counterexamples,
            metadata=metadata
        )
        print(json.dumps(response, indent=2))

# updateWorkspace('d8502ff0-977d-4e7f-af3f-3b7bb899ed18', 'New Test Car From Python',
#                 'New Description from the Python SDK')
# getWorkspace('d8502ff0-977d-4e7f-af3f-3b7bb899ed18')
# deleteWorkspace('671d1af6-9030-4561-968f-54b2fe6450ab')
# createWorkspace()
# getWorkspaces()
