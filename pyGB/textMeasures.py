import dataProcessing as dp
import re
import statistics 
import ioaux
from filelocs import gutenbergDir 

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)

class RelFr: 
    
    def __init__(self,terms):
        self.terms= terms
        
    def val(self,tokens,pos,posEnd):
        fr = 0
        for i in range(pos,posEnd):
            if tokens[i].lower() in self.terms:
                fr += 1
        return fr/(posEnd-pos)
    
class NotInDictRelFr: 
    
    def __init__(self,dictionary):
        self.dictionary= dictionary
        
    def val(self,tokens,pos,posEnd):
        fr = 0
        for i in range(pos,posEnd):
            if not tokens[i].lower() in self.dictionary:
                fr += 1
        return fr/(posEnd-pos)

class ReRelFr: 
    
    def __init__(self,regex):
        self.regex = regex
        
    def val(self,tokens,pos,posEnd):
        fr = 0
        for i in range(pos,posEnd):
            if re.match(self.regex,tokens[i].lower()):
                fr += 1
        return fr/(posEnd-pos)

class TypeTokenRatio: 
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        neww = set()
        for j in range(pos,posEnd):
            neww.add(tokens[j].lower())
        return len(neww)/(posEnd-pos)
    
class DialogueRatio: 
    
    def __init__(self,const):
        self.const = const
        
    def val(self,tokens,pos,posEnd):
        inQuote = False
        quotation = 0
        for j in range(pos,posEnd):
            if tokens[j] == 'qtst':
                inQuote = True
            elif tokens[j] == 'qtnd':
                inQuote = False
            elif inQuote:
                quotation += 1  
        return self.const*quotation/(posEnd-pos)
    
class QuotStats: 
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        inQuote = False
        length = 0
        qlens = []
        for j in range(pos,posEnd):
            if tokens[j] == 'qtst':
                inQuote = True
                length = 0
            elif tokens[j] == 'qtnd':
                inQuote = False
                if (length > 1):
                    qlens.append(length)
                length = 0
            elif inQuote:
                length += 1  
        if len(qlens) == 0:
            return 0
        m = statistics.mean(qlens)
        print(str(m) + ": " + str(qlens))
        return statistics.mean(qlens)
    
class InQuoteRelFreq: 
    
    def __init__(self,terms):
        self.terms= terms
        
    def val(self,tokens,pos,posEnd):
        inQuote = False
        quotation = 0
        freq = 0
        for j in range(pos,posEnd):
            if tokens[j] == 'qtst':
                inQuote = True
            elif tokens[j] == 'qtnd':
                inQuote = False
            elif inQuote:
                quotation += 1 
            if inQuote and tokens[j].lower() in self.terms: 
                freq += 1    
        if quotation == 0:
            return 0
        return freq/quotation
    
class InNarrRelFreq: 
    
    def __init__(self,terms):
        self.terms= terms
        
    def val(self,tokens,pos,posEnd):
        inQuote = False
        narrative = 0
        freq = 0
        for j in range(pos,posEnd):
            if tokens[j] == 'qtst':
                inQuote = True
            elif tokens[j] == 'qtnd':
                inQuote = False
            elif not inQuote:
                narrative += 1 
            if inQuote and tokens[j].lower() in self.terms: 
                freq += 1  
        if narrative == 0:
            return 0        
        return freq/narrative
    
class LongRelFr: 
    
    def __init__(self,wl):
        self.wl = wl
        
    def val(self,tokens,pos,posEnd):
        fr = 0
        for j in range(pos,posEnd):
            if len(tokens[j]) >= self.wl:
                fr += 1
        return fr/(posEnd-pos)
    
class AvgWordLn: 
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        wlen = 0
        for i in range(pos,posEnd):
            wlen = wlen + len(tokens[i])  
        return wlen/(posEnd-pos)
    
class AvgSentLn: 
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        sents = dp.sentencesFromTokens(tokens,pos,posEnd)
        return (posEnd-pos)/len(sents)
    
class AutoReadIndex: #https://en.wikipedia.org/wiki/Automated_readability_index
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        sents = dp.sentencesFromTokens(tokens,pos,posEnd)
        chars = 0
        words = 0
        for s in sents:
            for wrd in s:
                if re.match(r'\w[\w\-\']*',wrd):
                    words += 1
                    chars += len(wrd)
        if words < 1 or len(sents) < 1:
            return -1
        return 4.71*(chars/words) + 0.5*words/len(sents) - 21.43
    
class ColemanLiau: #https://en.wikipedia.org/wiki/Automated_readability_index
    
    def __init__(self):
        pass
        
    def val(self,tokens,pos,posEnd):
        sents = dp.sentencesFromTokens(tokens,pos,posEnd)
        chars = 0
        words = 0
        for s in sents:
            for wrd in s:
                if re.match(r'\w[\w\-\']*',wrd):
                    words += 1
                    chars += len(wrd)
        if words < 1 or len(sents) < 1:
            return -1
        return 5.88*(chars/words) - 29.6*len(sents)/words - 15.8
    
class ChunkMeasuring:  
    
    def __init__(self,chunkSize):
        self.chunkSize = chunkSize
    
    def measurements(self,select,measures):
        """Returns a list of lists of measurements of every
        fileStep'th file in the corpus meeting the selection
        condition as divided into (overlapping by chunkSize/2) 
        chunks.
    
        Keyword arguments:
        select -- selection condition 
        fileStep -- only process every fileStep'th file
        measures -- list of measures to be applied to each chunk
        """
        vals = []
        for i in range(len(measures)):
            vals.append([])
        for i in range(0,len(gutenbergFiles),select.fileStep):
            if select.sel(gutenbergFiles[i]):
                print(gutenbergFiles[i])
                tokens = dp.tokensFromFile(gutenbergDir + gutenbergFiles[i],False)
                pos = self.chunkSize # to ignore first chunk
                while pos+self.chunkSize <= len(tokens):
                    for i in range(len(measures)):
                        val = measures[i].val(tokens,pos,pos+self.chunkSize)
                        vals[i].append(val)
                    pos += round(self.chunkSize/2)
        return vals
    
class BookMeasuring:      
    
    def __init__(self):
        pass
    
    def measurements(self,select,measures):
        """Returns a list of lists of measurements of every
        fileStep'th file in the corpus meeting the selection
        condition as whole units.
    
        Keyword arguments:
        select -- selection condition 
        fileStep -- only process every fileStep'th file
        measures -- list of measures to be applied to each chunk
        """
        vals = []
        for i in range(len(measures)):
            vals.append([])
        for i in range(0,len(gutenbergFiles),select.fileStep):
            if select.sel(gutenbergFiles[i]):
                print(gutenbergFiles[i])
                tokens = dp.tokensFromFile(gutenbergDir + gutenbergFiles[i],False)
                for i in range(len(measures)):
                    val = measures[i].val(tokens,0,len(tokens))
                    vals[i].append(val)
        return vals
