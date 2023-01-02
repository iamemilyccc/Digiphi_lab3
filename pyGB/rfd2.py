import textMeasures as tm
import distribBars as db
from filelocs import metaDir 
import dictionaryStuff as ds

victM = ds.fileLinesToList(metaDir + 'victorianMale.txt')
victF = ds.fileLinesToList(metaDir + 'victorianFemale.txt')

db.plotFeatFeat(victM+victF,[tm.RelFr(['thing','things']),tm.RelFr(['world','worlds'])],10000,15,
                'Two words',('thing','world'),'twonouns',showPlot=False) 



