# -*- coding: utf-8 -*-


from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *

class ArticleScielo():
    def _init_(self,nomeArquivoTxt):
        
        self.nomeArquivoTxt = ""
        self.arquivo = NullFile()
        self.descritores_definidos = ""
        self.artigo = ""
        #self.extrair_conteudo()
        
    def extrair_conteudo(self,nomeArquivo):
        self.nomeArquivoTxt = nomeArquivo
        self.arquivo = open(self.nomeArquivoTxt,'r')
        for linha in self.arquivo.readLine():
            if linha == "Descritores":
                linha = self.arquivo.readLine()
                while (linha != "Artigo"):
                    self.descritores_definidos.__add__(linha)
                    linha = self.arquivo.readLine()
            if linha == "Artigo":
                self.artigo = self.arquivo.read()

    
artigo = ArticleScielo()
artigo.extrair_conteudo(r'../in/Artigo2.txt')
print artigo.descritores_definidos
print artigo.arquivo














