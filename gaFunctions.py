from math import floor

import midisim
from mido import MidiFile, MidiTrack, Message, MetaMessage
from io import BytesIO
import random as rand
import gaClasses as gac

midismVerbose = False

#pre downloaded embedding and model
emb_path = './midisim-embeddings\discover_midi_dataset_37292_genres_midis_embeddings_cc_by_nc_sa.npy'
model_path = './midisim-models/midisim_small_pre_trained_model_2_epochs_43117_steps_0.3148_loss_0.9229_acc.pth'

#embedings
corpus_midi_names, corpus_emb = midisim.load_embeddings(emb_path, verbose=midismVerbose)

#midisim model
model, ctx, dtype = midisim.load_model(model_path, verbose=midismVerbose)

def getEmbeddingFile(path):
    input_toks_seqs = midisim.midi_to_tokens(path, verbose=midismVerbose)
    return midisim.get_embeddings_bf16(model, input_toks_seqs, verbose=midismVerbose)

#MIDI data in a buffer
def getEmbeddingBuf(buf):
    input_toks_seqs = midisim.midi_to_tokens(buf, verbose=midismVerbose)
    return midisim.get_embeddings_bf16(model, input_toks_seqs, verbose=midismVerbose, show_progress_bar=midismVerbose)

def compareEmbeddings(emb1, emb2):
    #comparing emb2's simularity to emb1
    best_idx, best_vals = midisim.cosine_similarity_topk(emb1, emb2, verbose=midismVerbose)
    similarity_score = best_vals[0][0]  # scalar float
    return similarity_score
    #print(f"Similarity: {similarity_score:.4f}")

"""
score = 1: exact match
score > 0.85: very similar
score > 0.6: moderately similar
score > 0.3: loosely similar
otherwise dissimilar
"""

# Stochastic remainder selection
def getParents(barsIn, popSizeIn, inputEmb, tsN, tsD, bpm):
    nextBars = []
    eiFractionSum = 0

    sumFitness = 0

    for i in range(popSizeIn):
        similarityScore = compareEmbeddings(inputEmb, getEmbeddingBuf(renderMidi(barsIn[i], tsN, tsD, bpm, createFile=False)))
        barsIn[i].fitness = similarityScore
        sumFitness += similarityScore

    print(f"sum fitness: {sumFitness}")
    print(f"avr fitness: {sumFitness/popSizeIn}")

    for i in range(popSizeIn):
        #amount to be included guarenteed in next generation
        #https://datajobstest.com/data-science-repo/Genetic-Algorithm-Guide-[Tom-Mathew].pdf 2.7
        #expected individuals
        barsIn[i].ei = (barsIn[i].fitness / sumFitness) * popSizeIn
        n = floor(barsIn[i].ei)
        eiFractionSum += barsIn[i].ei-n
        #print(f"bar {i} with ei {barsIn[i].ei} evaluated")
        for j in range(n):
            #print(f"bar {i} with ei {barsIn[i].ei} added to next gen")
            nextBars.append(barsIn[i])

    # ei fractional / sum of fractional = normalised prob between 0-1
    # then find how many slots are left, sl
    # get a random number between 0-1, get values ei(n) < r <= ei(n+1), same for r + 1/sl % 1
    slotsLeft = popSizeIn - len(nextBars)
    #print(f"slots left = {slotsLeft} from {popSizeIn} - {len(nextBars)}")
    r = rand.random()
    eiNormSum = 0
    for i in range(slotsLeft):
        pointer = (r + (1 / slotsLeft) * i) % 1
        eiNormSum = 0
        selected = barsIn[-1]  # fallback: last bar covers any floating point gap near 1.0
        for j in range(popSizeIn):
            eiNormSum += (barsIn[j].ei - floor(barsIn[j].ei)) / eiFractionSum
            if eiNormSum > pointer:
                selected = barsIn[j]
                break
        nextBars.append(selected)

    print(f"new gen size: {len(nextBars)}")
    #fittest chromosomes will stay at the start of the new list, as they had a ei of 1 or higher
    #! although if ei is 2 or higher, there will duplicate genes, cossover of these genes would do nothing so there should be some randomness

    return nextBars

def getFittest(barsIn):
    #assumes the bars have already been compared to embedings
    fi = 0
    for i in range(len(barsIn)):
        if(barsIn[i].fitness > barsIn[fi].fitness):
            fi = i
    return barsIn[fi]

def crossover(barsIn, tsN, mutationProb):
    barsOut = []

    for i in range(len(barsIn)//2):
        #initial, picking the beat
        coBeat = rand.randint(1,tsN)
        bar1 = barsIn.pop(rand.randint(0, len(barsIn)-1))
        bar2 = barsIn.pop(rand.randint(0, len(barsIn)-1))

        while(coBeat == 1):
            subdiv = 0.5
            #* limiting to 1/64th notes
            for j in range(4):
                r = rand.random()
                #2/4 chance of terminating and keeping the current split position
                if(r < 0.5):
                    break
                #1/4 of going down a level at the increment forward
                elif(r < 0.75):
                    coBeat += subdiv
                #1/4 of going down a level at an current position
                subdiv /= 2

        print(f"crossover at {coBeat}")

        crBar = cr(bar1, bar2, coBeat)        
        if rand.random() <= mutationProb:
            mutate(crBar)       
        barsOut.append(crBar)

        crBar = cr(bar2, bar1, coBeat)     
        if rand.random() <= mutationProb:
            mutate(crBar)       
        barsOut.append(crBar)
    
    return barsOut

def cr(bar1, bar2, coBeat):
    #* beats are indexing from 1 where 1 is the starting beat in the bar
    outBar = gac.bar()
    bar1.copyBarNotes(bar1)
    bar2.copyBarNotes(bar2)

    for i in range(len(bar1.notes)):
        #if a note is before crossover, keep it, otherwise break
        if(bar1.notes[i].start < coBeat):
            outBar.addNote(gac.note(bar1.notes[i].pitches, bar1.notes[i].start))
            #print(f"pre 0, bar1.notes[i].start {bar1.notes[i].start} < coBeat {coBeat}")
        else:
            #print(f"pre 1, pass as note start {bar1.notes[i].start} > coBeat {coBeat}")
            break
    
    passedCo = False
    for i in range(len(bar2.notes)):
        #if a note is before crossover, skip
        #if note comes on or after crossover, add it
        #however, if there is no note at the crossover:
        #   go back to the previous note in the list and move its start to the crossover

        #if a note is before crossover, skip, icl extra check if this is last note in bar
        if(bar2.notes[i].start < coBeat):
            #print(f"0, pass as bar2 note start {bar2.notes[i].start} < coBeat")
            if(i+1 == len(bar2.notes)):
                #if this is the last note in the bar and its less than the co, then set it to the crossover point
                outBar.addNote(gac.note(bar2.notes[i].pitches, coBeat))
                #print(f"0.1, i+1 {i+1} == len(bar2.notes) {len(bar2.notes)}, thus this is only note in bar and must be placed at coBeat")
            #else, there is a note past it, eliminating the possibility that this note could be clipped by the coBeat
        elif(bar2.notes[i].start == coBeat):
            #if the notes start is on the crossover, add it to list with no changes and ingore previous note
            outBar.addNote(gac.note(bar2.notes[i].pitches, bar2.notes[i].start))
            passedCo = True
            #print(f"1, bar2.notes[i].start {bar2.notes[i].start} = coBeat {coBeat} and added as such")
        else:
            #else: note is > coBeat
            #if this is the first note to pass the crossover beat and there is a note behind,
            #move that previous note forward to the crossover point
            #print(f"2, note is > coBeat")

            if(passedCo == False and i != 0):
                passedCo = True
                outBar.addNote(gac.note(bar2.notes[i-1].pitches, coBeat))
                #print(f"2.1, first note to pass cobeat WITH prev note, adding previous note at coBeat")
            elif(not passedCo and i == 0):
                #this case shouldnt happen, as coBeat cannot be 1 and the first note will always be on 1, as rests are coded as "notes"
                #print(f"this case should not be happening")
                passedCo = True
                outBar.addNote(gac.note(bar2.notes[i].pitches, coBeat))
            

            #then add the note that is pass the crossover point
            outBar.addNote(gac.note(bar2.notes[i].pitches, bar2.notes[i].start))
            


    return outBar

#alter bars and notes in place
def mutate(barIn):
    #alters a bar object in place
    #so what does mutate do?
    #take a note, change it
    #pick note, take note after it, merge into first note
    if(len(barIn.notes) > 1):
        i = rand.randint(0, len(barIn.notes)-2)
        pitch = rand.randint(21, 108)
        barIn.notes.pop(i+1)
        barIn.notes[i] = gac.note(pitch, barIn.notes[i].start)

def renderMidi(barIn, tsN, tsD, bpm = 120, ppq = 480, createFile = True, name = "outputFOO"):
    #ppq = pulses per quater or ticks per beat, default is 480
    # therefore 480 ticks is a quater note, 480/2 is 1/8th note ect
    #just rendering as piano for now

    mid = MidiFile(ticks_per_beat=480)
    pianoTrack = MidiTrack()
    mid.tracks.append(pianoTrack)
    # https://stackoverflow.com/questions/61298392/time-signature-meta-message-in-midi
    pianoTrack.append(MetaMessage('time_signature', numerator=tsN, denominator=tsD, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    pianoTrack.append(MetaMessage('set_tempo', tempo=60000000//bpm, time=0)) #60,000,000 microseconds in a min, div by bpm to get ticks(?) for MIDI
    pianoTrack.append(Message('program_change', program=0, time=0))

    
    #TODO: a rest at the end of a bar isnt rendered
    for i in range(len(barIn.notes)-1):
        #? may need altering for chords if the note_ons need to be together?
        for pitch in barIn.notes[i].pitches:
            #print(f"note at {barIn.notes[i].start} with len: {barIn.notes[i+1].start - barIn.notes[i].start}")
            pianoTrack.append(Message('note_on',  note=pitch, velocity=64, time=0))
            pianoTrack.append(Message('note_off', note=pitch, velocity=64, time=int(ppq*(barIn.notes[i+1].start - barIn.notes[i].start))))

    #special case for last note
    for pitch in barIn.notes[len(barIn.notes)-1].pitches:
        #print(f"note at {barIn.notes[len(barIn.notes)-1].start} with len: {(tsN+1) - barIn.notes[len(barIn.notes)-1].start}")
        pianoTrack.append(Message('note_on',  note=pitch, velocity=64, time=0))
        pianoTrack.append(Message('note_off', note=pitch, velocity=64, time=int(ppq*((tsN+1) - barIn.notes[len(barIn.notes)-1].start))))
        

    
    if(createFile):
        mid.save(f'midi/{name}.mid')
        print("MIDI file saved!")
    else:
        buf = BytesIO()
        mid.save(file=buf)
        return buf.getvalue()
    
def getMetadata(midiPath):
    mid = MidiFile(midiPath)
    tsN = -1
    tsD = -1
    bpm = -1
    for msg in mid:
        if msg.is_meta:
            if msg.type == 'time_signature':
                tsN = msg.numerator
                tsD = msg.denominator
            elif msg.type == 'set_tempo':
                bpm = 60_000_000 // msg.tempo
    #TODO: some sort of check so we dont have -1 on any output
    #! also songs that change tempo or time sig?
    return [tsN, tsD, bpm]