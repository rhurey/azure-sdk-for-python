# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Conversation item parameters for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class ConversationItemRole(str, Enum):
    """Role of a conversation item."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"


class ContentType(str, Enum):
    """Type of content in a conversation item."""

    TEXT = "text"
    INPUT_TEXT = "input_text"
    INPUT_AUDIO = "input_audio"
    OUTPUT_AUDIO = "output_audio"
    FUNCTION_CALL = "function_call"


class TextContent(BaseModel):
    """Text content for a conversation item."""

    type: ContentType = ContentType.TEXT
    text: str


class InputTextContent(BaseModel):
    """Input text content for a conversation item."""

    type: ContentType = ContentType.INPUT_TEXT
    text: str


class FunctionCallContent(BaseModel):
    """Function call content for a conversation item."""

    type: ContentType = ContentType.FUNCTION_CALL
    name: str
    arguments: str


class ConversationItem(BaseModel):
    """A conversation item parameter for conversation.item.create events."""

    type: str = "message"
    role: ConversationItemRole
    content: List[Union[TextContent, InputTextContent, FunctionCallContent]]
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None