import ioaux
import dictionaryStuff as ds
from filelocs import metaDir 
from filelocs import gutenbergDir
import compareDists as cd
import textMeasures as tm
import dataProcessing as dp
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)
viFemale = ds.fileLinesToList(metaDir + 'victorianFemale.txt')

# dictJA = cd.authDict(['Jane Austen']) #returns a dictionary of the frequency of all tokens in all the author's books

def authbooks(authlist):
    AuthBooks = []
    for i in range(0, len(gutenbergFiles)):
        author = dp.authorFromFileName(gutenbergFiles[i])
        if author in authlist:
            AuthBooks.append(gutenbergFiles[i])
    return AuthBooks

def counttokens(authbooklist):
    tokendictM = defaultdict(int)
    tokendictF = defaultdict(int)
    alltokens = defaultdict(int)
    for book in authbooklist:
        tokens = dp.tokensFromFile(gutenbergDir + book, False) #list of tokens in the book
        for t in tokens:
            if t in ['he','him','his']:
                tokendictM[book] += 1
                alltokens[book] += 1
            elif t in ['she','her']:
                tokendictF[book] += 1
                alltokens[book] += 1
            else:
                alltokens[book] += 1
    return tokendictM, tokendictF, alltokens

def bookrankedbyYear(yearDict):
    years = sorted(yearDict.keys())
    books = []
    for year in years:
        books.append(yearDict[year])
    return books

def genderpronounsRFD(tokendictM, tokendictF, alltokens, books): 
    Mpronoun = []
    Fpronoun = []
    for book in books:
        M = float(tokendictM[book]) / float(alltokens[book]) *100
        F = float(tokendictF[book]) / float(alltokens[book]) *100
        Mpronoun.append(M)
        Fpronoun.append(F)
    return Mpronoun, Fpronoun

def genderpronounAvg(RfdAll):
    sum = float()
    for w in RfdAll:
        sum += w
    return (sum/ len(RfdAll))


def plotting(Mpronoun, Fpronoun):
    barWidth = 0.3
    fig = plt.subplots(figsize = (25,8))
    bar1 = np.arange(len(Mpronoun))
    bar2 = [x + barWidth for x in bar1]
    plt.bar(bar1, Mpronoun, color = (0.2, 0.4, 0.6, 0.6), align='edge', width=barWidth, label = 'Male Pronouns')
    plt.bar(bar2, Fpronoun, color = (0.6, 0.5, 0.4, 0.4), align='edge', width=barWidth, label = 'Female Pronouns')
    plt.xlabel('the Year when the Book was Written', fontweight='bold', fontsize=15)
    plt.ylabel('Rel.frequency (%)', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(Mpronoun))], ['Love And Freindship\n1790', 'Lady Susan\n1794', 'Sense and Sensibility\n1811', 'Pride and Prejudice\n1813', 'Mansfield Park\n1814', 'Emma\n1815', 'Northanger Abbey\n1817', 'Persuasion\n1817'])
    plt.legend()
    plt.show()

def plottingComp(ViMavg, ViFavg, JAMpavg, JAFpavg):
    barWidth = 0.25
    dataAvg = []
    dataJA = []
    dataAvg.append(ViMavg)
    dataAvg.append(ViFavg)
    dataJA.append(JAMpavg)
    dataJA.append(JAFpavg)
    fig = plt.subplots(figsize = (12,8), squeeze=True)
    bar1 = np.arange(len(dataAvg))
    bar2 = [x + barWidth for x in bar1]
    plt.bar(bar1, dataAvg, color = (0.3, 0.6, 0.4, 0.4), align='edge', width=barWidth, label = 'Avg. in the work of Female authors from Victorian Era')
    plt.bar(bar2, dataJA, color = (0.8, 0.6, 0.2, 0.5), align='edge', width=barWidth, label = 'Avg. in the work of Jane Austen')
    plt.xlabel('Gender Pronouns', fontweight='bold', fontsize=15)
    plt.ylabel('Rel.frequency (%)', fontweight='bold', fontsize=15)
    plt.xticks([r + barWidth for r in range(len(dataAvg))], ['Male Pronouns', 'Female Pronouns'])
    plt.legend()
    plt.show()


if __name__ == '__main__':
    viFemaleBooks = authbooks(viFemale)
    JAbooks = authbooks(['Jane Austen'])
    vitokendictM, vitokendictF, vialltokens = counttokens(viFemaleBooks)
    tokendictM, tokendictF, alltokens = counttokens(JAbooks)
    YearDict = {'1815':'Jane Austen___Emma.txt', '1794':'Jane Austen___Lady Susan.txt', '1790':'Jane Austen___Love And Freindship And Other Early Works.txt', '1814':'Jane Austen___Mansfield Park.txt', '1817':'Jane Austen___Northanger Abbey.txt', '1818':'Jane Austen___Persuasion.txt', '1813':'Jane Austen___Pride and Prejudice.txt', '1811':'Jane Austen___Sense and Sensibility.txt'}
    books = bookrankedbyYear(YearDict)
    # print(books)
    viMpro, viFpro = genderpronounsRFD(vitokendictM, vitokendictF, vialltokens, viFemaleBooks)
    AvgviMpro = genderpronounAvg(viMpro)
    AvgviFpro = genderpronounAvg(viFpro)
    # print(AvgviFpro)
    Mpronoun, Fpronoun = genderpronounsRFD(tokendictM, tokendictF, alltokens, books)
    AvgJAM = genderpronounAvg(Mpronoun)
    AvgJAF = genderpronounAvg(Fpronoun)
    plotting(Mpronoun, Fpronoun)
    plottingComp(AvgviMpro, AvgviFpro, AvgJAM, AvgJAF)