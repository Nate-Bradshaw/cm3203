import random as rand
from math import floor

import gaClasses as gac
import gaFunctions as gaf


inputMidiPath = "midi/Untitled_15.mid"

md = gac.getMetadata(inputMidiPath)

inputEmb = gaf.getEmbeddingFile(inputMidiPath)

popSize = 32

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
    newBar.addNote(gac.note(rand.randint(21, 108), tsNumerator))
    bars.append(newBar)

# for each whole int in expInd, that bar gets a slot. e.g. 2.5 would be 2 slots with a 0.5 chance of a 3rd
# any with 0 slots are eliminated, any with 1 stay and any with more get multiple slots

for i in range(10):
    parentBars = gaf.getParents(bars, popSize, inputEmb, tsNumerator, tsDenominator, bpm)
    bars = gaf.crossover(parentBars, tsNumerator, 0)
    gac.renderMidi(bars[0], tsNumerator, tsDenominator, name=f"Gen{i+1}")