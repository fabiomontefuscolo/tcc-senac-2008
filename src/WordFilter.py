class WordFilter:
    ''' Prove manipulacao de uma lista de stop words '''
    def __init__(self):
        self.stop_words = []
        
    def is_stopword(self,word):
        return (word in self.stop_words)
    
    def load_stopwords(self,file):
        file = open(file,'r')
        line = file.readline()
        while line:
            self.stop_words.append(line[0:-1])
            line = file.readline()