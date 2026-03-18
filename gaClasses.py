from mido import MidiFile, MidiTrack, Message, MetaMessage
from io import BytesIO

class note:
    def __init__(self, pitchIn, startIn, durationIn):
        self.pitch = pitchIn #TODO: restrict between 21 to 108 (piano) or to 127 (named notes) 
        self.start = startIn
        self.duration = durationIn

class bar: #single track bar
    notes = [] #! notes need to be kept in time order
    fitness = 0 #simularity score, 0 is no relation, 1 is identical, looking for a 0.9ish?
    srs = -1
    def __init__(self):
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

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
        pianoTrack.append(Message('note_off', note=note.pitch, velocity=64, time=ppq*note.duration))
    
    if(createFile):
        mid.save(f'midi/{name}.mid')
        print("MIDI file saved!")
    else:
        buf = BytesIO()
        mid.save(file=buf)
        return buf.getvalue()