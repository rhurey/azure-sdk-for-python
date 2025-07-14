# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""WebSocket connection implementation for Azure AI VoiceLive."""

from __future__ import annotations

import json
import logging
from typing import Iterator, Any, cast, Optional, Union

from .resources.session import VoiceLiveSessionResource
from .resources.response import VoiceLiveResponseResource
from .resources.conversation import VoiceLiveConversationResource
from .._types.websocket_connection_options import WebsocketConnectionOptions

_LOGGER = logging.getLogger(__name__)


class VoiceLiveConnection:
    """Represents a live WebSocket connection to the Azure AI VoiceLive API.

    This connection provides methods to send and receive data over the WebSocket connection.
    It is designed to be immutable and thread-safe.

    :param connection: The underlying WebSocket connection.
    :type connection: websockets.sync.client.ClientConnection
    """

    def __init__(self, connection) -> None:
        """Initialize a new VoiceLiveConnection.

        :param connection: The underlying WebSocket connection.
        :type connection: websockets.sync.client.ClientConnection
        """
        self._connection = connection
        
        # Initialize resource access
        self.session = VoiceLiveSessionResource(self)
        self.response = VoiceLiveResponseResource(self)
        self.conversation = VoiceLiveConversationResource(self)

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator over server events.

        This is an infinite-iterator that will continue to yield events until
        the connection is closed.

        :yields: Server events from the WebSocket connection.
        """
        from websockets.exceptions import ConnectionClosedOK

        try:
            while True:
                yield self.recv()
        except ConnectionClosedOK:
            return

    def recv(self) -> Any:
        """Receive the next message from the connection and parse it into an event object.

        Canceling this method is safe. There's no risk of losing data.

        :return: The parsed server event.
        :rtype: Any
        """
        return self.parse_event(self.recv_bytes())

    def recv_bytes(self) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into an event object like `.recv()` does,
        then you can call `.parse_event(data)`.

        :return: The raw message bytes.
        :rtype: bytes
        """
        message = self._connection.recv(decode=False)
        _LOGGER.debug(f"Received websocket message: %s", message)
        return message

    def send(self, event: Any) -> None:
        """Send an event to the server.

        :param event: The event to send.
        :type event: Any
        """
        # Handle both Pydantic models and dictionaries
        if hasattr(event, "to_json"):
            data = event.to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
        else:
            data = json.dumps(event)
        self._connection.send(data)

    def close(self, *, code: int = 1000, reason: str = "") -> None:
        """Close the WebSocket connection.

        :param code: The WebSocket close code.
        :type code: int
        :param reason: The WebSocket close reason.
        :type reason: str
        """
        self._connection.close(code=code, reason=reason)

    def parse_event(self, data: Union[str, bytes]) -> Any:
        """Parse raw data into a server event object.

        This is helpful if you're using `.recv_bytes()`.

        :param data: The raw data to parse.
        :type data: str or bytes
        :return: The parsed server event.
        :rtype: Any
        """
        # Will need to be updated to use actual event models once they're created
        return json.loads(data)