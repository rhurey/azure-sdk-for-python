# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Base resource implementation for Azure AI VoiceLive WebSocket API resources."""

from typing import Any


class BaseRealtimeResource:
    """Base class for all realtime resources."""

    def __init__(self, connection: Any) -> None:
        """Initialize a new resource.

        :param connection: The WebSocket connection.
        :type connection: VoiceLiveConnection
        """
        self._connection = connection