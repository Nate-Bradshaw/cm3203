import random as rand

import gaClasses as gac
import fitnessFunction as f

inputMidiPath = "midi/Untitled_15.mid"

md = gac.getMetadata(inputMidiPath)

inputEmb = f.getEmbeddingFile(inputMidiPath)

popSize = 32

tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]
#print(tsNumerator)
#print(tsDenominator)
#print(bpm)


#tsUpper = 3, tsLower = 4 is a time signiture of 3/4

bars = []

#create a bunch of random bars, 4 quarter notes each with rests
for i in range(popSize):
    newBar = gac.bar()
    for j in range(tsNumerator):
        #21 to 108 is all the notes on a piano named 1 to 88, aka A0 to C8
        #j used, first note is at beat 1 for the bar up to tsUpper
        #! indexing beats from 1 in notes, keep this in mind
        #durration of 1 beat, which would be a quater note with tsLower of 4 (E.g in 4/4 time sig)
        newNote = gac.note(rand.randint(21, 108), j+1, 1)
        #print(newNote.pitch)
        newBar.addNote(newNote)
    bars.append(newBar)
    f.compareEmbeddings(inputEmb, f.getEmbeddingBuf(gac.renderMidi(bars[i], tsNumerator, tsDenominator, bpm, createFile=False)))




def crossover():
    pass



"""
n1 = c.note("c4", 4.67, 2)
n2 = c.note("b2", 0, -1)

#print(n1.pitch)

b1 = c.bar()

b1.addNote(n1)
b1.addNote(n2)

print(b1.notes[0].pitch)
print(b1.notes[1].pitch)

n1 = c.note("a1", 4.67, 2) #creates a new object, list has ref to old object
n2.pitch = "e5" #changes refferenced object, same object that the list has access to

print(b1.notes[0].pitch)
print(b1.notes[1].pitch)
"""