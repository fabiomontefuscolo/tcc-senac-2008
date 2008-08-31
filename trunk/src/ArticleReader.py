# -*- coding: utf-8 -*-

#tel = {'jack': 4098, 'sape': 4139}

from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *

#descritores = {'HIV': }

sinonimos = {'Acquired Immune Deficiency Syndrome Virus' : 'HIV' ,
             'Acquired Immunodeficiency Syndrome Virus' : 'HIV' ,
             'AIDS Virus' : 'HIV' ,
             'HTLV-III' :  'HIV' , 
             'Human Immunodeficiency Virus' :  'HIV' }



stemmer = PorterStemmer()
filter = NullWordFilter()


#Carregar Stop-Words
wf = WordFilter()
wf.load_stopwords(r'..\stopwords\english')
filter = wf


# Arquivo de Entrada
fp = open(r'..\..\in\Entrada.txt','r')
conteudo = fp.read()

word = ''
output=''
for c in conteudo:
    if c.isalpha():
        word += c.lower()
    else:
        if word and not filter.is_stopword(word):
            output += stemmer.stem(word, 0, len(word)-1 )
            output += ' '
        word = ''
        
print output        


