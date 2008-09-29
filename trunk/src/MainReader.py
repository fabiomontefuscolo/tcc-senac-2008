
# -*- coding: utf-8 -*-
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *
from MeshReader import MeshHandler
from ArticleReader import ArticleReader


#MESHREADER
# Criar um objeto Parser
parser = make_parser()

# Instancia do MeshHandler
mh = MeshHandler()

# Arquivo de saida para gravacao
#fp = open('/home/fabio/workspace/Indexador/ouput/resultado.txt','w')

# Porter Stemmer
ps = PorterStemmer()

# Filtro de Stop Words
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

print "Mesh carregado!!!"
#ARTICLEREADER

#Criar um nome ArticleReader
ar = ArticleReader()

#Carrega o Steammer
ar.set_stemmer(ps)

#Carregar Stop-Words
ar.set_word_filter(wf)


# Arquivo de Entrada
ar.set_file(r'..\in\Artigo1.txt')
ar.open_file()

sinonimo = {}
ar.prepar_conteudo()
ar.compare(mh.desc_dic,sinonimo)

print mh.desc_dic
print ar.descritores