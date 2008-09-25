# -*- coding: utf-8 -*-


from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *


class ArticleReader():
    def __init__(self):
        self.nomeArquivo = ""
        self.conteudo = ""
        self.descritores = {}
        self.arquivo = NullFile()
        self.stemmer = NullStemmer()
        self.filter = NullWordFilter()
    def set_file(self,string):
        self.nomeArquivo = string
    def open_file(self):
        self.arquivo = open(self.nomeArquivo,'r')
    def set_stemmer(self, stemmer):
        self.stemmer = stemmer     
    def set_word_filter(self, filter):
        self.filter = filter
    def filter_and_steam(self):
        self.conteudo = self.arquivo.read()
        word = ''
        output = ''
        for c in self.conteudo:
            if c.isalpha():
                word += c.lower()
            else:
                if word and not self.filter.is_stopword(word):
                    output += self.stemmer.stem(word, 0, len(word)-1 )
                    output += ' '
                word = ''
        self.conteudo = output
 
    def prepar_conteudo(self):
        self.filter_and_steam()    
        self.conteudo = self.conteudo.split()
    def compare(self,listaDesc , listaSin):
        for i in range(len(self.conteudo)):

            #Uma Palavra
            print self.conteudo[i]+'\n'
            #Descritores
            if listaDesc.has_key(self.conteudo[i]):
                if(self.descritores.__contains__(listaDesc[self.conteudo[i]])):
                    self.descritores[listaDesc[self.conteudo[i]]] += 1
                else:
                    self.descritores[listaDesc[self.conteudo[i]]] = 1
                            
             #sinoniomos       
            if listaSin.has_key(self.conteudo[i]):
                if(self.descritores.__contains__(listaDesc[listaSin[self.conteudo[i]]])):
                    self.descritores[listaDesc[listaSin[self.conteudo[i]]]] += 1
                else:
                    self.descritores[listaDesc[listaSin[self.conteudo[i]]]] = 1
 
 
 
 
 
            #listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]]
            #Duas Palavras
            if i+1 < len(self.conteudo):
                print self.conteudo[i]+' '+self.conteudo[i+1]+'\n'
                #Descritores
                if listaDesc.has_key(self.conteudo[i]+' '+self.conteudo[i+1]):
                    if(self.descritores.__contains__(listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]])):
                        self.descritores[listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]]] += 1
                    else:
                        self.descritores[listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]]] = 1          
   
                #sinonimos
                if listaSin.has_key(self.conteudo[i]+' '+self.conteudo[i+1]):
                    if(self.descritores.__contains__(listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]]])):
                        self.descritores[listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]]]] += 1
                    else:
                        self.descritores[listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]]]] = 1  
   
   
   
   
                        
            #listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]
            #Tres Palavras      
            if i+2 < len(self.conteudo):
                print self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]+'\n'
                #Descritores
                if listaDesc.has_key(self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]):
                    if(self.descritores.__contains__(listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]])):
                        self.descritores[listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]] += 1
                    else:
                        self.descritores[listaDesc[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]] = 1
 
 
 
                #sinonimos
                if listaSin.has_key(self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]):
                    if(self.descritores.__contains__(listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]])):
                        self.descritores[listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]]] += 1
                    else:
                        self.descritores[listaDesc[listaSin[self.conteudo[i]+' '+self.conteudo[i+1]+' '+self.conteudo[i+2]]]] = 1
 
 
        
           

descritores = {'HIV': 'HIV Full String' ,
               'nitric' : 'Nitric full',
               'nitric oxid' : 'Nitric oxide full',
               'cell' : 'cell Full String' ,
               'acid' : 'acid Full String'         
            }
sinonimos = {'Acquired Immune Deficiency Syndrome Virus' : 'nitric oxid' ,
             'ablat' : 'nitric oxid' ,
             'AIDS Virus' : 'HIV' ,
             'HTLV-III' :  'HIV' , 
             'Human Immunodeficiency Virus' :  'HIV' }


#Criar um nome ArticleReader
ar = ArticleReader()

#Carrega o Steammer
stemmer = PorterStemmer()
ar.set_stemmer(stemmer)

#Carregar Stop-Words
wf = WordFilter()
wf.load_stopwords(r'..\stopwords\english')
ar.set_word_filter(wf)


# Arquivo de Entrada
ar.set_file(r'..\in\Entrada.txt')
ar.open_file()

ar.prepar_conteudo()
ar.compare(descritores,sinonimos)

print descritores
print ar.descritores

















