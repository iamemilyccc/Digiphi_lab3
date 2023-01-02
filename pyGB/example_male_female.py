import ioaux
import dictionaryStuff as ds
from filelocs import metaDir 
from filelocs import gutenbergDir
import compareDists as cd

gutenbergFiles = ioaux.getTxtFiles(gutenbergDir)
viFemale = ds.fileLinesToList(metaDir + 'victorianFemale.txt')
viMale = ds.fileLinesToList(metaDir + 'victorianMale.txt')

dictVictF = cd.authDict(viFemale)
dictVictM = cd.authDict(viMale)
cd.mkChi2CompDict(dictVictF,dictVictM,'chi2VicFem.txt')
cd.mkChi2CompDict(dictVictM,dictVictF,'chi2VicMen.txt')

#dictVict = cd.authDict(viFemale+viMale)
#dictWSM = cd.authDict(['William Somerset Maugham'])
#cd.mkChi2CompDict(dictWSM,dictVict,'chi2Maugham.txt')
#dictVW = cd.authDict(['Virginia Woolf'])
#cd.mkChi2CompDict(dictVW,dictVict,'chi2Woolf.txt')



