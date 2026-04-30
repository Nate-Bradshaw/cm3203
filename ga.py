import random as rand
from math import floor
from sys import argv, exit

import gaClasses as gac
import gaFunctions as gaf
import argsParser

#? add verbose / non verbose option?
#usage:
#& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py 
# filePath(path).mid 
# popSize(pos int) 
# number of generations
# top n individuals to be outputted
# CrossoverProb(0-1 float) 
# MutationProb(0-1 float) 
# octaveRange(pos int)
# notes(list of notes sepperated by (use # to indicate black keys on a keyboard) "," e.g. c,d,d#,f,g#
#   these will be the notes that the GA can use
#   leave empty or as "all" to use all notes
"""
& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py midi/user_test/Chopin_Nocturnes_Op9_No.2_EbMajor_alt.mid 32 100 10 0.75 0.5 0 d#,f,g,g#,a#,c,d
& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py midi/user_test/Free_Bird_Lynyrd_Skynyrd_solo_full.mid 32 100 10 0.75 0.5 0 c,d,f,g,a#
& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py midi/user_test/Free_Bird_Lynyrd_Skynyrd_solo_short.mid 32 100 10 0.75 0.5 0 c,d,f,g,a#
& G:/Uni_Gitlab/Year3/cm3203/mVenv/Scripts/python.exe g:/Uni_Gitlab/Year3/cm3203/ga.py midi/user_test/maryHadLamb.mid 32 100 10 0.75 0.5 0 c,d,e,g
"""
(inputMidiPath, popSize, numGens, numOut, crossoverProb, mutationProb, allowedPitches) = argsParser.parseArgs(argv)

inputEmb = gaf.getEmbeddingFile(inputMidiPath)

md = gaf.getMetadata(inputMidiPath)
tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]
#print(tsNumerator)
#print(tsDenominator)
#print(bpm)


#tsUpper = 3, tsLower = 4 is a time signiture of 3/4

bars = gaf.getRandomStartGen(popSize, allowedPitches)

# for each whole int in expInd, that bar gets a slot. e.g. 2.5 would be 2 slots with a 0.5 chance of a 3rd
# any with 0 slots are eliminated, any with 1 stay and any with more get multiple slots
i = 0

outputBars = []

for i in range(numOut):
    outputBars.append(gac.bar())

for i in range(numGens):
    parentBars = gaf.getParents(bars, popSize, inputEmb, tsNumerator, tsDenominator, bpm)
    f = gaf.getGenFittest(parentBars)
    print("")
    print(f"gen {i+1}")
    print(f"fittest chromosome fitness: {f.fitness}")

    outputBars = gaf.getFittest(bars, outputBars, numOut)

    bars = gaf.crossover(parentBars, tsNumerator, mutationProb, crossoverProb, allowedPitches)

    cumBarLen = 0
    for j in range(len(bars)):
        cumBarLen += len(bars[j].notes)
    

    print(f"average bar length of this gen = {cumBarLen / len(bars)}")

for bar in outputBars:
    gaf.renderMidi(bar, tsNumerator, tsDenominator, name=f"user_test/gen_outputs/{round(bar.fitness, 4)}")