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
        self.useBigrama = "N"
    def set_conteudo(self,string):
        self.conteudo = string
    def set_desc(self,desc):
        self.descritores = desc
    def set_file(self,string):
        self.nomeArquivo = string
    def open_file(self):
        self.arquivo = open(self.nomeArquivo,'r')
    def set_stemmer(self, stemmer):
        self.stemmer = stemmer     
    def set_word_filter(self, filter):
        self.filter = filter
    def filter_and_steam(self):
        if self.conteudo == "":
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
        
    def compare(self,listaDesc,listaSin,janela):
        self.descritores = {}
        for i in range(len(self.conteudo)):
            word = ""
            for j in range(janela):
                if (i+j) >= len(self.conteudo):
                    break
                word += self.conteudo[i+j]
                #print word
                
                if listaDesc.has_key(word):
                    if(self.descritores.__contains__(listaDesc[word])):
                        self.descritores[listaDesc[word]] += 1
                    else:
                        self.descritores[listaDesc[word]] = 1
                        
                if listaSin.has_key(word):
                    if(self.descritores.__contains__(listaDesc[listaSin[word]])):
                        self.descritores[listaDesc[listaSin[word]]] += 1
                    else:
                        self.descritores[listaDesc[listaSin[word]]] = 1
                
                word += " "
            #print "##Bigramas"
            if(self.useBigrama == "S"):
                self.bigrama(listaDesc, listaSin, janela, word, i)
            #print "##"
            #raw_input()
        #print self.descritores           
    
    def bigrama(self,listaDesc,listaSin,janela,palavra,i):
        if(i > 0 and len(palavra) > 2):
            palavras = palavra.split()
            for l in range(1,len(palavras)):
                bigrama = self.conteudo[i-1] + " " + palavras[l]
                if listaDesc.has_key(bigrama):
                    if(self.descritores.__contains__(listaDesc[bigrama])):
                        self.descritores[listaDesc[bigrama]] += 1
                    else:
                        self.descritores[listaDesc[bigrama]] = 1
                        
                if listaSin.has_key(bigrama):
                    if(self.descritores.__contains__(listaDesc[listaSin[bigrama]])):
                        self.descritores[listaDesc[listaSin[bigrama]]] += 1
                    else:
                        self.descritores[listaDesc[listaSin[bigrama]]] = 1
                #print bigrama
            

 
    def filter_desc_ocorrencias(self):
        if(self.descritores.__len__() > 0):
            self.descritores = sorted(self.descritores.items(),lambda x, y: cmp(x[1], y[1]), reverse=True)
            #print self.descritores.__getitem__(0)
            #print self.descritores.__getitem__(0)[1] / 5
            #print self.descritores.__len__()
            #print self.descritores.__getitem__(self.descritores.__len__()/2)[1]
            #qty = (self.descritores.__getitem__(0)[1] *10) / (self.descritores.__len__())
            #print qty
            limite = self.descritores.__getitem__(0)[1] / 5
            
            newdesc ={}
            for i in self.descritores:
                
                if i[1] >=limite:
                    newdesc[i[0]] = i[1]
            #self.descritores.
            self.descritores = newdesc
            #print self.descritores

    def filter_desc_quantidade(self):
        #print "Filtro por quantidade"
        if(self.descritores.__len__() > 0):
            #print "Tamanho: ", self.descritores.__len__()
            self.descritores = sorted(self.descritores.items(),lambda x, y: cmp(x[1], y[1]), reverse=True)
            limite = self.descritores.__len__() / 10
            #print "Limite: ", limite
            newdesc ={}
            for i in range(0,limite):
                    #print "Descritor: ",i , self.descritores[i][0] , self.descritores[i][1]
                    newdesc[self.descritores[i][0]] = self.descritores[i][1]
            #print "Terminou loop"
            self.descritores = newdesc
            #print "Atribuiu os descritores"

    def navigate_tree(self,tree,desc_dic):
        descritores_pais = {}
        for i in tree.items():
            #print i
            #if i[1]== "exercis" or i[1] == "yoga" or i[1] == "relax":
            if self.descritores.has_key(desc_dic[i[1]]):
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
        #print raiz
        novos_descritores = {}
        for r in descritores_pais.items():
            if r[0].__contains__(raiz):
                novos_descritores[r[0]] = r[1]
        #print novos_descritores
        
        contabilizar_filhos = {}
        for c in novos_descritores.iterkeys():
            contabilizar_filhos[c] = 0
        
        #print contabilizar_filhos
        for tudo in tree.iterkeys():
            for m in novos_descritores.iterkeys():
                if tudo.__contains__(m) and (len(tudo) == len(m)+4):
                    contabilizar_filhos[m] += 1
                    
        #print contabilizar_filhos
        #descritores_sugeridos = {}
        for l in novos_descritores.iteritems():
            if (l[1]*1.0 / contabilizar_filhos[l[0]]*1.0 ) > 0.2:
                self.descritores[desc_dic[tree[l[0]]] ] = l[1]
        #print descritores_sugeridos

           

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
ar.useBigrama = "S"
ar.prepar_conteudo()
ar.compare(descritores,sinonimos,3)

#print descritores
#print ar.descritores

















