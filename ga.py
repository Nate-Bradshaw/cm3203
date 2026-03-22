import random as rand
from math import floor

import gaClasses as gac
import fitnessFunction as f

def getParents(barsIn, popSizeIn):
    nextBars = []
    eiFractionSum = 0
    for i in range(popSizeIn):
        #amount to be included guarenteed in next generation
        #https://datajobstest.com/data-science-repo/Genetic-Algorithm-Guide-[Tom-Mathew].pdf 2.7
        #expected individuals
        barsIn[i].ei = (barsIn[i].fitness / sumFitness) * popSizeIn
        n = floor(barsIn[i].ei)
        eiFractionSum += barsIn[i].ei-n
        print(f"bar {i} with ei {barsIn[i].ei} evaluated")
        for j in range(n):
            print(f"bar {i} with ei {barsIn[i].ei} added to next gen")
            nextBars.append(barsIn[i])

    # ei fractional / sum of fractional = normalised prob between 0-1
    # then find how many slots are left, sl
    # get a random number between 0-1, get values ei(n) < r <= ei(n+1), same for r + 1/sl % 1


    slotsLeft = popSizeIn - len(nextBars)
    print(f"slots left = {slotsLeft} from {popSizeIn} - {len(nextBars)}")
    r = rand.random()
    eiNormSum = 0
    for i in range(slotsLeft):
        pointer = (r + (1/slotsLeft)*i) % 1
        print(f"pointer: {pointer}")
        eiNormSum = 0
        for j in range(popSizeIn):
            print(f"norm sum: {eiNormSum}")
            if(eiNormSum < pointer):
                eiNormSum += (barsIn[j].ei - floor(barsIn[j].ei)) / eiFractionSum
            else:
                nextBars.append(barsIn[j-1])
                print(f"bar {j} with ei {barsIn[j].ei} added to next gen in SUS")
                break

    print(f"new gen size: {len(nextBars)}")
    #fittest chromosomes will stay at the start of the new list, as they had a ei of 1 or higher
    #! although if ei is 2 or higher, there will duplicate genes, cossover of these genes would do nothing so there should be some randomness

    return nextBars

def crossover(barsIn, tsN):
    barsOut = []

    for i in range(len(barsIn)//2):
        #initial, picking the beat
        coBeat = rand.randint(1,tsN)
        bar1 = barsIn.pop(rand.randint(0, len(barsIn)-1))
        bar2 = barsIn.pop(rand.randint(0, len(barsIn)-1))

        subdiv = 0.5
        #* limiting to 1/64th notes
        for i in range(4):
            r = rand.random()
            #2/4 chance of terminating and keeping the current split position
            if(r < 0.5):
                break
            #1/4 of going down a level at the increment forward
            elif(r < 0.75):
                coBeat += subdiv
            #1/4 of going down a level at an current position
            subdiv /= 2
        
        barsOut.append(cr(bar1, bar2, coBeat))
        barsOut.append(cr(bar2, bar1, coBeat))
    
    return barsOut

def cr(bar1, bar2, coBeat):
    #* indexing from 1 where 1 is the starting beat in the bar
    cBar = gac.bar()

    #second bar in a crossover overides the first one
    cumBeats = 1
    for i in range(len(bar1.notes)):
        if(cumBeats >= coBeat):
            #go back and clip the end of last note
            if(len(cBar.notes) > 1):
                cBar.notes[len(cBar.notes)-1].duration = coBeat - cBar.getNoteBeat(i-1)
            break
        else:
            cumBeats += bar1.notes[i].duration
            cBar.addNote(gac.note(bar1.notes[i].pitch, bar1.notes[i].duration))
    cumBeats = 1
    for i in range(len(bar2.notes)):
        if(cumBeats < coBeat):
            cumBeats += bar2.notes[i].duration
            if(cumBeats > coBeat):
                cBar.addNote(gac.note(bar2.notes[i].pitch, (bar2.getNoteBeat(i) + bar2.notes[i].duration) - (cBar.getNoteBeat(len(cBar.notes)-1) + cBar.notes[len(cBar.notes)-1].duration)))
        else:
            cBar.addNote(gac.note(bar2.notes[i].pitch, bar2.notes[i].duration))
    
    return cBar

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
        newNote = gac.note(rand.randint(21, 108), 1)
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

parentBars = getParents(bars, popSize)
bars = crossover(parentBars, tsNumerator)