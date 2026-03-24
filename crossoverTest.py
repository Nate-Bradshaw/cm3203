import random as rand
from math import floor

import gaClasses as gac
import gaFunctions as gaf

inputMidiPath = "midi/Untitled_15.mid"

md = gaf.getMetadata(inputMidiPath)

inputEmb = gaf.getEmbeddingFile(inputMidiPath)

popSize = 2

tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]
bars = []

sumFitness = 0

#create a bunch of random bars, 4 quarter notes each with rests and then giving them a simularity score
for i in range(popSize):
    newBar = gac.bar()
    #starting with a full note
    newBar.addNote(gac.note(rand.randint(20, 21), tsNumerator))
    bars.append(newBar)

gaf.renderMidi(bars[0], tsNumerator, tsDenominator, name=f"coTestInput0")
gaf.renderMidi(bars[1], tsNumerator, tsDenominator, name=f"coTestInput1")

print(f"sum fitness: {sumFitness}")
print(f"avr fitness: {sumFitness/popSize}")

crBars = gaf.crossover(bars, tsNumerator, 0)

gaf.renderMidi(crBars[0], tsNumerator, tsDenominator, name=f"coTestOutput0")
gaf.renderMidi(crBars[1], tsNumerator, tsDenominator, name=f"coTestOutput1")

#case cobeat = 1
#output is mirrored inputs, as the whole beat replaces, works as intended