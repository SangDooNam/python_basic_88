# Manipulating the File System

## Description

In this exercise, we will focus on the `os` and `os.path` modules to manipulate the directory tree of our file system and we will practice some more with reading and writing files.

##

## Task

Take a look at the contents of the directory [src/data/messaging](src/data/messaging).

```
+ messaging
  + queue
    + sent (empty directory)
    - 1.txt
    - 2.txt
    - 3.txt
    - 4.txt
    - 5.txt
  + templates
    - ok.txt
    - ko.txt
  + users (empty directory)
```

You are going to emulate a system that sends messages between users. Every time a user writes a message on the web front-end, the details about the message will appear in the queue (as a file in the `queue` directory).

Your task is to deliver these messages and notify the users about the outcome of the delivery. Your script will have to do the following:

1. Look at the contents of the queue directory and see if there are any files in it.
2. For each file in that directory you will have to send the message.
3. Sending a message means adding a new file (with an autogenerated name) to the directory `unread` of the user who is the receiver of the message (in the `users` directory).
4. The delivered message must be a JSON representation of the initial message, not a copy of the original file in the queue.
5. If the sending succeeds, then:

    1. the original file in the `queue` directory should be moved to the `queue/sent` directory.
    2. the user who sent the message should receive a notification based on the template `ok.txt` (in the `templates` directory). *A notification is sent similarly to the way a message is sent, but storing the content as plain text and not a JSON string.*
6. If the sending does not succeed, then:

    1. the user who sent the message should receive a notification based on the template `ko.txt` (in the `templates` directory).
7. Once a message has been processed, you should append the result to a log file named `messages.log` that will be placed on the root directory of the project. Each message should add a line saying `Message {queue_file_name} processed with status {True/False}`.

For the system to work, you will have to check if the users (the `from` and `to` of the messages) have the required user directory tree and create it if they don't. Users with notifications or messages should have a directory in the `users` directory with the following tree:

```
+ users
  + {user_name}
    + read
    + unread
  + ...
```

These directories will be created, if they don't exist already, right before sending a message or a notification, so users without messages or notifications will not have a directory in the tree.

> Hints:
>
> - Define the ROOT paths of the system. You may want to define ROOT and DATA_ROOT, but maybe also QUEUE_ROOT or USERS_ROOT.
> - Once you identified the message files to send, start by converting the text content into Python dictionaries with the keys `from`, `to`, `title` and `body`. You can use these dictionaries to help you with the rest of the operations.
> - To store the dictionary into a file you will have to convert it into a string first, with the module `json` and the function [json.dumps(dict)](https://docs.python.org/3/library/json.html).
> - You can use the module `uuid` to create unique identifiers for the names of the files created. You can do so with [uuid.uuid4()](https://docs.python.org/3/library/uuid.html#uuid.uuid4).
> - To test the different template notifications (`ok.txt` and `ko.txt`), execute your `send_message` function randomly (i.e. only if  `random.random() > 0.5`).
> - In the same directory you will find a file named `process_queue.py` with a proposed structure and function names. You can use this file as a guide.
> - The content in the log file should not be overwritten, simply added at the end and in a new line.

- Once completed, the `messages.log` file should look similar to this (with random True/False values):

```
Message 4.txt processed with status False.
Message 2.txt processed with status True.
Message 5.txt processed with status False.
Message 1.txt processed with status False.
Message 3.txt processed with status True.

```

- The directory tree should look similar to this (depending on the successful messages):

```
+ messaging
  + queue
    + sent
      - 2.txt
      - 3.txt
    - 1.txt
    - 4.txt
    - 5.txt
  + templates
    - ok.txt
    - ko.txt
  + users
    + Emily
      + read
      + unread
        - 636ab349-e997-4d71-93c2-5152cde968e0.txt
        - d186cd2f-d93f-41ae-bab4-e5efd8436c8e.txt
    + Mary
      + read
      + unread
        - 6c6c3b84-ad94-463f-9392-492d9bf0ce96.txt
        - 1bf3d47b-29ff-4bad-8de9-ecf8bfe6e788.txt
    + Peter
      + read
      + unread
        - 33d37573-762f-4723-b16b-3b1322ee96c5.txt
        - 49c595ba-a7fe-4ec7-bd68-36781be324dc.txt
        - 4d2fd143-15ab-432c-80c4-75f2314ac7d5.txt
```

Confirm it worked as expected. For exemple, the successful messages in this case were 2 and 3, sent both by Emily.

Emily has two notifications:
**636ab349-e997-4d71-93c2-5152cde968e0.txt**
```
Hello Emily,

Your message to "Peter" with the title "Review" has been sent successfully.

Thank you for using our messaging system,

The organization

```

**d186cd2f-d93f-41ae-bab4-e5efd8436c8e.txt**
```
Hello Emily,

Your message to "Mary" with the title "Minutes" has been sent successfully.

Thank you for using our messaging system,

The organization

```

And both Peter and Mary have a file in their unread directory with the delivered message from Emily:
**Mary**
```
{"from": "Emily", "to": "Mary", "title": "Minutes", "body": "Hi Mary,\\nPlease, find attached the minutes of our last meeting."}
```
**Peter**
```
{"from": "Emily", "to": "Peter", "title": "Review", "body": "Hello Peter,\\nI have finished the review. You can find my feedback attached.\\nThe overall impression is very good, but I would advise on improving some parts of the flow. Let me know what do you think\\nBest regards!"}
```

Mary and Peter also have additional notifications about messages not being sent:
**Mary**
```
Hello Mary,

We regret to inform you that your message to "Joe" with the title "Consumables" could not be sent.

We will keep trying and inform you as soon as the message has been delivered.

Thank you for your understanding and your patience,

The organization

```
**Peter**
```
Hello Peter,

We regret to inform you that your message to "Emily" with the title "Review" could not be sent.

We will keep trying and inform you as soon as the message has been delivered.

Thank you for your understanding and your patience,

The organization

```
And:
```
Hello Peter,

We regret to inform you that your message to "Mary" with the title "Request for meeting" could not be sent.

We will keep trying and inform you as soon as the message has been delivered.

Thank you for your understanding and your patience,

The organization

```
