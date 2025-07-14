

# Azure Ai VoiceLive client library for Python

Azure AI VoiceLive provides a multi-modal conversational AI service that enables real-time interactions with AI models through text and audio modalities. This library enables WebSocket-based realtime communication with the Azure AI VoiceLive service.

## Getting started

### Install the package

```bash
python -m pip install azure-ai-voicelive
```

For WebSocket support, you'll also need to install the websockets package:

```bash
python -m pip install websockets
```

#### Prerequisites

- Python 3.8 or later is required to use this package.
- You need an [Azure subscription][azure_sub] to use this package.
- An existing Azure AI VoiceLive resource.

## Key concepts

### WebSocket Realtime API

The WebSocket-based realtime API allows you to create multi-modal conversational experiences with real-time communication. Here's how to use it:

### Synchronous API

```python
from azure.ai.voicelive import Realtime

# Create the client (placeholder)
client = None  # Will be available in the future
realtime = Realtime(client)

# Connect to the WebSocket
with realtime.connect(model="your-model-name") as connection:
    # Configure the session
    connection.session.update(session={"modalities": ["text"]})
    
    # Create a conversation item
    connection.conversation.item.create(
        item={
            "type": "message",
            "role": "user", 
            "content": [{"type": "input_text", "text": "Hello! How are you today?"}]
        }
    )
    
    # Request a response
    connection.response.create()
    
    # Process events
    for event in connection:
        if event.get("type") == "response.text.delta":
            print(event.get("delta"), end="", flush=True)
        elif event.get("type") == "response.text.done":
            print()
        elif event.get("type") == "response.done":
            break
```

### Asynchronous API

```python
import asyncio
from azure.ai.voicelive.aio import Realtime

# Create the client (placeholder)
client = None  # Will be available in the future
realtime = Realtime(client)

async def main():
    # Connect to the WebSocket
    async with realtime.connect(model="your-model-name") as connection:
        # Configure the session
        await connection.session.update(session={"modalities": ["text"]})
        
        # Create a conversation item
        await connection.conversation.item.create(
            item={
                "type": "message",
                "role": "user", 
                "content": [{"type": "input_text", "text": "Hello! How are you today?"}]
            }
        )
        
        # Request a response
        await connection.response.create()
        
        # Process events
        async for event in connection:
            if event.get("type") == "response.text.delta":
                print(event.get("delta"), end="", flush=True)
            elif event.get("type") == "response.text.done":
                print()
            elif event.get("type") == "response.done":
                break

asyncio.run(main())
```

## Resources

The SDK provides the following resources for the WebSocket API:

- `session` - Configure the session parameters
- `response` - Create and manage responses from the model
- `conversation` - Manage the conversation history
  - `item` - Create, delete, retrieve, and truncate conversation items

Each resource provides methods to interact with the WebSocket API according to the Azure AI VoiceLive protocol.

## Contributing

This project welcomes contributions and suggestions. Most contributions require
you to agree to a Contributor License Agreement (CLA) declaring that you have
the right to, and actually do, grant us the rights to use your contribution.
For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether
you need to provide a CLA and decorate the PR appropriately (e.g., label,
comment). Simply follow the instructions provided by the bot. You will only
need to do this once across all repos using our CLA.

This project has adopted the
[Microsoft Open Source Code of Conduct][code_of_conduct]. For more information,
see the Code of Conduct FAQ or contact opencode@microsoft.com with any
additional questions or comments.

<!-- LINKS -->
[code_of_conduct]: https://opensource.microsoft.com/codeofconduct/
[authenticate_with_token]: https://docs.microsoft.com/azure/cognitive-services/authentication?tabs=powershell#authenticate-with-an-authentication-token
[azure_identity_credentials]: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#credentials
[azure_identity_pip]: https://pypi.org/project/azure-identity/
[default_azure_credential]: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#defaultazurecredential
[pip]: https://pypi.org/project/pip/
[azure_sub]: https://azure.microsoft.com/free/

