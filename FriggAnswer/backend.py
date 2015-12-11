#/usr/bin/python
# coding: utf-8


from nltk.tokenize import sent_tokenize, word_tokenize
from pickle import load, dump
from tagger import Tagger
from nltk.corpus import wordnet as wn
import os, re

def get_files():
    """
    Função auxiliar que retorna um array de arquivos. e os paths dos arquivos
    que vão para a tupla.(creio que um loop deve ser criado para esse fim)
    """
    path_name = os.path.abspath('FriggAnswer')
   # path_name = os.path.abspath('')
    path_files = os.listdir(os.path.abspath(path_name + '/texts/'))
    files = []
    for p in path_files:
        files.append(open(path_name+'/texts/'+'\\'+p))
    return files, (path_name + '/texts/', path_name + '/texts2/')

class SearchEngine:
    """
    classe que considero a principal desse modulo. É a estrutura de dados que
    contém os arquivos para o processamento da engine.
    """
    def __init__(self):
        #  código para carregar o pickle
        self.search_data = {}
        self.load_data()
        #  carregando o tagger
        self.tagger = Tagger('portugues')

    def save(self):
        output = open('data.pkl', 'wb')
        dump(self.search_data, output)
        output.close()

    def insert(self, files):
        """
        Esse método tem como entrada um array de arquivos e uma tupla de path e
        retorna uma lista de indexação reversa.
        """
        for f in files:
            p_count = -1
            paragraph = sent_tokenize(f.read().decode('utf-8').lower())
            for p in paragraph:
                p_count +=1
                words = word_tokenize(p)
                classes = self.tagger.classify(words)
                for c in classes:
                    if re.match('N', c[1]):
                        if self.search_data.has_key(c[0]):
                            names = [n for n,_ in self.search_data[c[0]]]
                            if os.path.basename(f.name) in names:
                                self.search_data[c[0]][names.index(os.path.basename(f.name))][1].append(p_count)
                            else:
                                self.search_data[c[0]].append(((os.path.basename(f.name)),[p_count]))
                        else:
                            self.search_data.update({c[0]:[((os.path.basename(f.name)),[p_count])]})
        self.save()

    def search(self, name):
        """
        Algoritmo de busca simples que retorna um tupla com os arquivos.
        """
        if name in self.search_data:
            files = self.search_data[name]
            path_name = os.path.abspath('FriggAnswer')
            text_files = []
            if files is not None:
                for f in files:
                    text = open(path_name+'\\texts\\'+f[0]).read().decode('utf-8-sig')
                    opt_text = open(path_name+'\\texts2\\'+f[0]).read().decode('utf-8-sig').lower()
                    opt_text_data = GenSearchText().get_opt(opt_text)
                    #  tokenização
                    text_sent = sent_tokenize(text)
                    for i in f[1]:
                        element = (text_sent[i], opt_text_data[i]) #  modificado aqui
                        text_files.append(element)
            return set(text_files)
        else:
            return None

    def load_data(self):
        """
        função simples para carregar o arquivo
        """
        path = os.path.abspath('FriggAnswer')+'/pickle/'
        #path = os.path.abspath('pickle')+'\\'
        input_data = open(path + 'data.pkl')
        self.search_data = load(input_data)
        input_data.close()

class GenSearchText:
    """
    classe na qual gera os arquivos otimizados para a busca.
    """

    def get_opt(self, file_text):
        """
        Método que converte um txt em uma lista para o algorítmo de processamento
        """
        sentence = file_text.split('././')
        para = []
        for s in sentence:
            opt = []
            element = word_tokenize(s)
            for e in element:
                opt.append(tuple(e.split('/')))  #  mudei aqui
            if len(opt) != None:
                para.append(tuple(opt)) # mudei aqui também
        return tuple(para) # mudei aqui!

    def gen_synset(self, word):
        '''
        método gen_synset
        gera uma string com todos os nomes dos synsets gerados a partir de uma palavra
        depois da geração, todos os nomes dos synsets são concatenados e separados pelo char /
        '''
        syn1 = wn.synsets(u''+word[0], lang=u'por')
        syn_names = []
        for s in syn1:
            syn_names.append(s.name())
        str_name = '/'.join(syn_names)
        element = word[0]+'/'+word[1]+'/'+str_name
        return element

    def gen_opt(self, file_text):
        '''
        método que gera o novo texto.
        cada palavra é classificada e concatenada com o tipo através do caractere /
        depois, é concatenado com o retorno do synset.
        '''
        tagger = Tagger('portugues')
        tok = word_tokenize(file_text.read().decode('utf-8'))
        clas = tagger.classify(tok)
        p_text = []
        for c in clas:
            if c[1] == 'N' or re.match('ADJ',c[1]) or re.match('V',c[1]) or c[1] == '.':
                gen_set = self.gen_synset(c)
                p_text.append(gen_set)
        optimized_text = ' '.join(p_text)
        return optimized_text

def create_opt_texts():
    a,b = get_files()
    ge = GenSearchText()
    for f in a:
        text = ge.gen_opt(f)
        new_file = open(b[1]+'\\'+os.path.basename(f.name),'w')
        new_file.write(text.encode('utf-8'))
        new_file.close()

def create_bag(text):
    paragraph = sent_tokenize(text)
    word_list = []
    for p in paragraph:
        words = word_tokenize(p)
        word_list.append(words)
    return word_list

#  só para deixar claro que existe um vão aqui!
'''

a,b = get_files()
print a
se = SearchEngine()
se.insert(a)

se = SearchEngine()
a = se.search(u'ciência')
print len(a)
print a[0][0]
print '\n'
print a[0][1]
'''
