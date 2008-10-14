# -*- coding: utf-8 -*-

import pickle
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *


class MeshHandler(ContentHandler):
    def __init__(self):
        self.contador = 0
        self.nivel = 0
        self.elemento = ""
        self.data = ""
        self.file = NullFile()
        self.stemmer = NullStemmer()
        self.filter = NullWordFilter()
        self.desc_dic = {}
        self.sino_dic = {}
        self.descritor = ""
        self.sinonimo = ""
        self.preferido = ""
        self.ConceptPreferredTermYN = ''
        self.tree = {}

    def set_output(self, fp):
        self.file = fp

    def set_stemmer(self, stemmer):
        self.stemmer = stemmer
        
    def set_word_filter(self, filter):
        self.filter = filter

    def startElement(self, name, attrs):
        self.nivel += 1
        if name != 'String':
            self.elemento = name

        if name == 'DescriptorRecordSet':
            pass
        elif name == 'DescriptorRecord':
            self.contador += 1
            self.desc = ""
            self.sino = ""
        elif name == 'DescriptorUI':
            pass
        elif name == 'DescriptorName':
            pass
        elif name == 'TreeNumberList':
            pass
        elif name == 'TermList':
            pass
        elif name == 'Term': # Verificar se o atributo termprefered ￩ N, se sim, self.ConceptPreferredTermYN = 'N'
            self.ConceptPreferredTermYN = attrs.getValue("ConceptPreferredTermYN")
            pass
        elif name == 'ConceptList':
            pass
        elif name == 'ConceptName':
            pass
        elif name == 'ScopeNote':
            pass
        elif name == 'TreeNumber':
            pass
            #self.tree = {}

    def endElement(self, name):
        if name == 'DescriptorName' and self.nivel == 3:
            word = ''
            output = ''
            
            for c in (self.data + ' '):
                if c.isalpha():
                    word += c.lower()
                else:
                    if word:# and not self.filter.is_stopword(word):
                        output += self.stemmer.stem(word, 0, len(word)-1 )
                        output += ' '
                    word = ''
            self.desc_dic[output.strip()] = self.data
            self.descritor = output.strip()
            #raw_input(self.data + ": " + output)
            #self.file.write("Descriptor %d: %s\n" % (self.contador, self.data))
            
        elif name == 'ScopeNote':
            pass
            
        elif name == 'Term':
            if self.data != "" and self.ConceptPreferredTermYN == 'N':
                word = ''
                output = ''
                for c in (self.data + ' '):
                    if c.isalpha():
                        word += c.lower()
                    elif c.isalnum():
                        word += c
                    else:
                        if word:# and not self.filter.is_stopword(word):
                            output += self.stemmer.stem(word, 0, len(word)-1 )
                            output += ' '
                        word = ''
                self.sino_dic[output.strip()] = self.descritor
                #raw_input(self.data + "=" + output.strip() + ": " + self.descritor)
            self.ConceptPreferredTermYN = ''
        elif name == 'DescriptorRecord':
            #self.file.write("\n")
            pass
        elif name == 'TreeNumber':
            self.tree[self.descritor] = self.data
            #print self.tree
            #raw_input("1 ")
            #if len(self.tree) > 1:
            #    print self.tree
            #    raw_input("Tem 2: ")

        if name != 'String':
            self.data = ""

        self.nivel -= 1
       
    def characters(self, content):
        self.data += strip(content)
    
    def serialize(self, dic,file):
        pickle.dump(dic, file)
        
    
    def restore(self, dic,file,type):
        if type == "DESC":
            self.desc_dic = pickle.load(file)
        elif type == "SINO":
            self.sino_dic = pickle.load(file)
        #print dic
    def mesh_tree(self):
        return true 
        
# Criar um objeto Parser
parser = make_parser()

# Instancia do MeshHandler

mh = MeshHandler()

# Arquivo de saida para gravacao
#fp = open('/home/fabio/workspace/Indexador/ouput/resultado.txt','w')

# Porter Stemmer
ps = PorterStemmer()

# Filtro de Stop Word
wf = WordFilter()
wf.load_stopwords(r'../stopwords/english')

# Passa pointer do arquivo para o handler
#mh.set_output(fp)

# Vamos ver se o stemmer funciona
mh.set_stemmer(ps)


# Filtrar StopWords e lento
mh.set_word_filter(wf)

# Faz o Parser usar o MeshHandler
parser.setContentHandler(mh)

# Arquivo XML
parser.parse(r'../mesh/desc2008.xml')
#print mh.desc_dic
#pickle.dump(mh.desc_dic,open(r'../mesh/desc_dic','w'))
#pickle.dump(mh.sino_dic,open(r'../mesh/sino_dic','w'))
#pickle.dump(mh.tree,open(r'../mesh/tree','w'))
#print mh.desc_dic
