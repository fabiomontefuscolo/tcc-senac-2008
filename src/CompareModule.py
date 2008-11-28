# -*- coding: utf-8 -*-


from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *
import math

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
 
    def extrair_conteudo2(self,nomeArquivo):
        self.nomeArquivoTxt = nomeArquivo
        self.arquivo = open(self.nomeArquivoTxt,'r')
        desc = []
        artigo = ""
        #Ler conteudo
        for linha in self.arquivo:
            artigo =(artigo+" "+linha.strip())

        lista_descritores = open(r"../scielo/500_easy.txt",'r')
        #Ler Descritores
        leitura = "N" 
        for linha in lista_descritores:
            if(linha.__contains__("pid=")):
                if (nomeArquivo.__contains__(linha[0:len(linha)-1])):
                    leitura = "Y"
                else:
                    leitura = "N"
            if(leitura == "Y" and not linha.__contains__("pid=")):
                desc.append(linha.strip())
        
        lista_descritores.close()
        self.arquivo.close()
                 
        self.descritores_definidos = desc 
        self.artigo = artigo
        #self.descritores_definidos._   
      
 
 
    def precisao(self,dic,type):
        if type == "D":
            descritores = self.descritores_definidos
        elif type == "E":
            descritores = self.desc_existentes
            
        self.count = -1
        if (self.count == -1):
            self.count = 0
            for desc in dic.iterkeys():
            #print desc
                if descritores.__contains__(desc):
                    self.count = self.count + 1
        
        if(dic.__len__() == 0):
            return 0.0
        else:
            return (self.count)*1.0/(dic.__len__())*1.0    
 
    def cobertura(self,dic,type):
        if type == "D":
            descritores = self.descritores_definidos
        elif type == "E":
            descritores = self.desc_existentes
            
        if self.count == -1:
            self.count = 0
            for desc in dic.iterkeys():
            #print desc
                if descritores.__contains__(desc):
                    self.count = self.count + 1    
        
        if(dic.__len__() == 0):
            return 0.0
        else:
            return (self.count)*1.0/(descritores.__len__())*1.0
        #print count , " corretos de " , dic.__len__(), " encontrados"
        #print count , " corretos encontrados de " , self.descritores_definidos.__len__() , " definidos previamente"
        #print "Precisao = " , (count)*1.0/(dic.__len__())*1.0 , "%"
        #print "Cobertura = " , (count)*1.0/(self.descritores_definidos.__len__())*1.0 , "%"




    def descritores_existentes(self,conteudo,listaSino,janela):
        conteudo = self.filter_and_steam(conteudo) 
        descritores = {}
        listaDesc = {}
        stemmer = PorterStemmer()    
        #print "ddd" 
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
        diff = (len(self.desc_existentes) - len(descritores)) 
        self.desc_existentes = descritores
        return diff
        
def compare(article_qty,janela,tipos,scielo,ar,mh):
    #print "##Comparacao entre descritores obtidos pelo programa após um corte e analisando a arvore do Mesh com os descritores definidos previamente que realmente estão no texto ##"
    precisao = 0.0
    cobertura = 0.0
    total =0.0
    novos_tree = []
    novos = 0.0
    media = 0.0
    artigos_scielo = open(r"../scielo/arquivo.txt",'r')
    #artigos_scielo = open(r"../scielo/4casos.txt",'r')
    
    for i in artigos_scielo:
    #for i in range(1,article_qty+1):
        #print "Leitura do artigo ",total, "-> " , i
        #scielo.extrair_conteudo(r'../in/Artigo'+str(i)+'.txt')
        scielo.extrair_conteudo2(r'../scielo/articles_clean/'+i[0:len(i)-1]+'.txt')
        try:
            ar.set_conteudo(scielo.artigo)
            #novos = len(scielo.descritores_definidos)
            #media +=novos
            #novos_tree.append(novos)
            #print("setou")
            ar.preparar_conteudo()
            #print("preparou")
            if (tipos[4] == "S"):
                ar.useBigrama = "S"
            #print "ei"
            #print  mh.desc_dic,mh.sino_dic,janela
            ar.compare(mh.desc_dic,mh.sino_dic,janela)
            #print "comparou"
            texto = "Descritores Obtidos"
            if (tipos[0] == "S"):
                if (tipos[5] == "O"):
                    ar.filter_desc_ocorrencias()
                    #novos += len(ar.descritores)
                    #media +=novos
                    #novos_tree.append(novos)
                    #print "occorencias"
                if (tipos[5] == "Q"):
                    ar.filter_desc_quantidade()
                    #print "quantidade"
                texto += " com o corte"
            if (tipos[1] == "S"):
                #novos = ar.navigate_tree(mh.tree,mh.desc_dic)
                #novos_tree.append(novos)
                #media += novos
                
                #print "tree"
                texto += " com a navegacao na arvore"     
            if (tipos[3] == "S"):
                ar.navigate_tree(mh.tree,mh.desc_dic)
                if (tipos[5] == "O"):
                    ar.filter_desc_ocorrencias()
                if (tipos[5] == "Q"):
                    ar.filter_desc_quantidade()
            #print texto,":", ar.descritores
            
            if (tipos[2] == "S"):
                #print "S"            
                #scielo.descritores_existentes(scielo.artigo,mh.sino_dic,janela)
                novos = scielo.descritores_existentes(scielo.artigo,mh.sino_dic,janela)
                media +=novos
                novos_tree.append(novos)
                #print "cortou existentes"
                #print "Descritores Pre-definidos existentes no texto: ", scielo.desc_existentes
                #print len(scielo.desc_existentes) , "encontrados de " , len(scielo.descritores_definidos), "pre-definidos"
                precisao += scielo.precisao(ar.descritores,"E")
                #print "Precisao do artigo: ", scielo.precisao(ar.descritores,"E")
                cobertura += scielo.cobertura(ar.descritores,"E")
                #print "Cobertura do artigo: ", scielo.cobertura(ar.descritores,"E")
                
            else:
                #print "N"
                #print "Descritores Pre-definidos no texto: ", scielo.descritores_definidos 
                precisao += scielo.precisao(ar.descritores, "D")
                #print "Precisao do artigo: ", scielo.precisao(ar.descritores,"D")
                cobertura += scielo.cobertura(ar.descritores,"D")
                #print "Cobertura do artigo: ", scielo.cobertura(ar.descritores,"D")
            total += 1.0
            #print ""
            #raw_input()
        except:
             pass
             #print "Arquivo vazio"
    print "Artigos:",total
    print "Precisao;",precisao/total ,";Cobertura;",cobertura/total , ";F-measure;",(2.0*(precisao/total)*(cobertura/total) )/( (precisao/total) + (cobertura/total) )

    media = media*1.0 / total
    desvio = 0.0
    for n in novos_tree:
        desvio += pow((n - media),2)
    desvio = math.sqrt((1/(total-1))* desvio)
    print "Media: " , media , "// Desvio: " , desvio    


"""        
artigo = ArticleScielo()
artigo.extrair_conteudo(r'../in/Artigo2.txt')
print artigo.descritores_definidos
print artigo.artigo
print artigo.descritores_existentes(artigo.artigo)

"""
        #print "Descritores Pre-definidos: ",self.descritores_definidos
        #print "Descritores Obtidos: ", dic












