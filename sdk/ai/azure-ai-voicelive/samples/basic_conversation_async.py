# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------

"""
FILE: basic_conversation_async.py
DESCRIPTION:
    This sample demonstrates a basic text conversation with the Azure AI VoiceLive API
    using the WebSocket-based realtime API asynchronously.

USAGE:
    python basic_conversation_async.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_VOICELIVE_ENDPOINT - The endpoint of your Azure AI VoiceLive resource.
    2) AZURE_VOICELIVE_API_KEY - The API key of your Azure AI VoiceLive resource.
"""

import os
import asyncio
from azure.identity.aio import DefaultAzureCredential
from azure.ai.voicelive.aio import Realtime

# Get credentials and create client
endpoint = os.environ.get("AZURE_VOICELIVE_ENDPOINT")
key = os.environ.get("AZURE_VOICELIVE_API_KEY")

# You can also use DefaultAzureCredential instead of API key
# credential = DefaultAzureCredential()

# Create the VoiceLive client (this is a placeholder, actual API will be released later)
client = None  # Will be implemented when VoiceLiveClient is available
realtime = Realtime(client)

async def main():
    """Main function for the sample."""
    print("Azure AI VoiceLive - Basic Conversation Async Sample")
    
    # Connect to the realtime API
    async with realtime.connect(model="your-model-name") as connection:
        # Configure the session for text modality
        await connection.session.update(session={"modalities": ["text"]})
        
        # Send a message
        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello! How are you today?"}]
            }
        )
        
        # Request a response
        await connection.response.create()
        
        # Listen for events
        async for event in connection:
            if event.get("type") == "response.text.delta":
                print(event.get("delta"), end="", flush=True)
            elif event.get("type") == "response.text.done":
                print()
            elif event.get("type") == "response.done":
                break
            elif event.get("type") == "error":
                print(f"Error: {event.get('message')}")
                break

if __name__ == "__main__":
    asyncio.run(main())