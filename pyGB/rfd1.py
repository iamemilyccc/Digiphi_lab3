import textMeasures as tm
import distribBars as db
from filelocs import metaDir 
import dictionaryStuff as ds

victM = ds.fileLinesToList(metaDir + 'victorianMale.txt')
victF = ds.fileLinesToList(metaDir + 'victorianFemale.txt')

db.plotFeatFeat(victM+victF,[tm.RelFr(['the']),tm.RelFr(['and'])],500,15,
                'Two words',('the','and'),'theand',showPlot=False) 

prMasc = ['he','him','his']
prFem = ['she','her']

db.plotFeatFeat(victF+victM,[tm.RelFr(prFem),tm.RelFr(prMasc)],2000,15,
                'Gendered pronouns',('fem','masc'),'genderedpro',showPlot=False) 


