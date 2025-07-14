# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Async response resource implementation for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, Any, Optional

from .._base_resource import BaseRealtimeResource
from ...._types.realtime.client_event import ResponseCreateEvent, ResponseCancelEvent
from ...._types.realtime.response_params import Response


class VoiceLiveResponseResource(BaseRealtimeResource):
    """Resource for managing responses in a WebSocket connection."""

    async def create(self, *, response: Optional[Response] = None, event_id: Optional[str] = None) -> None:
        """Create a new response from the model.

        This event instructs the server to create a Response, which means triggering
        model inference. When in Server VAD mode, the server will create Responses
        automatically.

        A Response will include at least one Item, and may have two, in which case
        the second will be a function call. These Items will be appended to the
        conversation history.

        The server will respond with a `response.created` event, events for Items
        and content created, and finally a `response.done` event to indicate the
        Response is complete.

        The `response.create` event includes inference configuration like
        `instructions`, and `temperature`. These fields will override the Session's
        configuration for this Response only.

        :param response: Optional response configuration.
        :type response: Response
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ResponseCreateEvent(response=response, event_id=event_id)
        await self._connection.send(event)

    async def cancel(self, *, response_id: Optional[str] = None, event_id: Optional[str] = None) -> None:
        """Cancel an in-progress response.

        The server will respond with a `response.cancelled` event or an error 
        if there is no response to cancel.

        :param response_id: Optional ID of the response to cancel.
        :type response_id: str
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = ResponseCancelEvent(response_id=response_id, event_id=event_id)
        await self._connection.send(event)