# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""Session update parameters for Azure AI VoiceLive WebSocket API."""

from __future__ import annotations

from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field


class FunctionDefinition(BaseModel):
    """A function definition for the service."""

    name: str
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class Session(BaseModel):
    """Session parameters for session.update events."""

    modalities: Optional[List[str]] = None
    """The modalities to enable for this session, e.g., ["text", "audio"]."""

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

    functions: Optional[List[FunctionDefinition]] = None
    """Function definitions available to the model."""

    tools: Optional[List[Dict[str, Any]]] = None
    """Tool definitions available to the model."""

    voice: Optional[str] = None
    """Voice ID to use for audio responses."""

    function_call: Optional[Union[str, Dict[str, Any]]] = None
    """Controls function calling behavior."""