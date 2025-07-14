# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Async session resource implementation for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, Any, Optional

from .._base_resource import BaseRealtimeResource
from ...._types.realtime.client_event import SessionUpdateEvent
from ...._types.realtime.session_update_params import Session


class VoiceLiveSessionResource(BaseRealtimeResource):
    """Resource for managing the session in a WebSocket connection."""

    async def update(self, *, session: Session, event_id: Optional[str] = None) -> None:
        """Update the session configuration.

        The client may send this event at any time to update any field,
        except for `voice`. However, note that once a session has been
        initialized with a particular `model`, it can't be changed to
        another model using `session.update`.

        When the server receives a `session.update`, it will respond
        with a `session.updated` event showing the full, effective configuration.
        Only the fields that are present are updated. To clear a field like
        `instructions`, pass an empty string.

        :param session: The session configuration to update.
        :type session: Session
        :param event_id: Optional event ID for correlation.
        :type event_id: str
        """
        event = SessionUpdateEvent(session=session, event_id=event_id)
        await self._connection.send(event)