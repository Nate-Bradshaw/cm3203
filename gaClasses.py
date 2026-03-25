class note:
    def __init__(self, pitchesIn, startIn):
        #on pitch, may impliment rests as a value such as -1 or smthn
        # PITCHES IS A LIST OF NOTES TO ALLOW CHORDS
        self.pitches = pitchesIn #* a pitch of 20 or lower is converted into a rest (-1), means the odd of a rest can be increased
        if self.pitch <= 20:
            self.pitch = -1
        #duration in (usually, some time sigs it may be an 1/8th or 1/2th) quarter notes
        self.start = startIn

class bar: #single track bar
    notes = [] # notes should be kept in order
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
    
    def printNotes(self):
        outstr = ""
        for i  in range(len(self.notes)):
            outstr += f"[note: {i}, pitch: {self.notes[i].pitch}, duration: {self.notes[i].duration}], "
        print(outstr)
        return outstr