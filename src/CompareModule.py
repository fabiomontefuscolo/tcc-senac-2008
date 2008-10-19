# -*- coding: utf-8 -*-


from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *

class ArticleScielo():

    def _init_(self):
        self.nomeArquivoTxt = ""
        self.arquivo = NullFile()
        self.descritores_definidos = []
        self.desc_existentes = {}
        self.artigo = ""
        self.count = -1    

        #self.extrair_conteudo()
        
    def filter_and_steam(self,conteudo):
        stemmer = PorterStemmer()
        filter = WordFilter()
        filter.load_stopwords(r'../stopwords/english')
        word = ''
        output = ''
        for c in conteudo:
            if c.isalpha():
                word += c.lower()
            else:
                if word and not filter.is_stopword(word):
                    output += stemmer.stem(word, 0, len(word)-1 )
                    output += ' '
                word = ''
        return output
    
    def extrair_conteudo(self,nomeArquivo):
        self.nomeArquivoTxt = nomeArquivo
        self.arquivo = open(self.nomeArquivoTxt,'r')
        tipo = ""
        desc = []
        artigo = ""
        for linha in self.arquivo:
            #print linha.
            #raw_input()
           
            if linha.strip() == "Descritores":
                #print "Achou o descritor"
                tipo = "DESC"

            elif linha.strip() == "Artigo":
                tipo = "ART"
                #print "Achou o Artigo"
 
            else:
                if tipo == "DESC":
                    if linha.strip() != "":
                        desc.append(linha.strip())
                    #self.descritores_definidos.append(linha.strip())
                elif tipo == "ART":
                    artigo =(artigo+" "+linha.strip())
                        
        self.descritores_definidos = desc 
        self.artigo = artigo
        #self.descritores_definidos._   
            #self.descritores_definidos = descritores_definidos
 
 
    def precisao(self,dic):
        self.count = -1
        if (self.count == -1):
            self.count = 0
            for desc in dic.iterkeys():
            #print desc
                if self.descritores_definidos.__contains__(desc):
                    self.count = self.count + 1
        
        if(dic.__len__() == 0):
            return 0.0
        else:
            return (self.count)*1.0/(dic.__len__())*1.0    
 
    def cobertura(self,dic):
        if self.count == -1:
            self.count = 0
            for desc in dic.iterkeys():
            #print desc
                if self.descritores_definidos.__contains__(desc):
                    self.count = self.count + 1    
        
        if(dic.__len__() == 0):
            return 0.0
        else:
            return (self.count)*1.0/(self.descritores_definidos.__len__())*1.0
        #print count , " corretos de " , dic.__len__(), " encontrados"
        #print count , " corretos encontrados de " , self.descritores_definidos.__len__() , " definidos previamente"
        #print "Precisao = " , (count)*1.0/(dic.__len__())*1.0 , "%"
        #print "Cobertura = " , (count)*1.0/(self.descritores_definidos.__len__())*1.0 , "%"


    def descritores_existentes(self,conteudo,listaSino,janela):
        conteudo = self.filter_and_steam(conteudo) 
        descritores = {}
        listaDesc = {}
        stemmer = PorterStemmer()     
        for i in self.descritores_definidos:
            output = ""
            word = ''
            for c in (i + ' '):
                    if c.isalpha():
                        word += c.lower()
                    else:
                        if word:# and not self.filter.is_stopword(word):
                            output += stemmer.stem(word, 0, len(word)-1 )
                            output += ' '
                        word = ''
                        listaDesc[output.strip()] = i
        #print listaDesc
        #print conteudo
        conteudo = conteudo.split()
        for i in range(len(conteudo)):
            word = ""
            for j in range(janela):
                if (i+j) >= len(conteudo):
                    break
                word += conteudo[i+j]
                #print word
                if listaDesc.has_key(word):
                    if(descritores.__contains__(listaDesc[word])):
                        descritores[listaDesc[word]] += 1
                    else:
                        descritores[listaDesc[word]] = 1
                
                if listaSino.has_key(word) and listaDesc.has_key(listaSino[word]):
                    if(descritores.__contains__(listaDesc[listaSino[word]])):
                        descritores[listaDesc[listaSino[word]]] += 1
                    else:
                        descritores[listaDesc[listaSino[word]]] = 1        
                
                word += " "
        
        self.desc_existentes = descritores
"""        
artigo = ArticleScielo()
artigo.extrair_conteudo(r'../in/Artigo2.txt')
print artigo.descritores_definidos
print artigo.artigo
print artigo.descritores_existentes(artigo.artigo)

"""
        #print "Descritores Pre-definidos: ",self.descritores_definidos
        #print "Descritores Obtidos: ", dic












