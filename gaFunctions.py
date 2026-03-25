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

def crossover(barsIn, tsN, mutationProb):
    barsOut = []

    for i in range(len(barsIn)//2):
        #initial, picking the beat
        coBeat = rand.randint(1,tsN)
        bar1 = barsIn.pop(rand.randint(0, len(barsIn)-1))
        bar2 = barsIn.pop(rand.randint(0, len(barsIn)-1))

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
    cBar = gac.bar()

    #second bar in a crossover overides the first one
    cumBeats = 1
    for i in range(len(bar1.notes)+1):
        if(cumBeats > coBeat):
            #go back and clip the end of last note
            cBar.notes[len(cBar.notes)-1].duration = coBeat - cBar.getNoteBeat(i-1)
            break
        else:
            #go to beat at end of next note
            cumBeats += bar1.notes[i].duration
            cBar.addNote(gac.note(bar1.notes[i].pitch, bar1.notes[i].duration))

    cumBeats = 1
    for i in range(len(bar2.notes)):
        if(cumBeats < coBeat):
            cumBeats += bar2.notes[i].duration
            if(cumBeats > coBeat):
                #clipping the note
                cBar.addNote(gac.note(bar2.notes[i].pitch, (bar2.getNoteBeat(i) + bar2.notes[i].duration) - (cBar.getNoteBeat(len(cBar.notes)-1) + cBar.notes[len(cBar.notes)-1].duration)))
        else:
            cBar.addNote(gac.note(bar2.notes[i].pitch, bar2.notes[i].duration))
    
    return cBar

def mutate(barIn):
    #alters a bar object in place
    #so what does mutate do?
    #take a note, change it
    #pick note, take note after it, merge into first note
    if(len(barIn.notes) > 1):
        i = rand.randint(0, len(barIn.notes)-2)
        pitch = rand.randint(20, 108)
        barIn.notes[i].duration += barIn.notes.pop(i+1).duration
        barIn.notes[i].pitch = pitch

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

    t = 0
    #TODO: a rest at the end of a bar isnt rendered
    for note in barIn.notes:
        if note.pitch == -1:
            t += int(ppq*note.duration)
        else:
            pianoTrack.append(Message('note_on',  note=note.pitch, velocity=64, time=t))
            pianoTrack.append(Message('note_off', note=note.pitch, velocity=64, time=int(ppq*note.duration)))
            if(int(ppq*note.duration) == 0):
                print("note dur of 0")
            t = 0
    
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