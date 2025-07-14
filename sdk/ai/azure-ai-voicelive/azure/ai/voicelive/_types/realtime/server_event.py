# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Server event types for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ServerEventType(str, Enum):
    """Types of server events from the Azure AI VoiceLive realtime API."""

    SESSION_UPDATED = "session.updated"
    RESPONSE_CREATED = "response.created"
    RESPONSE_CANCELLED = "response.cancelled"
    RESPONSE_DONE = "response.done"
    RESPONSE_TEXT_DELTA = "response.text.delta"
    RESPONSE_TEXT_DONE = "response.text.done"
    INPUT_AUDIO_BUFFER_CLEARED = "input_audio_buffer.cleared"
    INPUT_AUDIO_BUFFER_COMMITTED = "input_audio_buffer.committed"
    CONVERSATION_ITEM_CREATED = "conversation.item.created"
    CONVERSATION_ITEM_DELETED = "conversation.item.deleted"
    CONVERSATION_ITEM_TRUNCATED = "conversation.item.truncated"
    CONVERSATION_ITEM_RETRIEVED = "conversation.item.retrieved"
    OUTPUT_AUDIO_BUFFER_CLEARED = "output_audio_buffer.cleared"
    ERROR = "error"


class VoiceLiveServerEvent(BaseModel):
    """Base class for all server events received from the Azure AI VoiceLive service."""

    type: ServerEventType
    event_id: Optional[str] = None


class ResponseTextDeltaEvent(VoiceLiveServerEvent):
    """Event for text delta responses from the model."""

    type: ServerEventType = ServerEventType.RESPONSE_TEXT_DELTA
    delta: str
    finish_reason: Optional[str] = None


class ErrorEvent(VoiceLiveServerEvent):
    """Event for errors from the service."""

    type: ServerEventType = ServerEventType.ERROR
    error: Dict[str, Any]
    message: str