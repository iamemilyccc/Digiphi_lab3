from scipy.stats import chisquare
from dictionaryStuff import updateDict
from dictionaryStuff import storeDictFr
import ioaux
import dataProcessing as dp
from filelocs import gutenbergDir 
from filelocs import outputDir 

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)

def listOverlap(l1,l2):
    for e in l1:
        if e in l2:
            return True
    return False

def authDict(authlist):
    """Create dictionary for (all books by) author.""" 
    dictAuth = {}
    for i in range(0,len(gutenbergFiles),1):
        auth = dp.authorFromFileName(gutenbergFiles[i])
        if auth in authlist:
            tokens = dp.tokensFromFile(gutenbergDir + gutenbergFiles[i],False)
            for t in tokens:
                updateDict(dictAuth,t)
            dictAuth['*ALL*'] = len(tokens)
            print(gutenbergFiles[i])
    return dictAuth

def contextDict(authors,terms):
    """Creates dictionary for sentences by authors containing any of given terms.
    and one dictionary for the other sentences by the same authors.
    """ 
    dictInC = {}
    dictOutC = {}
    for i in range(0,len(gutenbergFiles),1):
        auth = dp.authorFromFileName(gutenbergFiles[i])
        if authors == 'ALL' or auth in authors:
            sents = dp.sentencesFromFile(gutenbergDir + gutenbergFiles[i])
            for sent in sents:
                lowercase(sent)
                if listOverlap(sent,terms):
                    for w in sent:
                        if not w in terms:
                            updateDict(dictInC,w)
                            updateDict(dictInC,'*ALL*',lowercase=False)
                else:
                    for w in sent:
                        updateDict(dictOutC,w)
                        updateDict(dictOutC,'*ALL*',lowercase=False)
            print(gutenbergFiles[i])
    return (dictInC,dictOutC)

def twoContextsDict(authors,terms1,terms2):
    """Creates dictionary for sentences by authors containing any of given terms1.
    and one dictionary for sentences by authors containing any of given terms2.
    """ 
    dictInC1 = {}
    dictInC2 = {}
    for i in range(0,len(gutenbergFiles),1):
        auth = dp.authorFromFileName(gutenbergFiles[i])
        if authors == 'ALL' or auth in authors:
            sents = dp.sentencesFromFile(gutenbergDir + gutenbergFiles[i])
            for sent in sents:
                lowercase(sent)
                if listOverlap(sent,terms1):
                    for w in sent:
                        if not w in terms1:
                            updateDict(dictInC1,w)
                            updateDict(dictInC1,'*ALL*',lowercase=False)
                elif listOverlap(sent,terms2):
                    for w in sent:
                        if not w in terms2:
                            updateDict(dictInC2,w)
                            updateDict(dictInC2,'*ALL*',lowercase=False)
            print(gutenbergFiles[i])
    return (dictInC1,dictInC2)

def lowercase(sentence):
    for i in range(len(sentence)):
        sentence[i] = sentence[i].lower()

def mkChi2CompDict(dct1,dct2,file):
    nTot = dct1['*ALL*'] + dct2['*ALL*']
    chi2dict = {}
    for wrd in dct1.keys():
        if (dct1[wrd] > 5 and wrd in dct2 and 
            dct2[wrd] > 5 and not wrd == '*ALL*' and
            # overrepresented in dct1
            dct1[wrd]/dct1['*ALL*'] > dct2[wrd]/dct2['*ALL*']):
            nWrd = dct1[wrd] + dct2[wrd]
            # expected contingency table at independence
            exp0 = nWrd*dct1['*ALL*']/nTot
            expM =  [exp0,           dct1['*ALL*']-exp0,
                     nWrd-exp0,      dct2['*ALL*']-nWrd+exp0]
            # real numbers contingency table
            realM = [dct1[wrd], dct1['*ALL*']-dct1[wrd],
                     dct2[wrd], dct2['*ALL*']-dct2[wrd]]
            chi2statistic,_ = chisquare(realM,expM)
            chi2dict[wrd] = chi2statistic
    storeDictFr(chi2dict,outputDir + file)







        
        
        
        
        
        