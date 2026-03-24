class note:
    def __init__(self, pitchIn, durationIn):
        #on pitch, may impliment rests as a value such as -1 or smthn
        self.pitch = pitchIn #* a pitch of 20 or lower is converted into a rest (-1), means the odd of a rest can be increased
        if self.pitch <= 20:
            self.pitch = -1
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