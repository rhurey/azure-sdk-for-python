# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Conversation resource implementation for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, Any, Optional

from .._base_resource import BaseRealtimeResource
from .conversation_item import VoiceLiveConversationItemResource


class VoiceLiveConversationResource(BaseRealtimeResource):
    """Resource for managing conversations in a WebSocket connection."""

    def __init__(self, connection: Any) -> None:
        """Initialize a new conversation resource.

        :param connection: The WebSocket connection.
        :type connection: VoiceLiveConnection
        """
        super().__init__(connection)
        self.item = VoiceLiveConversationItemResource(connection)