# !/usr/bin/env python -w
# coding=utf-8
import json
import watson_developer_cloud


class Entity:
    """
    DOCSTRING
    """

    def __init__(self, username=None, password=None, version=None):
        self.conversation = watson_developer_cloud.ConversationV1(
            username=username,  # '46b3dba5-3f3e-4b04-b8f2-38e65eaefe1a',
            password=password,  # "7Q3xmUgDqYxM",
            version=version  # "2017-05-26"
        )

    def getAllEntities(self, workspace_id):
        response = self.conversation.list_entities(
            workspace_id=workspace_id,
            export=False or False,
            page_limit=10,
            include_count=True  # ,
            # sort=None,
            # cursor=None

        )
        print(json.dumps(response, indent=2))

    def createEntity(self, workspace_id=None, entity=None, description=None, metadata=None, values=None,
                     fuzzy_match=False):
        response = self.conversation.create_entity(
            workspace_id=workspace_id,
            entity=entity,
            description=description,
            metadata=metadata,
            values=values,
            fuzzy_match=fuzzy_match
        )
        print(json.dumps(response, indent=2))

    def deleteEntity(self, workspace_id, entity):
        self.conversation.delete_entity(
            workspace_id=workspace_id,
            entity=entity
        )
        print("[!]Deleted Entity {}[!]".format(entity))

    def getEntity(self, worksapace_id, entity):
        response = self.conversation.get_entity(
            workspace_id=worksapace_id,
            entity=entity
        )
        print(json.dumps(response, indent=2))

    def updateEntity(self, workspace_id, entity, new_entity, new_description, new_metadata, new_values):
        response = self.conversation.update_entity(
            workspace_id=workspace_id,
            entity=entity,
            new_entity=new_entity,
            new_description=new_description,
            new_metadata=new_metadata,
            new_fuzzy_match=False or True,
            new_values=new_values
        )
        print(json.dumps(response, indent=2))
