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
# octaveRange(pos int)
# notes(list of notes sepperated by (use # to indicate black keys on a keyboard) "/" e.g. c/d/d#/f/g#
#   these will be the notes that the GA can use
#   leave empty or as "all" to use all notes

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
        octaveRange = int(argv[5])
        if(octaveRange < 0 or octaveRange > 10):
            print(f"mEror, octave range {octaveRange} is out of range 0 to 11")
            exit()
    except:
        print(f"mEror, octave range {argv[5]} is not an int or not entered correctly")
        exit()
else:
    print("No octave range given! defaulting to 1")
    octaveRange = 1

# midi 0 is a c (not a named note, but would be c (asumedly))
# midi 127 is G9
# middle C is midi 60
# octaves are 12 notes long
if(len(argv) >= 7):
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    allowedNotes = []
    if(argv == "all"):
        allowedNotes = [0,1,2,3,4,5,6,7,8,9,10,11]
    else:
        noteIn = argv[6].split("/")
        for n in noteIn:
            if(len(n) == 1 or len(n) == 2):
                n = n.upper()
                if(n in notes):
                    allowedNotes.append(notes.index(n))
                else:
                    print(f"given note {n} is not a note or formatted incorectly, skipping")
        allowedNotes = list(set(allowedNotes))
        allowedNotes.sort()

        nRange = gaf.getOctaveRange(inputMidiPath, octaveRange)
        print(nRange)

        allowedPitches = []

        for p in range(nRange[1]-nRange[0]):
            p += nRange[0]
            if((p%12) in allowedNotes):
                allowedPitches.append(p)

        print(allowedPitches)

else:
    print("No notes given! defaulting to all notes allowed")

print(allowedNotes)
exit()


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

