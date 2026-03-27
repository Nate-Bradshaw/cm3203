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

newBar = gac.bar()
newBar.addNote(gac.note(50, 1))
#newBar.addNote(gac.note(55, 2))
bars.append(newBar)
newBar = gac.bar()
newBar.addNote(gac.note(30, 1))
#newBar.addNote(gac.note(35, 2))
bars.append(newBar)

gaf.renderMidi(bars[0], tsNumerator, tsDenominator, name=f"coTestInput0")
gaf.renderMidi(bars[1], tsNumerator, tsDenominator, name=f"coTestInput1")


for i in range(1):
    bars = []
    newBar = gac.bar()
    newBar.addNote(gac.note(50, 1))
    newBar.addNote(gac.note(55, 2))
    bars.append(newBar)
    newBar = gac.bar()
    newBar.addNote(gac.note(30, 1))
    newBar.addNote(gac.note(35, 2))
    bars.append(newBar)

    #crBars = gaf.crossover(bars, tsNumerator, 0)
    gaf.mutate(bars[0])
    gaf.mutate(bars[1])

    gaf.renderMidi(bars[0], tsNumerator, tsDenominator, name=f"mutateTest0")
    gaf.renderMidi(bars[1], tsNumerator, tsDenominator, name=f"mutateTest1")


    #gaf.renderMidi(crBars[0], tsNumerator, tsDenominator, name=f"coTestOutput{i}_0")
    #gaf.renderMidi(crBars[1], tsNumerator, tsDenominator, name=f"coTestOutput{i}_1")


#case cobeat = 1
#output is mirrored inputs, as the whole beat replaces, works as intended