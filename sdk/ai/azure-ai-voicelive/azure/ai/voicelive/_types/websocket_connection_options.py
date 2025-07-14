# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Type definitions for WebSocket connection options."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence, Tuple, Union
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from websockets import Subprotocol
    from websockets.extensions import ClientExtensionFactory


class WebsocketConnectionOptions(TypedDict, total=False):
    """WebSocket connection options copied from `websockets`.

    For example: https://websockets.readthedocs.io/en/stable/reference/asyncio/client.html#websockets.asyncio.client.connect

    :keyword Sequence[ClientExtensionFactory] extensions: List of supported extensions, in order in which they should be
        negotiated and run.
    :keyword Sequence[Subprotocol] subprotocols: List of supported subprotocols, in order of decreasing preference.
    :keyword str compression: The "permessage-deflate" extension is enabled by default. Set compression to None to disable
        it. See the compression guide for details.
    :keyword int max_size: Maximum size of incoming messages in bytes. None disables the limit.
    :keyword int max_queue: or tuple[int, int]: High-water mark of the buffer where frames are received. It defaults to
        16 frames. The low-water mark defaults to max_queue // 4. You may pass a (high, low) tuple to set the high-water
        and low-water marks. If you want to disable flow control entirely, you may set it to None, although that's a bad
        idea.
    :keyword int write_limit: or tuple[int, int]: High-water mark of write buffer in bytes. It is passed to
        set_write_buffer_limits(). It defaults to 32 KiB. You may pass a (high, low) tuple to set the high-water and
        low-water marks.
    """

    extensions: Optional[Sequence[ClientExtensionFactory]]
    subprotocols: Optional[Sequence[Subprotocol]]
    compression: Optional[str]
    max_size: Optional[int]
    max_queue: Optional[Union[int, Tuple[Optional[int], Optional[int]]]]
    write_limit: Optional[Union[int, Tuple[int, Optional[int]]]]