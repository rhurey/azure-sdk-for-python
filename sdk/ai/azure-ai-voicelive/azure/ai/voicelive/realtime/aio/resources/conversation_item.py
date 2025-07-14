# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Async conversation item resource implementation for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, Any, Optional

from .._base_resource import BaseRealtimeResource
from ...._types.realtime.client_event import (
    ConversationItemCreateEvent,
    ConversationItemDeleteEvent,
    ConversationItemRetrieveEvent,
    ConversationItemTruncateEvent,
)
from ...._types.realtime.conversation_item_param import ConversationItem


class VoiceLiveConversationItemResource(BaseRealtimeResource):
    """Resource for managing conversation items in a WebSocket connection."""

    async def create(
        self, *, item: ConversationItem, previous_item_id: Optional[str] = None, event_id: Optional[str] = None
    ) -> None:
        """Create a new conversation item.

        Add a new Item to the Conversation's context, including messages, function
        calls, and function call responses. This event can be used both to populate a
        "history" of the conversation and to add new items mid-stream, but has the
        current limitation that it cannot populate assistant audio messages.

        If successful, the server will respond with a `conversation.item.created`
        event, otherwise an `error` event will be sent.

        :param item: The conversation item to create.
        :type item: ConversationItem
        :param previous_item_id: Optional ID of the item to insert after.
        :type previous_item_id: str
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ConversationItemCreateEvent(item=item, previous_item_id=previous_item_id, event_id=event_id)
        await self._connection.send(event)

    async def delete(self, *, item_id: str, event_id: Optional[str] = None) -> None:
        """Delete a conversation item.

        Send this event when you want to remove any item from the conversation
        history. The server will respond with a `conversation.item.deleted` event,
        unless the item does not exist in the conversation history, in which case the
        server will respond with an error.

        :param item_id: ID of the item to delete.
        :type item_id: str
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ConversationItemDeleteEvent(item_id=item_id, event_id=event_id)
        await self._connection.send(event)

    async def retrieve(self, *, item_id: str, event_id: Optional[str] = None) -> None:
        """Retrieve a conversation item.

        Send this event when you want to retrieve the server's representation of a
        specific item in the conversation history. This is useful, for example,
        to inspect user audio after noise cancellation and VAD.

        The server will respond with a `conversation.item.retrieved` event,
        unless the item does not exist in the conversation history, in which case the
        server will respond with an error.

        :param item_id: ID of the item to retrieve.
        :type item_id: str
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ConversationItemRetrieveEvent(item_id=item_id, event_id=event_id)
        await self._connection.send(event)

    async def truncate(
        self, *, item_id: str, audio_end_ms: int, content_index: int, event_id: Optional[str] = None
    ) -> None:
        """Truncate a conversation item.

        Send this event to truncate a previous assistant message's audio. The server
        will produce audio faster than realtime, so this event is useful when the user
        interrupts to truncate audio that has already been sent to the client but not
        yet played. This will synchronize the server's understanding of the audio with
        the client's playback.

        Truncating audio will delete the server-side text transcript to ensure there
        is not text in the context that hasn't been heard by the user.

        If successful, the server will respond with a `conversation.item.truncated`
        event.

        :param item_id: ID of the item to truncate.
        :type item_id: str
        :param audio_end_ms: End time in milliseconds.
        :type audio_end_ms: int
        :param content_index: Index of the content to truncate.
        :type content_index: int
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ConversationItemTruncateEvent(
            item_id=item_id, audio_end_ms=audio_end_ms, content_index=content_index, event_id=event_id
        )
        await self._connection.send(event)