"""Process the message queue."""
# Your imports here
import os
import json
import uuid
import random

# Define your constants here
ROOT = os.path.abspath(os.getcwd())
DATA_ROOT = os.path.dirname(ROOT)
QUEUE_ROOT = os.path.join(ROOT, "queue")
USERS_ROOT = os.path.join(ROOT, "users")

# You can use the following structure of functions or make your own.

# Sending a message means adding a new file to the directory unread
# A notification is sent similarly to the way a massage is sent

# unread directory
# sent directory queue/sent
# root directory messages.log  Message {queue_file_name} processed with status {True/False}.
# user_name directory read directory unread directory user_name/read, user_name/unread
# this user directory will be created, if they don't exist already, right before sending a message or notification


def parse_message(text):
    """Convert a text message into a dictionary."""
    lst = []
    message_dict = {}
    with open(os.path.join(QUEUE_ROOT, text), "r") as message:
        message_list = message.readlines()
        for line in message_list:
            splited = line.split(":")
            lst.append(splited)
        for i in lst:
            key = i[0]
            for j in i[1:]:
                if key not in message_dict:
                    message_dict[key] = {}
                message_dict[key] = j

    return message_dict


def create_user_directories(user):
    """Create a new user directory tree."""
    path_user = os.path.join(USERS_ROOT, user)
    path_read = os.path.join(path_user, 'read')
    path_unread = os.path.join(path_user, 'unread')
    os.makedirs(path_user, exist_ok=True)
    os.makedirs(path_read, exist_ok=True)
    os.makedirs(path_unread, exist_ok=True)


def create_file_name():
    """Create a unique name."""
    file_format = ".txt"
    file_name = str(uuid.uuid4()) + file_format

    return file_name


def send_message(message):
    """Send a message to a user."""
    log_path = os.path.join(ROOT, "messages.log")
    if random.random() > 0.5:
        to = parse_message(message).get("to")
        to = to.replace("\n", "").strip()
        create_user_directories(to)
        unread = "unread"
        file_name = create_file_name()
        msg = json.dumps(parse_message(message))
        status = True
        with open(
            os.path.join(USERS_ROOT, to, unread ,file_name), "w"
        ) as sending_msg:
            sending_msg.write(msg)

        with open(log_path, "a") as log:
            log_message = f"Message {message} processed with status {status}."
            log.write(log_message + "\n")
        notification(status, message)
        move_to_sent(message)
        return True
    else:
        status = False
        with open(log_path, "a") as log:
            log_message = f"Message {message} processed with status {status}."
            log.write(log_message + "\n")
        notification(status, message)
        return False


def move_to_sent(message):
    """Move the queue file to the queue sent directory."""
    sent = "sent"
    path_sent = os.path.join(QUEUE_ROOT, sent)
    os.makedirs(path_sent, exist_ok=True)
    os.rename(os.path.join(QUEUE_ROOT, message), os.path.join(path_sent, message))


def process_queue():
    """Take the messages in the queue and send them."""
    send_message("1.txt")
    send_message("2.txt")
    send_message("3.txt")
    send_message("4.txt")
    send_message("5.txt")


def notification(status, message):
    """Send notifications according to the message status."""
    sender = parse_message(message).get("from")
    sender = sender.replace("\n", "").strip()
    to = parse_message(message).get("to")
    to = to.replace("\n", "").strip()
    title = parse_message(message).get("title")
    title = title.replace("\n", "").strip()
    path_ok = os.path.join(ROOT, "templates", "ok.txt")
    path_ko = os.path.join(ROOT, "templates", "ko.txt")
    path_sender = os.path.join(USERS_ROOT, sender, 'unread')
    file_name = create_file_name()
    create_user_directories(sender)
    if status:
        with open(path_ok, "r") as ok:
            ok_txt = ok.read()
            ok_txt = ok_txt.format(sender=sender, to=to, title=title)
        with open(path_sender + file_name, "w") as notifcation_ok:
            notifcation_ok.write(ok_txt)
    else:
        with open(path_ko, "r") as ko:
            ko_txt = ko.read()
            ko_txt = ko_txt.format(sender=sender, to=to, title=title)
        with open(path_sender + file_name, "w") as notifcation_ko:
            notifcation_ko.write(ko_txt)


process_queue()
