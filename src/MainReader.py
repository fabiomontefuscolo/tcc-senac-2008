
# -*- coding: utf-8 -*-
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from string import strip
from Stemmer import PorterStemmer
from WordFilter import WordFilter
from NullClasses import *
from MeshReader import MeshHandler
from ArticleReader import ArticleReader
from CompareModule import ArticleScielo


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
#parser.parse(r'../mesh/desc2008.xml')

#Carregar Dicionarios serializados
mh.restore(mh.desc_dic,open(r'../mesh/desc_dic'))
mh.restore(mh.sino_dic,open(r'../mesh/sino_dic'))
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
#ar.set_file(r'..\in\Artigo1.txt')
#ar.open_file()

sinonimo = {}
desc2 = {u'Radiology': 2, u'Early Diagnosis': 1, u'Research': 2, u'Cyclins': 2, u'Cell Cycle': 2, u'Deoxycytidine': 1, u'Mortality': 2, u'Pyrenes': 1, u'Globins': 2, u'Chromatin': 1, u'Aggression': 1, u'Incidence': 1, u'Emergencies': 1, u'Goals': 1, u'Molecular Weight': 1, u'Organizations': 1, u'MEDLINE': 22, u'Paraffin Embedding': 4, u'Heart': 1, u'Cells': 15, u'Phosphorylation': 1, u'Air': 1, u'Mechanics': 2, u'Forms': 1, u'Metaplasia': 1, u'England': 1, u'Methods': 3, u'Exons': 1, u'Comparative Study': 1, u'Nucleic Acids': 1, u'Preventive Medicine': 1, u'Classification': 1, u'Role': 2, u'Pathology': 3, u'Population': 2, u'Hospitals': 4, u'Risk Factors': 1, u'Buffers': 2, u'Genomics': 7, u'Statistics': 8, u'Retinoblastoma': 2, u'Sodium': 2, u'Sports': 1, u'International Agencies': 1, u'Archives': 2, u'Amplifiers': 3, u'Life': 2, u'World Health Organization': 1, u'Chromosomes': 2, u'Risk': 6, u'Particulate Matter': 1, u'Men': 2, u'Genes, Reporter': 1, u'Water': 1, u'Xylenes': 1, u'Sodium Hydroxide': 1, u'Carcinoma': 14, u'Histology': 6, u'Gels': 1, u'Observation': 5, u'Work': 1, u'Heating': 1, u'Finches': 1, u'Patients': 7, u'Habits': 11, u'Digestion': 2, u'Oncogenes': 4, u'Nitrates': 1, u'Pleura': 1, u'RNA': 1, u'Metals': 1, u'Estrogens': 1, u'DNA Methylation': 3, u'Gallbladder': 1, u'Viruses': 1, u'Cyclin-Dependent Kinase 6': 1, u'14-3-3 Proteins': 4, u'Japan': 3, u'Technology': 3, u'Mercaptoethanol': 1, u'Universities': 2, u'Centrifugation': 2, u'Death': 1, u'Genetics': 5, u'Temperature': 1, u'Humanities': 4, u'Epithelium': 1, u'Periodicals': 2, u'Snow': 1, u'Education': 1, u'Mutation': 1, u'Phenol': 1, u'Medicine': 1, u'Histidine': 1, u'Beryllium': 1, u'Formates': 1, u'Chloroform': 1, u'Epidemiology': 4, u'Incubators': 2, u'Adult': 1, u'Chile': 23, u'Paraffin': 4, u'Schools': 2, u'Smoking': 18, u'Cities': 1, u'Precipitation': 1, u'Association': 5, u'Women': 2, u'DNA': 22, u'Carbonates': 1, u'Sputum': 6, u'Science': 4, u'Instruction': 1, u'Suggestion': 3, u'Abstracts': 1, u'Carcinogens': 7, u'Hydroxides': 1, u'Health': 1, u'Tables': 8, u'Tissues': 5, u'Culture': 1, u'Lung': 37, u'Gene Silencing': 2, u'Ink': 4, u'Schools, Medical': 2, u'Mutagens': 2, u'Serum': 3, u'Fixatives': 2, u'Aging': 3, u'World Health': 1, u'Therapeutics': 1, u'Prognosis': 2, u'Cats': 2, u'Adenocarcinoma': 4, u'Inhalation': 4, u'Tobacco': 2, u'Survival': 1, u'Genes': 29, u'Biopsy': 1, u'Adonis': 7, u'Ethanol': 2, u'Silver': 1, u'Solutions': 1, u'Cytology': 2, u'Methylation': 70, u'Enzymes': 2, u'CpG Islands': 7, u'Cadherins': 1, u'Acids': 2, u'Disease': 3, u'Diagnosis': 1, u'Hydrocarbons': 3, u'Methyltransferases': 3, u'Thorax': 2, u'Rats': 1, u'Silver Nitrate': 1, u'Prevalence': 5, u'Environmental Pollution': 1, u'Individuation': 1, u'Retinoblastoma Protein': 1, u'Gold': 1, u'Collections': 1}

#ar.prepar_conteudo()
#ar.compare(mh.desc_dic,mh.sino_dic)
scielo = ArticleScielo()
precisao = 0.0
cobertura = 0.0
total =0.0

for i in range(1,51):
    print "Leitura do artigo ",i
    #nome = "./in/Artigo"+str(i)+".txt"
    scielo.extrair_conteudo(r'../in/Artigo'+str(i)+'.txt')
    ar.set_conteudo(scielo.artigo)
    ar.prepar_conteudo()
    #ar.set_desc(desc)
    ar.compare(mh.desc_dic,mh.sino_dic,3)
    #ar.descritores = desc2
    ar.filter_desc()
    print "Descritores Pre-definidos: ",scielo.descritores_definidos
    print "Descritores Obtidos: ", ar.descritores
    print "Descritores Pre-definidos existentes no texto: ", scielo.descritores_existentes(scielo.artigo)
    print len(scielo.descritores_existentes(scielo.artigo)) , " de " , len(scielo.descritores_definidos)
    precisao += scielo.precisao(ar.descritores)
    print "Precisao do artigo: ", scielo.precisao(ar.descritores)
    cobertura += scielo.cobertura(ar.descritores)
    print "Cobertura do artigo: ", scielo.cobertura(ar.descritores)
    total=i
    print ""
    #raw_input()

print "\nPrecisao geral do programa para",total,"documentos:",precisao/total
print "\nCobertura geral do programa para",total,"documentos:",cobertura/total

#mh.serialize(mh.desc_dic, open(r'../mesh/desc_dic','w'))
#mh.serialize(mh.sino_dic, open(r'../mesh/sino_dic','w'))


#print mh.desc_dic
#print ar.descritores