import textMeasures as tm
import bookplot as bp

book = 'Agatha Christie___The Mysterious Affair at Styles.txt'
labels = ['Inglethorp','Howard','Poirot']
tms = [tm.RelFr(['alfred','inglethorp']),
       tm.RelFr(['evelyn','howard']),
       tm.RelFr(['hercule','poirot'])]

bp.plotBook(book,tms,labels,20,
            'mysteriousAffair',showPlot=False)

tms = [tm.RelFr(['leopold','bloom']),
       tm.RelFr(['stephen','dedalus']),
       tm.RelFr(['i','me','my','we','us','our',])]
labels = ['LB','SD','1st']
bp.plotBook('James Joyce___Ulysses.txt',tms,labels,30,
            'ulysses',showPlot=False)