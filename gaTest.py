import random as rand
from math import floor

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

sumFitness = 0

#create a bunch of random bars, 4 quarter notes each with rests and then giving them a simularity score
for i in range(popSize):
    newBar = gac.bar()
    #TODO: with some randomness allow the starting pop have full notes. Start with a full note, with a chance to be subdivided. repeat for all
    #TODO: until all notes have been passed and not subdivided
    for j in range(tsNumerator):
        #21 to 108 is all the notes on a piano named 1 to 88, aka A0 to C8
        #j used, first note is at beat 1 for the bar up to tsUpper
        #! indexing beats from 1 in notes, keep this in mind
        #durration of 1 beat, which would be a quater note with tsLower of 4 (E.g in 4/4 time sig)
        newNote = gac.note(rand.randint(21, 108), j+1, 1)
        #print(newNote.pitch)
        newBar.addNote(newNote)
    bars.append(newBar)
    similarityScore = f.compareEmbeddings(inputEmb, f.getEmbeddingBuf(gac.renderMidi(bars[i], tsNumerator, tsDenominator, bpm, createFile=False)))
    bars[i].fitness = similarityScore
    sumFitness += similarityScore
# Stochastic remainder selection

print(f"sum fitness: {sumFitness}")
print(f"avr fitness: {sumFitness/popSize}")



# for each whole int in expInd, that bar gets a slot. e.g. 2.5 would be 2 slots with a 0.5 chance of a 3rd
# any with 0 slots are eliminated, any with 1 stay and any with more get multiple slots

nextBars = []
eiFractionSum = 0
for i in range(popSize):
    #amount to be included guarenteed in next generation
    #https://datajobstest.com/data-science-repo/Genetic-Algorithm-Guide-[Tom-Mathew].pdf 2.7
    #expected individuals
    bars[i].ei = (bars[i].fitness / sumFitness) * popSize
    n = floor(bars[i].ei)
    eiFractionSum += bars[i].ei-n
    print(f"bar {i} with ei {bars[i].ei} evaluated")
    for j in range(n):
        print(f"bar {i} with ei {bars[i].ei} added to next gen")
        nextBars.append(bars[i])

# ei fractional / sum of fractional = normalised prob between 0-1
# then find how many slots are left, sl
# get a random number between 0-1, get values ei(n) < r <= ei(n+1), same for r + 1/sl % 1


slotsLeft = popSize - len(nextBars)
print(f"slots left = {slotsLeft} from {popSize} - {len(nextBars)}")
r = rand.random()
eiNormSum = 0
for i in range(slotsLeft):
    pointer = (r + (1/slotsLeft)*i) % 1
    print(f"pointer: {pointer}")
    eiNormSum = 0
    for j in range(popSize):
        print(f"norm sum: {eiNormSum}")
        if(eiNormSum < pointer):
            eiNormSum += (bars[j].ei - floor(bars[j].ei)) / eiFractionSum
        else:
            nextBars.append(bars[j-1])
            print(f"bar {j} with ei {bars[j].ei} added to next gen in SUS")
            break



print(f"new gen size: {len(nextBars)}")




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