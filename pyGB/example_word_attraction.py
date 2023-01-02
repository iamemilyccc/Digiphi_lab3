import ioaux
import dictionaryStuff as ds
from filelocs import metaDir 
from filelocs import gutenbergDir
import compareDists as cd

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)
viFemale = ds.fileLinesToList(metaDir + 'victorianFemale.txt')
viMale = ds.fileLinesToList(metaDir + 'victorianMale.txt')

dictDogSents,dictOther = cd.contextDict(viFemale+viMale,['child','children',"child's","children's"])
cd.mkChi2CompDict(dictDogSents,dictOther,'chi2VictChildren.txt')

eat = ['eat','eats','ate','eaten','eating']
dictEatSents,dictOther = cd.contextDict(viFemale+viMale,eat)
cd.mkChi2CompDict(dictEatSents,dictOther,'chi2VictEating.txt')

dictOW = cd.authDict(['Oscar Wilde'])
dictVW = cd.authDict(['Virginia Woolf'])
dictVict = cd.authDict(viFemale+viMale)
cd.mkChi2CompDict(dictOW,dictVict,'chi2Wilde.txt')
cd.mkChi2CompDict(dictVW,dictVict,'chi2Woolf.txt')