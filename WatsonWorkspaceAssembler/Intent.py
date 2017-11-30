# !/usr/bin/env python -w
# coding=utf-8
import json
import watson_developer_cloud


class Intent:
    """
    DOCSTRING
    """

    def __init__(self, username=None, password=None, version=None):
        self.conversation = watson_developer_cloud.ConversationV1(
            username=username,  # '46b3dba5-3f3e-4b04-b8f2-38e65eaefe1a',
            password=password,  # "7Q3xmUgDqYxM",
            version=version  # "2017-05-26"
        )

    def getAllIntents(self, workspace_id=None, export=False, page_limit=None, include_count=False, sort=None,
                      cursor=None):
        response = self.conversation.list_intents(
            workspace_id=workspace_id,
            export=export,
            page_limit=page_limit,
            include_count=include_count,
            sort=sort,
            cursor=cursor
        )
        print(json.dumps(response, indent=2))

    def createIntent(self, workspace_id=None, intent=None, description=None, examples=None):
        response = self.conversation.create_intent(
            workspace_id=workspace_id,
            intent=intent,
            description=description,
            examples=examples
        )
        print(json.dumps(response, indent=2))

    def deleteIntent(self, workspace_id=None, intent=None):
        self.conversation.delete_intent(
            workspace_id=workspace_id,
            intent=intent
        )
        print("[!]Deleted Intent {}[!]".format(intent))

    def getIntent(self, workspace_id, intent, export):
        response = self.conversation.get_intent(
            workspace_id=workspace_id,
            intent=intent,
            export=export
        )
        print(json.dumps(response, indent=2))

    def updateIntent(self, workspace_id=None, intent=None, new_intent=None, new_description=None, new_examples=None):
        response = self.conversation.update_intent(
            workspace_id=workspace_id,
            intent=intent,
            new_intent=new_intent,
            new_description=new_description,
            new_examples=new_examples
        )
        print(json.dumps(response, indent=2))
