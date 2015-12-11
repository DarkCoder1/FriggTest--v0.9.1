#/usr/bin/python
# coding: utf-8

from django.db import models

from inference import Search
from question import Question
from backend import SearchEngine, create_bag
from messages import return_message
#from django.db.models.loading import get_model

question = Question()
inferencer = Search()

#model = get_model('backend', 'say_work')

def answer(perg):
    if perg == None or perg == "" or perg is None or len(perg) <=2:
        return u"Escreva algo para que eu possa responder!"
    key = question.genKeyWords(perg)
    files = get_data(key)
    if files is None:
        return u"Eu não tenho ideia!"
    else:
        res = inferencer.search(key, files)
        return return_data(res)

def answer_file(perg, file):
    if perg == "" or perg is None or len(perg) <=2:
        return u"Escreva algo para que eu possa responder!"
    key = question.genKeyWords(perg)
    arch = create_bag(file.read().decode('utf-8-sig'))
    res = inferencer.search_file(key, arch)
    return return_data_files(res)

def get_data(key):
    files = []
    for k in key:
        file = SearchEngine().search(k[0])
        if file is not None:
            if file not in files:
                files += file
    if files is not None:
        return get_best_files(files)
    return None

def get_best_files(paragraphs):
    if len(paragraphs) == 1:
        return paragraphs
    elif len(set(paragraphs)) != len(paragraphs):
        para = [p for p in paragraphs if paragraphs.count(p) > 1]
        return set(para)
    else:
        return paragraphs


def return_data(result):
    message = u''+return_message()
    for r in result:
        message += "\n\n" + r
    return message

def return_data_files(result):
    message = u''+return_message()
    message += "\n\n" + ' '.join(result)
    return message