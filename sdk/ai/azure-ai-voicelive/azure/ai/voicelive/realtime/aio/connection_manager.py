# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Async WebSocket connection manager implementation for Azure AI VoiceLive."""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Optional, Dict, Any, Type

import httpx

from .connection import VoiceLiveConnection
from ..._types.websocket_connection_options import WebsocketConnectionOptions

_LOGGER = logging.getLogger(__name__)


class VoiceLiveConnectionManager:
    """Async connection manager for VoiceLiveConnection.

    This class provides a context manager for managing WebSocket connections
    to the Azure AI VoiceLive service.

    :param client: The Azure AI VoiceLive client
    :type client: azure.ai.voicelive.aio.VoiceLiveClient
    :param model: The model to use
    :type model: str
    :param extra_query: Additional query parameters
    :type extra_query: Dict[str, str]
    :param extra_headers: Additional headers
    :type extra_headers: Dict[str, str]
    :param websocket_connection_options: WebSocket connection options
    :type websocket_connection_options: WebsocketConnectionOptions
    """

    def __init__(
        self,
        *,
        client: Any,
        model: str,
        extra_query: Dict[str, str] = None,
        extra_headers: Dict[str, str] = None,
        websocket_connection_options: WebsocketConnectionOptions = None,
    ) -> None:
        """Initialize a new VoiceLiveConnectionManager.

        :param client: The Azure AI VoiceLive client
        :type client: azure.ai.voicelive.aio.VoiceLiveClient
        :param model: The model to use
        :type model: str
        :param extra_query: Additional query parameters
        :type extra_query: Dict[str, str]
        :param extra_headers: Additional headers
        :type extra_headers: Dict[str, str]
        :param websocket_connection_options: WebSocket connection options
        :type websocket_connection_options: WebsocketConnectionOptions
        """
        self.__client = client
        self.__model = model
        self.__connection: Optional[VoiceLiveConnection] = None
        self.__extra_query = extra_query or {}
        self.__extra_headers = extra_headers or {}
        self.__websocket_connection_options = websocket_connection_options or {}

    async def __aenter__(self) -> VoiceLiveConnection:
        """Enter the context manager and connect to the WebSocket.

        :return: The VoiceLiveConnection
        :rtype: VoiceLiveConnection
        """
        try:
            from websockets.asyncio.client import connect
        except ImportError as exc:
            raise ImportError("You need to install `websockets` to use the WebSocket API") from exc

        # Prepare URL and connection parameters
        url = self._prepare_url()
        _LOGGER.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            _LOGGER.debug("Connection options: %s", self.__websocket_connection_options)

        # Connect to the WebSocket
        self.__connection = VoiceLiveConnection(
            await connect(
                str(url),
                additional_headers={
                    **(await self.__client._get_auth_headers()),  # pylint: disable=protected-access
                    "Azure-Beta": "voicelive-realtime=v1",
                    **(self.__extra_headers or {}),
                },
                **self.__websocket_connection_options,
            )
        )

        return self.__connection

    # Alias for aenter that can be called directly
    enter = __aenter__

    def _prepare_url(self) -> httpx.URL:
        """Prepare the WebSocket URL.

        :return: The WebSocket URL
        :rtype: httpx.URL
        """
        if self.__client._websocket_base_url is not None:  # pylint: disable=protected-access
            base_url = httpx.URL(self.__client._websocket_base_url)  # pylint: disable=protected-access
        else:
            base_url = httpx.URL(self.__client._endpoint)  # pylint: disable=protected-access
            base_url = base_url.copy_with(scheme="wss")

        merge_raw_path = base_url.raw_path.rstrip(b"/") + b"/realtime"
        url = base_url.copy_with(
            raw_path=merge_raw_path,
            params={
                **base_url.params,
                "model": self.__model,
                **self.__extra_query,
            },
        )
        return url

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Exit the context manager and close the WebSocket.

        :param exc_type: The exception type, if any
        :type exc_type: Type[BaseException]
        :param exc: The exception, if any
        :type exc: BaseException
        :param exc_tb: The exception traceback, if any
        :type exc_tb: TracebackType
        """
        if self.__connection is not None:
            await self.__connection.close()
            self.__connection = None