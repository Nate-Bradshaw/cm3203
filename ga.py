import random as rand
from math import floor
from sys import argv, exit
import atexit

import csv
import time

import gaClasses as gac
import gaFunctions as gaf
import argsParser

#usage:
# /ga.py filePath.mid popSize numGens numOut crossoverProb mutationProb octaveRange notes
# filePath.mid 
# popSize, population size (int: positive, even. max 1024) default: 32
# numGens, number of generations (int: positive) default: 100
# numOut, top n individuals to be outputted (int: nonzero, positive) default: 10
# CrossoverProb, probability of a crossover occuring for a pair of chromosomes (float: 0-1) default: 0.7
# MutationProb, probability of a mutation occuring for a chromosome (float: 0-1) default: 0.5
# octaveRange, range of notes included each side of the input MIDI's note range (int: 1 to 11) default: 1
#   11 would allow for all MIDI pitches
# notes(list of notes sepperated by (use # to indicate black keys on a keyboard) "," e.g. c,d,d#,f,g#
#   these will be the notes that the GA can use within the octave range, e.g. if only "c" is selected, only c notes will be included
#   leave empty or as "all" to use all notes

"""
below are the arguments used with the usability survey
/ga.py midi/Chopin_Nocturnes_Op9_No.2_EbMajor_alt.mid 32 100 10 0.75 0.5 0 d#,f,g,g#,a#,c,d
/ga.py midi/Chopin_Nocturnes_Op9_No.2_EbMajor_alt.mid 32 100 10 0.75 0.5 0
/ga.py midi/Free_Bird_Lynyrd_Skynyrd_solo_short.mid 32 100 10 0.75 0.5 0 c,d,f,g,a#
/ga.py midi/Free_Bird_Lynyrd_Skynyrd_solo_short.mid 32 100 10 0.75 0.5 0
/ga.py midi/maryHadLamb.mid 32 100 10 0.75 0.5 0 c,d,e,g
/ga.py midi/maryHadLamb.mid 32 100 10 0.75 0.5 0
"""
(inputMidiPath, popSize, numGens, numOut, crossoverProb, mutationProb, allowedPitches) = argsParser.parseArgs(argv)

inputEmb = gaf.getEmbeddingFile(inputMidiPath)

md = gaf.getMetadata(inputMidiPath)
tsNumerator = md[0]
tsDenominator = md[1]
bpm = md[2]

bars = gaf.getRandomStartGen(popSize, allowedPitches)

outputBars = []

outFitness = []
outTime = []

for i in range(numOut):
    outputBars.append(gac.bar())

# making sure that the results of the genetic algorithm are saved
def saveBars():
    for bar in outputBars:
        gaf.renderMidi(bar, tsNumerator, tsDenominator, name=f"results/{round(bar.fitness, 4)}")
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(outFitness)
        writer.writerow(outTime)
atexit.register(saveBars)

for i in range(numGens):
    start = time.time()
    (sumFitness, parentBars) = gaf.getParents(bars, popSize, inputEmb, tsNumerator, tsDenominator, bpm)
    f = gaf.getGenFittest(parentBars)
    print("")
    print(f"gen {i+1}")
    print(f"sum fitness: {sumFitness}")
    print(f"avr fitness: {sumFitness/popSize}")
    outFitness.append(sumFitness/popSize)
    print(f"fittest chromosome fitness: {f.fitness}")

    outputBars = gaf.getFittest(bars, outputBars, numOut)

    bars = gaf.crossover(parentBars, tsNumerator, mutationProb, crossoverProb, allowedPitches)

    cumBarLen = 0
    for j in range(len(bars)):
        cumBarLen += len(bars[j].notes)
    
    print(f"average bar length of this gen = {cumBarLen / len(bars)}")
    outTime.append(time.time() - start)
