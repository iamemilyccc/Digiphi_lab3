import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import dataProcessing as dp
from filelocs import gutenbergDir 
from filelocs import outputDir 

col = ['dodgerblue','red','black','orange','darkgreen','darkgray','maroon']
mrkr = ['+','v','o','v','o','^','s','>','o']

def smooth(curve):
    curves = [0.0] * len(curve)
    curves[0] = curve[0]
    curves[len(curve)-1] = curve[len(curve)-1]
    for i in range(1,len(curve)-1):
        curves[i] = (curve[i-1] + curve[i] + curve[i+1])/3
    return curves 
        
def plotBook(file,meas,labels,chunks,img,showPlot=True):
    tokens = dp.tokensFromFile(gutenbergDir + file,False)
    dataBook = []
    for i in range(len(meas)):
        dataBook.append([])
    x_val = []
    pos = 0
    chunk = 0
    while chunk < chunks:
        cl = round((len(tokens)-pos)/(chunks-chunk))
        for i in range(len(meas)):
            dataBook[i].append(meas[i].val(tokens,pos,pos+cl))
        x_val.append((chunk+1)/chunks)
        pos = pos + cl
        chunk += 1
    plt.figure(figsize=(7,5),num=file)
    for i in range(len(dataBook)):
        plt.plot(x_val,dataBook[i],color=col[i],marker=mrkr[i],label=labels[i])
    plt.legend()
    plt.savefig(outputDir + img + '.png',dpi=600,bbox_inches='tight')
    if showPlot:
        plt.show()
