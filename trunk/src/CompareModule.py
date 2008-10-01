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
        self.artigo = ""
        #self.extrair_conteudo()
        
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
        count = 0
        print "Descritores Pre-definidos: ",self.descritores_definidos
        print "Descritores Obtidos: ", dic
        for desc in dic.iterkeys():
            #print desc
            if self.descritores_definidos.__contains__(desc):
                count = count + 1
        
        print count , " corretos de " , dic.__len__(), " encontrados"
        print count , " corretos encontrados de " , self.descritores_definidos.__len__() , " definidos previamente"
        print "Precisao = " , (count)*1.0/(dic.__len__())*1.0 , "%"
        print "Cobertura = " , (count)*1.0/(self.descritores_definidos.__len__())*1.0 , "%"
artigo = ArticleScielo()
artigo.extrair_conteudo(r'../in/Artigo2.txt')
#print artigo.descritores_definidos
#print artigo.artigo














