import re
import io
from filelocs import gutenbergDir 
from filelocs import outputDir 

import dataProcessing as dp
import ioaux as ioaux

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)
separator = '@' # in word/number dictionary files

class WrdEntry:    
    """Just for frequency sorting."""
    def __init__(self,wrd,val):
        self.wrd= wrd
        self.val = val    
    def __lt__(self, other):
        if (self.val == other.val):
            return self.wrd < other.wrd
        return self.val > other.val  
    def asString(self):
        return self.wrd + separator + str(self.val)

def dv(dictionary,key):
    if key in dictionary:
        return dictionary[key]
    return 0

def updateDict(dictionary,key,val=1,lowercase=True):
    if lowercase:
        key = key.lower()
    if key in dictionary:
        dictionary[key] = dictionary[key] + val
    else:
        dictionary[key] = val
        
def storeDictFr(dictionary,file):
    """For storing dictionary, frequency sorted."""
    wLst = []
    for key in dictionary.keys():
        wLst.append(WrdEntry(key,dictionary[key]))
    wLst.sort()
    text_file = open(file, "w", encoding="utf8")
    for wrdEntry in wLst:
        text_file.write(wrdEntry.asString() + "\n")
    text_file.close() 
        
def storeDictAlpha(dictionary,file):
    """For storing dictionary, alphabetically sorted."""
    wLst = []
    for key in dictionary.keys():
        if re.match('.*[aeiou].*',key):
            wLst.append(key)
    wLst.sort()
    text_file = open(file, "w", encoding="utf8")
    for key in wLst:
        text_file.write(key + separator + str(dictionary[key]) + "\n")
    text_file.close()     
 
def loadDict(file): 
    """For loading dictionary from text file."""   
    wordDict = {}
    lineNr = 0
    with io.open(file,encoding="utf8") as infile:
        for line in infile:
            parts = line.strip().split(separator)
            if (len(parts) > 1):
                freq = int(parts[1])
                wordDict[parts[0]] = freq
            lineNr = lineNr + 1
    print("Loaded: " + file + " (" + str(lineNr) + " entries)")
    return wordDict
    
def fileLinesToList(file):
    fLst = []
    with open(file) as infile:
        for line in infile:
            fLst.append(line.strip())
    return fLst
        
def generateCorpusStatistics(step):
    authorsBooks = {}
    authorsToks = {}
    freqs = {}
    wLst = []
    for i in range(0,len(gutenbergFiles),step):
        auth = dp.authorFromFileName(gutenbergFiles[i])
        updateDict(authorsBooks,auth,lowercase=False)
        sents = dp.sentencesFromFile(gutenbergDir + gutenbergFiles[i])
        wc = 0
        for sent in sents:
            for t in sent:
                wc += 1
                updateDict(freqs,t,lowercase=True)
        updateDict(authorsToks,auth,val=wc,lowercase=False)
        wLst.append(str(i) + ':' + str(wc) + ':' + gutenbergFiles[i])
    storeDictFr(authorsBooks,outputDir+"authorsBooks.txt")
    storeDictFr(authorsToks,outputDir+"authorsToks.txt")
    storeDictFr(freqs,outputDir+"freqs.txt")
    text_file = open(outputDir+"wlist.txt", "w", encoding="utf8")
    for entry in wLst:
        text_file.write(entry + "\n")
    text_file.close() 


