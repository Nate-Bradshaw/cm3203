import random as rand
from math import floor

import gaClasses as gac
import gaFunctions as gaf

from sys import argv, exit
from os import path

#? add verbose / non verbose option?
#usage:
#& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py 
# filePath(path).mid 
# popSize(pos int) 
# CrossoverProb(0-1 float) 
# MutationProb(0-1 float) 
# noteRangeEx(pos int)
# Scale(note then maj/min with sepperating / e.g. d#/maj, only uses sharps, no flats)

if(len(argv) < 2):
    print("mEror, not enough args, please give a file")
    exit()


#TODO: put these into args
if(path.exists(argv[1])): inputMidiPath = argv[1]
else: 
    print(f"mEror, path {argv[1]} doesnt exist")
    exit()

if(len(argv) >= 3):
    try:
        popSize = int(argv[2])
        print(popSize)
        if(popSize <= 1 or popSize > 1024 or popSize % 2 != 0):
            print(f"mEror, popsize {popSize} is out of range 2 to 1000 or not an even number")
            exit()
    except:
        print(f"mEror, popsize {argv[2]} is not an int or not entered correctly")
        exit()
else:
    print("No pop size given! defaulting to 32")
    popSize = 32

if(len(argv) >= 4):
    try:
        crossoverProb = float(argv[3])
        print(crossoverProb)
        if(crossoverProb > 1 or crossoverProb < 0):
            print(f"mEror, crossover prob {crossoverProb} is out of range 0 to 1")
            exit()
    except:
        print(f"mEror, crossover prob {argv[3]} is not an float or not entered correctly")
        exit()
else:
    print("No crossover prob given! defaulting to 0.7")
    crossoverProb = 0.7
    
if(len(argv) >= 5):
    try:
        mutationProb = float(argv[4])
        print(mutationProb)
        if(mutationProb > 1 or mutationProb < 0):
            print(f"mEror, mutation prob {mutationProb} is out of range 0 to 1")
            exit()
    except:
        print(f"mEror, mutation prob {argv[4]} is not an float or not entered correctly")
        exit()
else:
    print("No mutation prob given! defaulting to 0.5")
    mutationProb = 0.5

if(len(argv) >= 6):
    try:
        rangeIn = int(argv[5])
        if(rangeIn < 0 or rangeIn > 127):
            print(f"mEror, note range extention {rangeIn} is out of range 0 to 127")
            exit()
        nRange = gaf.getNoteRange(inputMidiPath, rangeIn)
    except:
        print(f"mEror, note range extention {argv[5]} is not an int or not entered correctly")
        exit()
else:
    print("No note range extension given! defaulting 127 (all midi note pitches allowed)")
    nRange = gaf.getNoteRange(inputMidiPath, 127)

if(len(argv) >= 7):
    scale = argv[6].split("/")
    #algorithm for knowing a root notes midi value and then making a list of all in range (above) based on major or minor scale
else:
    print("No scale given! defaulting to no scale (all notes allowed)")


inputEmb = gaf.getEmbeddingFile(inputMidiPath)

md = gaf.getMetadata(inputMidiPath)
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
    newBar.addNote(gac.note(gaf.getRandomNote(nRange), 1))
    bars.append(newBar)

# for each whole int in expInd, that bar gets a slot. e.g. 2.5 would be 2 slots with a 0.5 chance of a 3rd
# any with 0 slots are eliminated, any with 1 stay and any with more get multiple slots
i = 0



for i in range(100):
    print(f"gen {i}")
    parentBars = gaf.getParents(bars, popSize, inputEmb, tsNumerator, tsDenominator, bpm)
    f = gaf.getFittest(parentBars)
    print(f"fittest member fitness: {f.fitness}")

    if(f.fitness >= 0.95):
        #pass
        #gaf.renderMidi(f, tsNumerator, tsDenominator, name=f"genTest/geni{i}_fit{f.fitness}")
        gaf.renderMidi(f, tsNumerator, tsDenominator, name=f"genTest/nearMatch")
        f.printNotes()

    #gaf.renderMidi(f, tsNumerator, tsDenominator, name=f"genTest/{i}geni_fit{f.fitness}")


    bars = gaf.crossover(parentBars, tsNumerator, mutationProb, crossoverProb, nRange)

    cumBarLen = 0
    for j in range(len(bars)):
        cumBarLen += len(bars[j].notes)
    

    print(f"avr bar len of this gen = {cumBarLen / len(bars)}")
    #bars[1].printNotes()


    #gaf.renderMidi(bars[maxBarj], tsNumerator, tsDenominator, name=f"genTest/Gen{i+1}_{maxBarj}")
    #gaf.renderMidi(bars[1], tsNumerator, tsDenominator, name=f"genTest/Gen{i+1}_{1}")

