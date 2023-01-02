import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
import textMeasures as tm
from filelocs import outputDir 

#Based on
#http://www.apnorton.com/blog/2016/12/19/Visualizing-Multidimensional-Data-in-Python/
#https://medium.com/@luckylwk/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b

# Appearance of plots
col = ['red','dodgerblue','palegreen','darkgray','maroon','orange']
mrkr = ['v','>','o','^','s','o']

class LDAtransf:
    def transf(self,X_norm,y):
        lda = LDA(n_components=2) #2-dimensional LDA
        return pd.DataFrame(lda.fit_transform(X_norm, y))
    
class TSNEtransf:
    def transf(self,X_norm,y):
        tsne = TSNE(n_components=2, verbose=1, perplexity=15, n_iter=500)
        return pd.DataFrame(tsne.fit_transform(X_norm))
    
class PCAtransf:
    def transf(self,X_norm,y):
        pca = sklearnPCA(n_components=2) #2-dimensional PCA
        return pd.DataFrame(pca.fit_transform(X_norm))

def scatter(name,name2,feats,transf,labels,showPlot=True):
    cols =  ['Class']
    for i in range(feats):
        cols.append('W' + str(i+1))
    data = pd.read_csv(outputDir + name + '.csv',names=cols)
    y = data['Class']          # Split off classifications
    X = data.loc[:, 'W1':]     # Split off features
    X_norm = (X - X.min())/(X.max() - X.min())
    transformed = transf.transf(X_norm,y)
    plt.figure(figsize=(7,5))
    for i in range(0,len(labels)):
            plt.scatter(transformed[y==i][0],transformed[y==i][1],
                        marker=mrkr[i],s=20,label=labels[i],c=col[i])
    plt.legend()
    plt.savefig(outputDir + name2 + '.png',dpi=600,bbox_inches='tight')
    if showPlot:
        plt.show()
        
import dataProcessing as dp
bookM = tm.BookMeasuring()
  
def plotDocsByAuth(auths,meas,transf,name,showPlot=True):
    text_file = open(outputDir + name + '.csv', "w", encoding="utf8")
    for i in range(len(auths)):
        vals = bookM.measurements(dp.SelAuthor([auths[i]],1),meas)
        for j in range(len(vals[0])):
            vstr = str(i) + ','
            for k in range(len(meas)):
                vstr = vstr + str(round(vals[k][j]*10000)/10000) + ','
            text_file.write(vstr[0:-1] + '\n')
    text_file.close()
    labels = []
    for a in auths:
        labels.append(a.split(' ')[-1])
    scatter(name,name,len(meas),transf,labels,showPlot=showPlot)

def plotAuthReuseFeats(auths,meas,transf,name,name2,showPlot=True):
    labels = []
    for a in auths:
        labels.append(a.split(' ')[-1])
    scatter(name,name2,len(meas),transf,labels,showPlot=showPlot)