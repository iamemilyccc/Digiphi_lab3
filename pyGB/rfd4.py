import textMeasures as tm
import distribBars as db
from filelocs import metaDir 
import dictionaryStuff as ds

victM = ds.fileLinesToList(metaDir + 'victorianMale.txt')
victF = ds.fileLinesToList(metaDir + 'victorianFemale.txt')
prMasc = ['he','him','his']
prFem = ['she','her']

db.plotGrGr(victF,victM,tm.RelFr(prFem),2000,15,
            'Fem. pns',('women','men'),'femProVict',showPlot=False) 

db.plotGrGr(victF,victM,tm.RelFr(prMasc),2000,15,
            'Masc. pns',('women','men'),'mascProVict',showPlot=False) 

db.plotGrGr(victF,victM,tm.RelFr('and'),500,15,
            '"and"',('women','men'),'andGendVict',showPlot=False) 

db.plotGrGr(victF,victM,tm.RelFr('the'),500,15,
            '"the"',('women','men'),'theGendVict',showPlot=False) 
