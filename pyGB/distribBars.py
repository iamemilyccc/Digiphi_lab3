import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import dataProcessing as dp
import dictionaryStuff as ds
from filelocs import outputDir 
from filelocs import metaDir 
import textMeasures as tm

femaleAuth = ds.fileLinesToList(metaDir + "femaleAuthors.txt")
    
yFactor = 1000 # will turn e.g. relative frequencies into per mille.
    
def plot2distr(sel1,sel2,meas,measuring,barN,title,cats,fname,showPlot=True):
    vals1 = measuring.measurements(sel1,[meas])
    vals1 = sortAndFilter(vals1,0.98)
    vals2 = measuring.measurements(sel2,[meas])  
    vals2 = sortAndFilter(vals2,0.98)
    plot(vals1[0],vals2[0],barN,title,cats,fname,showPlot=showPlot)    
    
def plotGrGr(list1,list2,meas,chunkSize,barN,title,cats,fname,showPlot=True):
    measuring = tm.ChunkMeasuring(chunkSize)
    sel1 = dp.SelAuthor(list1,1)
    sel2 = dp.SelAuthor(list2,1)
    plot2distr(sel1,sel2,meas,measuring,barN,title,cats,fname,showPlot=showPlot)
        
def plotGrGrWorks(list1,list2,meas,barN,title,cats,fname,showPlot=True):
    bookM = tm.BookMeasuring()
    sel1 = dp.SelAuthor(list1,1)
    sel2 = dp.SelAuthor(list2,1)
    plot2distr(sel1,sel2,meas,bookM,barN,title,cats,fname,showPlot=showPlot)
     
def plotFeMa(meas,chunkSize,barN,title,fname,mStep,showPlot=True):
    measuring = tm.ChunkMeasuring(chunkSize)
    sel1 = dp.SelAuthor(femaleAuth,1)
    sel2 = dp.SelAuthorCompl(femaleAuth,mStep)
    plot2distr(sel1,sel2,meas,measuring,barN,title,('Female', 'Male'),fname,showPlot=showPlot)
       
def plotFeatFeat(auths,meas,chunkSize,barN,title,cats,fname,showPlot=True):
    chunkM = tm.ChunkMeasuring(chunkSize)
    vals = chunkM.measurements(dp.SelAuthor(auths,1),meas)
    vals = sortAndFilter(vals,0.98)
    plot(vals[0],vals[1],barN,title,cats,fname,showPlot=showPlot)

def bars(vals,minV,step,barsN): 
    staples = [0] * barsN
    for val in vals:
        interv = math.floor((val - minV) / step)
        if interv == barsN:
            interv = interv - 1
        staples[interv] += 1
    for i in range(0,barsN):
        staples[i] = (100.0 * staples[i])/len(vals)
    return staples

def plot(vals1,vals2,barN,title,cats,fname,showPlot=True):
    maxV = max(vals1[-1],vals2[-1])
    minV = min(vals1[0],vals2[0])
    step = (maxV - minV)/barN
    xVals = []
    for i in range(0,barN+1):
        xVals.append(minV + i * step)
    bars1 = bars(vals1,minV,step,barN)
    bars2 = bars(vals2,minV,step,barN)
    fig = plt.figure(figsize=(7,5))
    ax = fig.add_subplot(111)
    plt.title(title + ' n=(' + str(len(vals1)) + ', ' + str(len(vals2)) + ')')
    width = 2
    dist = 6
    posns = np.arange(0,dist*barN,dist)  # the x locations for the groups
    rects1 = ax.bar(posns+dist/2-0.5*width, bars1, width, color='blue')
    rects2 = ax.bar(posns+dist/2+0.5*width, bars2, width, color='red')
    ax.set_ylabel('Fraction of chunks')
    labels = [''] * (barN+1)
    for p in range(0,barN+1,2):
        labels[p] = str(round(yFactor*xVals[p]))
    ax.set_xticks(posns)
    ax.set_xticklabels(labels)
    ax.legend( (rects1[0], rects2[0]), cats )
    plt.savefig(outputDir + fname + '.png',dpi=600,bbox_inches='tight')
    if showPlot:
        plt.show()
        
def sortAndFilter(vals,keepFr):
    """Used to remove extremely high values, in list of list of values"""
    for i in range(len(vals)):
        vals[i].sort()
        keep = round(keepFr*len(vals[i]))
        vals[i] = vals[i][0:keep]
    return vals
    
