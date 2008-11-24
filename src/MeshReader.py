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
        self.PreferredConceptYN = ''
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
        elif name == 'Concept':
            self.PreferredConceptYN = attrs.getValue("PreferredConceptYN")
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
            if(self.ConceptPreferredTermYN == 'N' or self.PreferredConceptYN == 'N'):
                if self.data != "" :
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
            #else:
                #print self.PreferredConceptYN , self.ConceptPreferredTermYN
            self.ConceptPreferredTermYN = ''
        elif name == 'Concept':
            self.PreferredConceptYN = ''
        
        elif name == 'DescriptorRecord':
            #self.file.write("\n")
            pass
        elif name == 'TreeNumber':
            self.tree[self.data] = self.descritor
            #print self.tree
            #raw_input("1 ")
            #if self.desc_dic[self.descritor] == "Exercise":
            #    print self.tree[self.descritor]
                
            #    raw_input("Tem 2: ")

        if name != 'String':
            self.data = ""

        self.nivel -= 1
       
    def characters(self, content):
        self.data += strip(content)
    
    def serialize(self, dic,file):
        pickle.dump(dic, file)
        
    
    def restore(self, file,type):
        #dic = pickle.load(file)
        if type == "DESC":
            self.desc_dic = pickle.load(file)
        elif type == "SINO":
            self.sino_dic = pickle.load(file)
        elif type == "TREE":
            self.tree = pickle.load(file) 
        #print dic
 
"""        
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
#parser.parse(r'../mesh/desc2008.xml')
#print mh.desc_dic
#pickle.dump(mh.desc_dic,open(r'../mesh/desc_dic','w'))
#pickle.dump(mh.sino_dic,open(r'../mesh/sino_dic','w'))
#pickle.dump(mh.tree,open(r'../mesh/tree','w'))
#print mh.desc_dic
mh.restore(open(r'../mesh/desc_dic'),"DESC")
mh.restore(open(r'../mesh/tree'), "TREE")

#3print mh.desc_dic.get(mh.desc_dic. )
print mh.desc_dic.get("yoga")
print mh.desc_dic.get("relax")
print mh.desc_dic.get("exercis")#mh.desc_dic.get("Exercise")
#mh.tree.items()
#print mh.tree
descritores_pais = {}
for i in mh.tree.items():
    #print i
    if i[1]== "exercis" or i[1] == "yoga" or i[1] == "relax":
        #print i
        pai = ""
        for j in i[0]:
            if j == ".":
                if descritores_pais.has_key(pai):
                    descritores_pais[pai] += 1
                else:
                    descritores_pais[pai] = 1
                #print "Pai" ,pai , mh.tree.get(pai)
            pai += j
max = 0
raiz = ""
for r in descritores_pais.items():
    if len(r[0]) == 3:
        #print r[0]
        if r[1] > max:
            max = r[1]
            raiz = r[0]
print raiz
novos_descritores = {}
for r in descritores_pais.items():
    if r[0].__contains__(raiz):
        novos_descritores[r[0]] = r[1]
print novos_descritores

contabilizar_filhos = {}
for c in novos_descritores.iterkeys():
    contabilizar_filhos[c] = 0

print contabilizar_filhos
for tudo in mh.tree.iterkeys():
    for m in novos_descritores.iterkeys():
        if tudo.__contains__(m) and (len(tudo) == len(m)+4):
            contabilizar_filhos[m] += 1
            
print contabilizar_filhos
descritores_sugeridos = {}
for l in novos_descritores.iteritems():
    if (l[1]*1.0 / contabilizar_filhos[l[0]]*1.0 ) > 0.2:
        descritores_sugeridos[mh.desc_dic[mh.tree[l[0]]] ] = l[1]
print descritores_sugeridos
"""
#print descritores_pais
#print mh.tree.get("exercis")
#print mh.tree.__getitem__("I03.350")
#mh.tree.iteritems()

