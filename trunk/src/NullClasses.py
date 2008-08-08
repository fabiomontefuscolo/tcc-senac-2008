class NullFile:
    def __init__(self):
        pass

    def write(self,str):
        print str,

class NullStemmer:
    def __init__(self):
        pass

    def stem(self, word, start, end):
        return word
    
class NullWordFilter:
    def __init__(self):
        pass
    
    def is_stopword(self,word):
        return False