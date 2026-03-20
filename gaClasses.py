from mido import MidiFile, MidiTrack, Message, MetaMessage
from io import BytesIO
import random as rand

class note:
    def __init__(self, pitchIn, durationIn):
        #on pitch, may impliment rests as a value such as -1 or smthn
        self.pitch = pitchIn #TODO: restrict between 21 to 108 (piano) or to 127 (named notes)
        #duration in (usually, some time sigs it may be an 1/8th or 1/2th) quarter notes
        self.duration = durationIn

class bar: #single track bar
    notes = [] #! notes need to be kept in time order
    fitness = 0 #simularity score, 0 is no relation, 1 is identical, looking for a 0.9ish?
    ei = 0 #expected individuals in next pop
    srs = -1
    def __init__(self):
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

    def getNoteBeat(self, noteIndex):
        if(noteIndex < len(self.notes)):
            cumBeat = 1
            for i in range(noteIndex):
                cumBeat += self.notes[i].duration
            return cumBeat
        else:
            print(f"getNoteBeat {noteIndex} is out of range for length {len(self.notes)}")
            return -1

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


def crossover(bar1 = bar(), bar2 = bar(), tsN = 4):
    #* indexing from 1 where 1 is the starting beat in the bar
    cBar1 = bar()
    cBar2 = bar()

    #initial, picking the beat
    coBeat = rand.randint(1,tsN)

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

    #! TEMP
    coBeat = 2.25

    #second bar in a crossover overides the first one
    cumBeats = 1
    for i in range(len(bar1.notes)):
        if(cumBeats >= coBeat):
            #go back and clip the end of last note
            if(len(cBar1.notes) > 1):
                cBar1.notes[len(cBar1.notes)-1].duration = coBeat - cBar1.getNoteBeat(i-1)
            break
        else:
            cumBeats += bar1.notes[i].duration
            cBar1.addNote(note(bar1.notes[i].pitch, bar1.notes[i].duration))
    cumBeats = 1
    for i in range(len(bar2.notes)):
        if(cumBeats < coBeat):
            cumBeats += bar2.notes[i].duration
            if(cumBeats > coBeat):
                cBar1.addNote(note(bar2.notes[i].pitch, (bar2.getNoteBeat(i) + bar2.notes[i].duration) - (cBar1.getNoteBeat(len(cBar1.notes)-1) + cBar1.notes[len(cBar1.notes)-1].duration)))
        else:
            cBar1.addNote(note(bar2.notes[i].pitch, bar2.notes[i].duration))
    
    return cBar1
    

def renderMidi(barIn, tsN, tsD, bpm = 120, ppq = 480, createFile = True, name = "output"):
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

    for note in barIn.notes:
        pianoTrack.append(Message('note_on',  note=note.pitch, velocity=64, time=0))
        pianoTrack.append(Message('note_off', note=note.pitch, velocity=64, time=int(ppq*note.duration)))
    
    if(createFile):
        mid.save(f'midi/{name}.mid')
        print("MIDI file saved!")
    else:
        buf = BytesIO()
        mid.save(file=buf)
        return buf.getvalue()