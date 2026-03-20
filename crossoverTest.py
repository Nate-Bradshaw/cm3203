import random as rand
from math import floor

import gaClasses as gac
import fitnessFunction as f

inputMidiPath = "midi/Untitled_15.mid"

md = gac.getMetadata(inputMidiPath)

inputEmb = f.getEmbeddingFile(inputMidiPath)

popSize = 2

tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]
bars = []

sumFitness = 0

#create a bunch of random bars, 4 quarter notes each with rests and then giving them a simularity score
for i in range(popSize):
    newBar = gac.bar()
    #TODO: with some randomness allow the starting pop have full notes. Start with a full note, with a chance to be subdivided. repeat for all
    #TODO: until all notes have been passed and not subdivided
    for j in range(tsNumerator):
        newNote = gac.note(rand.randint(21, 108), 1)
        newBar.addNote(newNote)
    bars.append(newBar)
    gac.renderMidi(bars[i], tsNumerator, tsDenominator, name=f"coTest{i}")
    #similarityScore = f.compareEmbeddings(inputEmb, f.getEmbeddingBuf(gac.renderMidi(bars[i], tsNumerator, tsDenominator, bpm, createFile=False)))
    #bars[i].fitness = similarityScore
    #sumFitness += similarityScore


print(f"sum fitness: {sumFitness}")
print(f"avr fitness: {sumFitness/popSize}")

gac.renderMidi(gac.crossover(bars[0], bars[1]), tsNumerator, tsDenominator, name=f"coTestOutput")