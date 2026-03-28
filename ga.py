import random as rand
from math import floor

import gaClasses as gac
import gaFunctions as gaf


inputMidiPath = "midi/Untitled_15.mid"

md = gaf.getMetadata(inputMidiPath)

inputEmb = gaf.getEmbeddingFile(inputMidiPath)

popSize = 16

tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]
#print(tsNumerator)
#print(tsDenominator)
#print(bpm)


#tsUpper = 3, tsLower = 4 is a time signiture of 3/4

bars = []

#create a bunch of random bars, 4 quarter notes each with rests and then giving them a simularity score
for i in range(popSize):
    newBar = gac.bar()
    #starting with a full note
    #! if randint hits 20 or lower, the bar will be just a rest, thus breaking the embedding 
    #! and causing a crash: improve midi renderer to properly render rests to re-impliment
    newBar.addNote(gac.note(rand.randint(21, 108), 1))
    bars.append(newBar)

# for each whole int in expInd, that bar gets a slot. e.g. 2.5 would be 2 slots with a 0.5 chance of a 3rd
# any with 0 slots are eliminated, any with 1 stay and any with more get multiple slots
i = 0



for i in range(100):
    print(f"gen {i}")
    parentBars = gaf.getParents(bars, popSize, inputEmb, tsNumerator, tsDenominator, bpm)
    f = gaf.getFittest(parentBars)
    if(f.fitness >= 0.8):
        gaf.renderMidi(f, tsNumerator, tsDenominator, name=f"genTest/0.8")
        break

    bars = gaf.crossover(parentBars, tsNumerator, 0.5)

    maxBarLen = 0
    maxBarj = 0
    for j in range(len(bars)):
        if (maxBarLen < len(bars[j].notes)):
            maxBarLen = len(bars[j].notes)
            maxBarj = j

    print(f"max bar len of this gen = {maxBarLen}")

    bars[maxBarj].printNotes()
    #bars[1].printNotes()


    #gaf.renderMidi(bars[maxBarj], tsNumerator, tsDenominator, name=f"genTest/Gen{i+1}_{maxBarj}")
    #gaf.renderMidi(bars[1], tsNumerator, tsDenominator, name=f"genTest/Gen{i+1}_{1}")

