import textMeasures as tm
import plotTwoDimensions as p2d
import dictionaryStuff as ds
from filelocs import metaDir 

fvAuth = ds.fileLinesToList(metaDir + 'fiveVictorian.txt')
feats = [tm.RelFr(['and']),tm.RelFr(['the']),tm.RelFr(['that']),
         tm.RelFr(['is']),tm.RelFr(['with'])]

p2d.plotDocsByAuth(fvAuth,feats,p2d.LDAtransf(),'fvAuth',showPlot=False)
      
p2d.plotAuthReuseFeats(fvAuth,feats,p2d.PCAtransf(),'fvAuth','fvAuthPCA',showPlot=False)      

p2d.plotAuthReuseFeats(fvAuth,feats,p2d.TSNEtransf(),'fvAuth','fvAuthTSNE',showPlot=False)      