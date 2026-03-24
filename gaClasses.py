from mido import MidiFile

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