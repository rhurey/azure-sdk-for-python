# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Azure AI VoiceLive async realtime implementation."""

from typing import Dict, Any, Optional

from .connection_manager import VoiceLiveConnectionManager
from ..._types.websocket_connection_options import WebsocketConnectionOptions


class Realtime:
    """Azure AI VoiceLive async realtime implementation.

    This class provides access to the WebSocket-based realtime API for VoiceLive.
    """

    def __init__(self, client) -> None:
        """Initialize a new Realtime instance.

        :param client: The Azure AI VoiceLive client.
        :type client: azure.ai.voicelive.aio.VoiceLiveClient
        """
        self._client = client

    def connect(
        self,
        *,
        model: str,
        extra_query: Dict[str, str] = None,
        extra_headers: Dict[str, str] = None,
        websocket_connection_options: WebsocketConnectionOptions = None,
    ) -> VoiceLiveConnectionManager:
        """Connect to the Azure AI VoiceLive realtime API.

        :param model: The model to use.
        :type model: str
        :param extra_query: Additional query parameters.
        :type extra_query: Dict[str, str]
        :param extra_headers: Additional headers.
        :type extra_headers: Dict[str, str]
        :param websocket_connection_options: WebSocket connection options.
        :type websocket_connection_options: WebsocketConnectionOptions
        :return: A connection manager for the WebSocket connection.
        :rtype: VoiceLiveConnectionManager
        """
        return VoiceLiveConnectionManager(
            client=self._client,
            model=model,
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )