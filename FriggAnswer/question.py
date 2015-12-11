#/usr/bin/python
# coding: utf-8

from nltk.tokenize import word_tokenize
from tagger import Tagger
import re

class Question:

  def preProcess(self, question):
    if len(question) == 0 or question == None:
      return [u'escreve algo primeiro!']
    elif len(question) > 200:
      return[u'Isso está muito grande. Diminua!']
    else:
      token = word_tokenize(question.lower())
      if(len(token) < 3):
        return [u'algo está errado!']
      return token

  def genKeyWords(self, question):
    questionToken = self.preProcess(question)
    tagger = Tagger('portugues')
    token = tagger.classify(questionToken)
    keyList = []
    for tok in token:
      if tok[1] == 'N' or re.match('ADJ', tok[1]) or re.match('V', tok[1]):
        keyList.append(tok)
    print keyList
    print len(keyList)
    return keyList


