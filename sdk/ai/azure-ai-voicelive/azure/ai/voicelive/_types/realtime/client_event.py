# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Client event types for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union, cast

from pydantic import BaseModel, Field

from .conversation_item_param import ConversationItem
from .session_update_params import Session
from .response_params import Response


class ClientEventType(str, Enum):
    """Types of client events for the Azure AI VoiceLive realtime API."""

    SESSION_UPDATE = "session.update"
    RESPONSE_CREATE = "response.create"
    RESPONSE_CANCEL = "response.cancel"
    INPUT_AUDIO_BUFFER_CLEAR = "input_audio_buffer.clear"
    INPUT_AUDIO_BUFFER_COMMIT = "input_audio_buffer.commit"
    INPUT_AUDIO_BUFFER_APPEND = "input_audio_buffer.append"
    CONVERSATION_ITEM_DELETE = "conversation.item.delete"
    CONVERSATION_ITEM_CREATE = "conversation.item.create"
    CONVERSATION_ITEM_TRUNCATE = "conversation.item.truncate"
    CONVERSATION_ITEM_RETRIEVE = "conversation.item.retrieve"
    OUTPUT_AUDIO_BUFFER_CLEAR = "output_audio_buffer.clear"


class VoiceLiveClientEvent(BaseModel):
    """Base class for all client events sent to the Azure AI VoiceLive service."""

    type: ClientEventType
    event_id: Optional[str] = None

    def to_json(
        self, *, use_api_names: bool = True, exclude_defaults: bool = True, exclude_unset: bool = True
    ) -> str:
        """Convert the event to a JSON string.

        :param bool use_api_names: Whether to use API names (vs. Python names)
        :param bool exclude_defaults: Whether to exclude default values
        :param bool exclude_unset: Whether to exclude unset values
        :return: JSON string representation of the event
        :rtype: str
        """
        return json.dumps(
            self.dict(by_alias=use_api_names, exclude_defaults=exclude_defaults, exclude_unset=exclude_unset)
        )


class SessionUpdateEvent(VoiceLiveClientEvent):
    """Event to update the session configuration."""

    type: ClientEventType = ClientEventType.SESSION_UPDATE
    session: Session


class ResponseCreateEvent(VoiceLiveClientEvent):
    """Event to create a new response."""

    type: ClientEventType = ClientEventType.RESPONSE_CREATE
    response: Optional[Response] = None


class ResponseCancelEvent(VoiceLiveClientEvent):
    """Event to cancel an in-progress response."""

    type: ClientEventType = ClientEventType.RESPONSE_CANCEL
    response_id: Optional[str] = None


class InputAudioBufferClearEvent(VoiceLiveClientEvent):
    """Event to clear the input audio buffer."""

    type: ClientEventType = ClientEventType.INPUT_AUDIO_BUFFER_CLEAR


class InputAudioBufferCommitEvent(VoiceLiveClientEvent):
    """Event to commit the input audio buffer."""

    type: ClientEventType = ClientEventType.INPUT_AUDIO_BUFFER_COMMIT


class InputAudioBufferAppendEvent(VoiceLiveClientEvent):
    """Event to append audio to the input audio buffer."""

    type: ClientEventType = ClientEventType.INPUT_AUDIO_BUFFER_APPEND
    audio: str


class ConversationItemDeleteEvent(VoiceLiveClientEvent):
    """Event to delete a conversation item."""

    type: ClientEventType = ClientEventType.CONVERSATION_ITEM_DELETE
    item_id: str


class ConversationItemCreateEvent(VoiceLiveClientEvent):
    """Event to create a new conversation item."""

    type: ClientEventType = ClientEventType.CONVERSATION_ITEM_CREATE
    item: ConversationItem
    previous_item_id: Optional[str] = None


class ConversationItemTruncateEvent(VoiceLiveClientEvent):
    """Event to truncate a conversation item."""

    type: ClientEventType = ClientEventType.CONVERSATION_ITEM_TRUNCATE
    item_id: str
    audio_end_ms: int
    content_index: int


class ConversationItemRetrieveEvent(VoiceLiveClientEvent):
    """Event to retrieve a conversation item."""

    type: ClientEventType = ClientEventType.CONVERSATION_ITEM_RETRIEVE
    item_id: str


class OutputAudioBufferClearEvent(VoiceLiveClientEvent):
    """Event to clear the output audio buffer."""

    type: ClientEventType = ClientEventType.OUTPUT_AUDIO_BUFFER_CLEAR