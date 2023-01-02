import re
import ioaux as ioaux
from filelocs import gutenbergDir 

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)
    
replacements = [('...', ' '),('_', ' '),
                ("n't", ' not'),("I'm", 'I am'),
                ("e're", 'e are'),("ou're", 'ou are'),
                ("hey're", 'hey are'),(" it's", ' it is'),
                (" he's", ' he is'),(" she's", ' she is'),
                ("That's", 'That is'),("that's", 'that is'),
                ("It's", 'It is'),("He's", 'He is'),
                ("here's", 'here is'),
                ("'ll", ' will'),("'ve", ' have'),
                ("She's", 'She is'),('Mr.', 'Mr'),('Mrs.', 'Mrs'),
                ('St.', 'St'),('Dr.', 'Dr')]     
        
def tokenizeLine(line):
    l = line.replace('\n', '')
    for r in replacements:
        l = l.replace(*r)
    #l = extractQuotation(l)
    l = re.sub(r'([ABCDEFGHJKLMNOPQRSTUVXYZ])\.','\\1',l) # removes full stop in initals
    tokens = re.findall(r'\w[\w\-\']*|\d+|[.,!?:]|--',l) 
    return tokens

def normalText(line):
    if not re.match('.*[a-z].*$',line):
        return False
    if re.match('^[\d ]*$',line):
        return False
    if re.match(r'^\[.*',line):
        return False
    return True

def tokensFromFile(file,rememberParagraphs):
    tokens = []
    with open(file,'r',encoding="utf8") as myfile:    
        lines=myfile.readlines()
        for line in lines:
            if normalText(line):
                tokensL = tokenizeLine(line)
                for tok in tokensL:
                    tokens.append(tok)
            elif rememberParagraphs:
                tokens.append('<P>')
    return tokens

def cap(t):
    return re.match('[A-Z].*',t)

def sentencesFromTokens(t,beg,end):
    sents = [[]]
    for i in range(beg,end):
        if t[i] == '<P>' and len(sents[-1]) > 0:
            sents.append([]) 
        elif t[i] == '<P>':
            pass
        elif cap(t[i]) and len(sents[-1]) and re.match('[.!?:]',sents[-1][-1]):
            sents.append([t[i]])
        else: 
            sents[-1].append(t[i])
    if sents[-1] == []:
        sents = sents[0:-1]
    return sents

def sentencesFromFile(file):
    tokens = tokensFromFile(file,True)
    return sentencesFromTokens(tokens,0,len(tokens))

def authorFromFileName(f):   
    ff = f.split('__',1)
    return ff[0]    
              
class SelAuthor: 
    """For selecting all corpus files by authors in a given list."""
    def __init__(self,authlist,fileStep):
        self.authlist= authlist
        self.fileStep = fileStep
        
    def sel(self,file): 
        return authorFromFileName(file) in self.authlist
    
class SelAuthorCompl: 
    """For selecting corpus files by all authors not members of a given list."""
    def __init__(self,authlist,fileStep):
        self.authlist = authlist
        self.fileStep = fileStep
        
    def sel(self,file): 
        return not authorFromFileName(file) in self.authlist

