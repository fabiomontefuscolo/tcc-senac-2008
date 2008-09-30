# -*- coding: utf-8 -*-

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
		elif name == 'Term':
			pass
		elif name == 'ConceptList':
			pass
		elif name == 'ConceptName':
			pass
		elif name == 'ScopeNote':
			pass

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
			self.descritor = output
			#raw_input(self.data + ": " + output)
			#self.file.write("Descriptor %d: %s\n" % (self.contador, self.data))
			
		elif name == 'ScopeNote':
			pass
			
		elif name == 'Term':
			if self.data != "":
				self.sino_dic[self.data] = self.descritor
				#raw_input(self.data + ": " + self.descritor)
			
		elif name == 'DescriptorRecord':
			#self.file.write("\n")
			pass

		if name != 'String':
			self.data = ""

		self.nivel -= 1

	def characters(self, content):
		self.data += strip(content)
"""		
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
"""
#print mh.desc_dic