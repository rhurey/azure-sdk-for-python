# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Response parameters for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class Response(BaseModel):
    """Response parameters for response.create events."""

    instructions: Optional[str] = None
    """Instructions for the model, similar to system message in chat."""

    temperature: Optional[float] = None
    """Temperature for model sampling, between 0.0 and 2.0."""

    top_p: Optional[float] = None
    """Top-p sampling parameter, between 0.0 and 1.0."""

    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""

    seed: Optional[int] = None
    """Random seed for deterministic results."""

    function_call: Optional[Union[str, Dict[str, Any]]] = None
    """Controls function calling behavior."""