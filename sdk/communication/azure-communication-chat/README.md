# Azure Communication Service SDK for Python

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

## Set Azure Communication Resource endpoint after it is created
```python
endpoint = "https://<Azure-Communication-Resource-Name>.communications.azure.com"
```

## Request an [User Access Token](https://review.docs.microsoft.com/en-us/azure/project-spool/concepts/user-access-tokens?branch=pr-en-us-104477&tabs=c-sharp%2Cjavascript-simple-token-init%2Ccsharp-shared-credential)
```python
token = "<your token string>"
```

## Create the chat client

```python
from azure.communication.chat import ChatClient
chat_client = ChatClient(token, endpoint)
```

# Key concepts

A chat conversation is represented by a thread. Each user in the thread is called a thread member. Thread members can chat with one another privately in a 1:1 chat or huddle up in a 1:N group chat. Users also get near-real time updates for when others are typing and when they have read the messages.

Once you initialized a `ChatClient` class, you can do the following chat operations:

## Create, get, update, and delete threads

```Python
create_thread(request, correlation_vector=None, **kwargs)
get_thread
update_thread
delete_thread
```

## Send, get, update, and delete messages

```Python
sendMessage
getMessage
getMessages
updateMessage
deleteMessage
```

## Get, add, and remove members

```Python
get_members
add_members
remove_member
```

## Send typing notification

```python
send_typing_notification
```

## Send and get read receipt

```Python
send_read_receipt
get_read_receipts
```

# Examples

The following sections provide several code snippets covering some of the most common tasks, including:

- [Thread Operations](#thread-operations)
- [Message Operations](#message-operations)
- [Thread Member Operations](#thread-member-operations)
- [Events Operations](#event-operations)

## Thread Operations

### Create a thread

Use the `create_thread` method to create a chat thread.
`CreateThreadRequest` is used to describe the thread request, an example is shown in the code snippet below.

- Use `topic` to give a thread topic;
- Use `is_sticky_thread` to specify if the thread's members are mutable, sticky thread has an immutable member list, members cannot be added or removed;
- Use `members` to list the thread members to be added to the thread;

`CreateThreadResponse` is the response returned from creating a thread, it contains an `id` which is the unique ID of the thread.

```Python
from azure.communication.chat.models import CreateThreadRequest, ThreadMember
body = CreateThreadRequest(
            topic="test topic",
            members=[ThreadMember(
                id=<8:user_id, you can get an example from User Access Token's payload 'skypeid' >,
                display_name='name',
                member_role='Admin',
                share_history_time='0'
            )],
            is_sticky_thread=False
 )
create_thread_response = chat_client.create_thread(body)
thread_id = create_thread_response.id;
```

### Get a thread

The `get_thread` method retrieves a thread from the service.
`thread_id` is the unique ID of the thread.

```Python

```

### Update a thread

Use `update_thread` method to update a thread's properties
`thread_id` is the unique ID of the thread.
`UpdateThreadRequest` is used to describe the property change of the thread.

- Use `topic` to give thread a new topic;

```python

```

### Delete a thread

Use `delete_thread` method to delete a thread
`thread_id` is the unique ID of the thread.

```Python

```

## Message Operations

### Send a message

Use `send_message` method to sends a message to a thread identified by threadId.
`CreateMessageRequest` is used to describe the message request, an example is shown in the code snippet below.

- Use `content` to provide the chat message content;
- Use `priority` to specify the message priority level, such as 'Normal' or 'High' ;
- Use `sender_display_name` to specify the display name of the sender;
- Use `client_message_id` to add a client-specific Id in a numeric unsigned Int64 format, which can be used for client deduping.

`MessageResponse` is the response returned from sending a message, it contains an id, which is the unique ID of the message, and a clientMessageId.

```Python

```

### Get a message

The `get_message` method retrieves a message from the service.
`thread_id` is the unique ID of the thread.
`message_id` is the unique ID of the message.

```python

```

### Get messages

The `get_,essages` method retrieves messages from the service.
`thread_id` is the unique ID of the thread.

```Python

```

### Update a message

Use `update_message` to update a message identified by threadId and messageId.
`thread_id` is the unique ID of the thread.
`message_id` is the unique ID of the message.
`UpdateMessageRequest` is used to describe the request of a message update, an example is shown in the code snippet below.

- Use `content` to provide a new chat message content;
- Use `messageType` to specify the message type, such as "Text" or "RichText" ;

```Python

```

### Delete a message

Use `delete_message` to delete a message.
`thread_id` is the unique ID of the thread.
`message_Id` is the unique ID of the message.

```python

```

## Thread Member Operations

### Get thread members

Use `get_members` to retrieve the members of the thread identified by threadId.
`thread_id` is the unique ID of the thread.

```python

```

### Add thread members

Use `add_members` method to add thread members to the thread identified by threadId.
`thread_id` is the unique ID of the thread.
`AddThreadMembersRequest` is used to describe the request of thread members addition, an example is shown in the code snippet below.

- Use `members` to list the thread members to be added to the thread;

```Python

```

### Remove thread member

Use `remove_member` method to remove thread member from the thread identified by threadId.
`thread_id` is the unique ID of the thread.
`member_id` is the ID of the member to be removed from the thread.

```python

```

## Events Operations

### Send typing notification

Use `send_typing_notification` method to post a typing notification event to a thread, on behalf of a user.

```Python

```

### Send read receipt

Use `send_read_receipt` method to post a read receipt event to a thread, on behalf of a user.
`thread_id` is the unique ID of the thread.

```python

```

### Get read receipts

`get_read_receipts` method retreives read receipts for a thread.
`thread_id` is the unique ID of the thread.

```python

```

# Troubleshooting

Running into issues? This section should contain details as to what to do there.

# Next steps

More sample code should go here, along with links out to the appropriate example tests.

# Contributing

If you encounter any bugs or have suggestions, please file an issue in the [Issues](<https://github.com/Azure/azure-sdk-for-python/issues>) section of the project.

![Impressions](https://azure-sdk-impressions.azurewebsites.net/api/impressions/azure-sdk-for-python%2Fsdk%2Ftemplate%2Fazure-template%2FREADME.png)
