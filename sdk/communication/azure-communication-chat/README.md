[![Build Status](https://dev.azure.com/azure-sdk/public/_apis/build/status/azure-sdk-for-python.client?branchName=master)](https://dev.azure.com/azure-sdk/public/_build/latest?definitionId=46?branchName=master)

# Azure Communication Configuration Package client library for Python

This package contains a Python SDK for Azure Communication Services for Chat.
Read more about Azure Communication Services [here](https://review.docs.microsoft.com/en-us/azure/project-spool/overview?branch=pr-en-us-104477)

# Getting started

## Prerequisites

- Python 2.7, or 3.5 or later is required to use this package.
- An Azure Communication Resource, learn how to create one from [Create an Azure Communication Resource](https://review.docs.microsoft.com/en-us/azure/project-spool/quickstarts/create-a-communication-resource?branch=pr-en-us-104477)

## Install the package

Install the Azure Communication Service SDK

```bash
pip install azure-communication-chat
```

## User Access Tokens

User access tokens enable you to build client applications that directly authenticate to Azure Communication Services. You can generate these tokens with azure.communication.configuration module, and then use them to initialize the Communication Services SDKs. Example of using azure.communication.configuration:

```bash
pip install azure-communication-configuration
```

```python
from azure.communication.configuration._user_management_client import UserManagementClient
user_token_client = UserManagementClient.from_connection_string("<connection string of your Communication Resource>")
token_response = user_token_client.user_management.issue_token(scopes=["chat"])
token = token_response.token
```

You may also want to set the user identity from token_response.token.identity because that user should be added as a member of list[ThreadMember] when you creating
a new chat thread with this token. It is because the initiator of the create request must be in the list of the members of the chat thread.

```python
user_id = token_response.identity
```

## Create the chat client

```python
from azure.communication.chat import ChatClient
# Your unique Azure Communication service endpoint
endpoint = "https://<RESOURCE_NAME>.communcationservices.azure.com"
token = "<User Access Tokens>"
chat_client = ChatClient(token, endpoint)
```

# Key concepts

A chat conversation is represented by a thread. Each user in the thread is called a thread member. Thread members can chat with one another privately in a 1:1 chat or huddle up in a 1:N group chat. Users also get near-real time updates for when others are typing and when they have read the messages.

Once you initialized a `ChatClient` class, you can do the following chat operations:

## Create, get, update, and delete threads

```Python
create_chat_thread(topic, thread_members, **kwargs)
get_chat_thread(thread_id, **kwargs)
list_chat_threads(**kwargs)
update_chat_thread(thread_id, topic, **kwargs)
delete_chat_thread(thread_id, **kwargs)
```

## Send, get, update, and delete messages

```Python
send_chat_message(thread_id, content, **kwargs)
get_chat_message(thread_id, message_id, **kwargs)
list_chat_messages(thread_id, **kwargs)
update_chat_message(thread_id, message_id, content, **kwargs)
delete_chat_message(thread_id, message_id, **kwargs)
```

## Get, add, and remove members

```Python
list_chat_members(thread_id, **kwargs)
add_chat_members(thread_id, thread_members, **kwargs)
remove_chat_member(thread_id, member_id, **kwargs)
```

## Send typing notification

```python
send_typing_notification(thread_id, **kwargs)
```

## Send and get read receipt

```Python
send_read_receipt(thread_id, message_id, **kwargs)
list_read_receipts(thread_id, **kwargs)
```

# Examples

The following sections provide several code snippets covering some of the most common tasks, including:

- [Thread Operations](#thread-operations)
- [Message Operations](#message-operations)
- [Thread Member Operations](#thread-member-operations)
- [Events Operations](#events-operations)

## Thread Operations

### Create a thread

Use the `create_chat_thread` method to create a chat thread.

- Use `topic` to give a thread topic;
- Use `thread_members` to list the `ThreadMember` to be added to the thread;
- `id`, required, it is the id of the thread member in the formatm ``8:acs:ResourceId_AcsUserId``.
- `display_name`, optional, is the display name for the thread member.
- `share_history_time`, optional, time from which the group chat history is shared with the member in EPOCH time (milliseconds).
'0' means share everything, '-1' means share nothing

`CreateThreadResult` is the result returned from creating a thread, it contains an `id` which is the unique ID of the thread.

```Python
from azure.communication.chat.models import ThreadMember
topic="test topic",
thread_members=[ThreadMember(
    id='<user identity>',
    display_name='name',
    share_history_time='0'
)],

create_thread_result = chat_client.create_chat_thread(topic, thread_members)
thread_id = create_thread_result.id
```

### Get a thread

The `get_chat_thread` method retrieves a thread from the service.
`thread_id` is the unique ID of the thread.

```Python
thread = chat_client.get_chat_thread(thread_id)
```

### Update a thread

Use `update_chat_thread` method to update a thread's properties
`thread_id` is the unique ID of the thread.
`topic` is used to describe the change of the thread topic

- Use `topic` to give thread a new topic;

```python
topic="new topic"
chat_client.update_chat_thread(thread_id, topic)
```

### Delete a thread

Use `delete_chat_thread` method to delete a thread
`thread_id` is the unique ID of the thread.

```Python
chat_client.delete_chat_thread(thread_id)
```

## Message Operations

### Send a message

Use `send_chat_message` method to sends a message to a thread identified by threadId.

- Use `content` to provide the chat message content, it is required
- Use `priority` to specify the message priority level, such as 'Normal' or 'High', if not speficied, 'Normal' will be set
- Use `sender_display_name` to specify the display name of the sender, if not specified, empty name will be set

`CreateMessageResult` is the response returned from sending a message, it contains an id, which is the unique ID of the message.

```Python
from azure.communication.chat.models import MessagePriority

content='hello world'
priority=MessagePriority.NORMAL
sender_display_name='sender name'

create_message_result= chat_client.send_chat_message(thread_id, content, priority=priority, sender_display_name=sender_display_name)
```

### Get a message

The `get_chat_message` method retrieves a message from the service.
`thread_id` is the unique ID of the thread.
`message_id` is the unique ID of the message.

`Message` is the response returned from getting a message, it contains an id, which is the unique ID of the message, and other fields please refer to azure.communication.chat.models.Message

```python
message = chat_client.get_chat_message(thread_id, message_id)
```

### Get messages

The `list_chat_messages` method retrieves messages from the service.
`thread_id` is the unique ID of the thread.

`ListMessagesResult` is the response returned from listing messages, it contains messages field, which is a list of Message, and other fields please refer to azure.communication.chat.models.ListMessagesResult

```Python
list_messages_result = chat_client.list_chat_messages(thread_id)
print(list_messages_result.messages)
```

### Update a message

Use `update_chat_message` to update a message identified by threadId and messageId.
`thread_id` is the unique ID of the thread.
`message_id` is the unique ID of the message.
`conent` is the message content to be updated.

- Use `content` to provide a new chat message content;

```Python
content = "updated message content"
chat_client.update_chat_message(thread_id, message_id, content)
```

### Delete a message

Use `delete_chat_message` to delete a message.
`thread_id` is the unique ID of the thread.
`message_Id` is the unique ID of the message.

```python
chat_client.delete_chat_message(thread_id, message_id)
```

## Thread Member Operations

### Get thread members

Use `list_chat_members` to retrieve the members of the thread identified by threadId.
`thread_id` is the unique ID of the thread.

`[ThreadMember]` is the response returned from listing members

```python
members = chat_client.list_chat_members(thread_id)
for member in members:
    print(member)
```

### Add thread members

Use `add_chat_members` method to add thread members to the thread identified by threadId.
`thread_id` is the unique ID of the thread.

- Use `thread_members` to list the `ThreadMember` to be added to the thread;
- `id`, required, it is the id of the thread member in the formatm ``8:acs:ResourceId_AcsUserId``.
- `display_name`, optional, is the display name for the thread member.
- `share_history_time`, optional, time from which the group chat history is shared with the member in EPOCH time (milliseconds).
'0' means share everything, '-1' means share nothing

```Python
from azure.communication.chat.models import ThreadMember
member = ThreadMember(
    id='<user id>',
    display_name='name',
    share_history_time='0')
thread_members = [member]
chat_client.add_chat_members(self._thread_id, thread_members)
```

### Remove thread member

Use `remove_chat_member` method to remove thread member from the thread identified by threadId.
`thread_id` is the unique ID of the thread.
`member_id` is the ID of the member to be removed from the thread.

```python
chat_client.remove_chatmember(thread_id, member_id)
```

## Events Operations

### Send typing notification

Use `send_typing_notification` method to post a typing notification event to a thread, on behalf of a user.
`thread_id` is the unique ID of the thread.

```Python
chat_client.send_typing_notification(thread_id)
```

### Send read receipt

Use `send_read_receipt` method to post a read receipt event to a thread, on behalf of a user.
`thread_id` is the unique ID of the thread.

```python

chat_client.send_read_receipt(thread_id, mesage_id)
```

### Get read receipts

`list_read_receipts` method retreives read receipts for a thread.
`thread_id` is the unique ID of the thread.

`[ReadReceipt]` is the response returned from listing read receipts

```python
read_receipts = chat_client.list_read_receipts(thread_id)
```

## Sample Code

These are code samples that show common scenario operations with the Azure Communication Chat client library.
The async versions of the samples (the python sample files appended with `_async`) show asynchronous operations,
and require Python 3.5 or later.
Before run the sample code, refer to [Prerequisites](#Prerequisites) to create a resource and get an User Access Token,
and set them into Environment Variables

```bash
set AZURE_COMMUNICATION_SERVICE_ENDPOINT="https://<RESOURCE_NAME>.communcationservices.azure.com"
set TOKEN="<user access token>"
```

```python
pip install pyjwt
python samples\chat_sample.py
python samples\chat_sample_async.py
```

# Troubleshooting

Running into issues? This section should contain details as to what to do there.

# Next steps

More sample code should go here, along with links out to the appropriate example tests.

# Contributing

If you encounter any bugs or have suggestions, please file an issue in the [Issues](<https://github.com/Azure/azure-sdk-for-python/issues>) section of the project.

![Impressions](https://azure-sdk-impressions.azurewebsites.net/api/impressions/azure-sdk-for-python%2Fsdk%2Ftemplate%2Fazure-template%2FREADME.png)
