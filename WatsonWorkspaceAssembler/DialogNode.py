# !/usr/bin/env python -w
# coding=utf-8
import json
import watson_developer_cloud


class DialogNode:
    """
    DOCSTRING
    """

    def __init__(self, username, password, version):
        self.conversation = watson_developer_cloud.ConversationV1(
            username=username,
            password=password,
            version=version
        )

    def getAllNodes(self, workspace_id=None, page_limit=None, include_count=None, sort=None, cursor=None):
        response = self.conversation.list_dialog_nodes(
            workspace_id=workspace_id,
            page_limit=page_limit,
            include_count=include_count,
            sort=sort,
            cursor=cursor
        )
        print(json.dumps(response, indent=2))

    def createNode(self, workspace_id=None, dialog_node=None, description=None, conditions=None, parent=None,
                   previous_sibling=None, output=None, context=None, metadata=None, next_step=None, actions=None,
                   title=None, node_type=None, event_name=None, variable=None):
        response = self.conversation.create_dialog_node(
            workspace_id=workspace_id,
            dialog_node=dialog_node,
            description=description,
            conditions=conditions,
            parent=parent,
            previous_sibling=previous_sibling,
            output=output,
            context=context,
            metadata=metadata,
            next_step=next_step,
            actions=actions,
            title=title,
            node_type=node_type,
            event_name=event_name,
            variable=variable
        )
        print(json.dumps(response, indent=2))

    def deleteNode(self, workspace_id, dialog_node):
        self.conversation.delete_dialog_node(
            workspace_id=workspace_id,
            dialog_node=dialog_node
        )
        print("[!]Deleted node {}[!]".format(dialog_node))

    def getNode(self, workspace_id, dialog_node):
        response = self.conversation.get_dialog_node(
            workspace_id=workspace_id,
            dialog_node=dialog_node
        )
        print(json.dumps(response, indent=2))

    def updateNode(self, workspace_id=None, dialog_node=None, new_dialog_node=None, new_description=None,
                   new_conditions=None, new_parent=None, new_previous_sibling=None, new_output=None, new_context=None,
                   new_metadata=None, new_next_step=None, new_title=None, new_type=None, new_event_name=None,
                   new_variable=None, new_actions=None):
        response = self.conversation.update_dialog_node(
            workspace_id=workspace_id,
            dialog_node=dialog_node,
            new_dialog_node=new_dialog_node,
            new_description=new_description,
            new_conditions=new_conditions,
            new_parent=new_parent,
            new_previous_sibling=new_previous_sibling,
            new_output=new_output,
            new_context=new_context,
            new_metadata=new_metadata,
            new_next_step=new_next_step,
            new_title=new_title,
            new_type=new_type,
            new_event_name=new_event_name,
            new_variable=new_variable,
            new_actions=new_actions
        )
        print(json.dumps(response, indent=2))
