from sys import exit
from os import path
import gaFunctions as gaf

# Contains parsing and defaults for command line arguments

# takes in list of args, returns tuple of values.
def parseArgs(argv):
    if(len(argv) < 2):
        print("mEror, not enough args, please give a file")
        exit()

    if(path.exists(argv[1])): 
        inputMidiPath = argv[1]
        print(f"file {inputMidiPath} used")
    else: 
        print(f"mEror, path {argv[1]} doesnt exist")
        exit()

    if(len(argv) >= 3):
        try:
            popSize = int(argv[2])
            print(f"Population size: {popSize}")
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
            numGens = int(argv[3])
            print(f"Number of generations: {numGens}")
            if(numGens < 1):
                print(f"mEror, number of generations {numGens} given is not positive")
                exit()
        except:
            print(f"mEror, number of generations {argv[3]} is not an int or not entered correctly")
            exit()
    else:
        print("No number of generation given! defaulting to 100")
        numGens = 100

    if(len(argv) >= 5):
        try:
            numOut = int(argv[4])
            print(f"Number of outputs: {numOut}")
            if(numOut < 1):
                print(f"mEror, number of outputs {numOut} given is not positive")
                exit()
        except:
            print(f"mEror, number of outputs {argv[4]} is not an int or not entered correctly")
            exit()
    else:
        print("No number of outputs given! defaulting to 10")
        numOut = 10

    if(len(argv) >= 6):
        try:
            crossoverProb = float(argv[5])
            print(f"Crossover probibility: {crossoverProb}")
            if(crossoverProb > 1 or crossoverProb < 0):
                print(f"mEror, crossover prob {crossoverProb} is out of range 0 to 1")
                exit()
        except:
            print(f"mEror, crossover prob {argv[5]} is not an float or not entered correctly")
            exit()
    else:
        print("No crossover prob given! defaulting to 0.7")
        crossoverProb = 0.7
        
    if(len(argv) >= 7):
        try:
            mutationProb = float(argv[6])
            print(f"Mutation probibility: {crossoverProb}")
            if(mutationProb > 1 or mutationProb < 0):
                print(f"mEror, mutation prob {mutationProb} is out of range 0 to 1")
                exit()
        except:
            print(f"mEror, mutation prob {argv[6]} is not an float or not entered correctly")
            exit()
    else:
        print("No mutation prob given! defaulting to 0.5")
        mutationProb = 0.5

    if(len(argv) >= 8):
        try:
            octaveRange = int(argv[7])
            print(f"Octave range: {octaveRange}")
            if(octaveRange < 1 or octaveRange > 10):
                print(f"mEror, octave range {octaveRange} is out of range 1 to 11")
                exit()
        except:
            print(f"mEror, octave range {argv[7]} is not an int or not entered correctly")
            exit()
    else:
        print("No octave range given! defaulting to 1")
        octaveRange = 1

    # midi 0 is a c (not a named note, but would be c (asumedly))
    # midi 127 is G9
    # middle C is midi 60
    # octaves are 12 notes long

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    allowedNotes = []
    if(argv == "all" or len(argv) < 9):
        print("No notes given! defaulting to all notes allowed")
        allowedNotes = [0,1,2,3,4,5,6,7,8,9,10,11]
    else:
        noteIn = argv[8].split(",")
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
    print(f"nRange: {nRange} with octaveR: {octaveRange}")

    allowedPitches = []

    for p in range(nRange[1]-nRange[0]):
        p += nRange[0]
        if((p%12) in allowedNotes):
            allowedPitches.append(p)

    print(f"Allowed pitches: {allowedPitches}")

    return (inputMidiPath, popSize, numGens, numOut, crossoverProb, mutationProb, allowedPitches)