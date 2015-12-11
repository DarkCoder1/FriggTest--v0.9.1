__author__ = 'Bruno'
import xml.etree.ElementTree as et
import random, os

xml = os.path.abspath('FriggAnswer') + '/static/FriggAnswer/strings.xml'
tree = et.parse(xml)
root = tree.getroot()

def search_messages(tag):
    responses = []
    for element in root.iter(tag):
        messages = element.getchildren()
        for m in messages:
            responses.append(m.text)
    return responses

def intro_message():
    messages = search_messages('message-intro')
    rand = random.randrange(len(messages) - 1)
    return messages[rand]

def error_message():
    messages = search_messages('message-error')
    rand = random.randrange(len(messages))
    return messages[rand]

def return_message():
    messages = search_messages('message-found')
    rand = random.randrange(len(messages))
    return messages[rand]