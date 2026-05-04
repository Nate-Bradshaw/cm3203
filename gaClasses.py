# contains the bar and note class for use as chromosomes

class note:
    def __init__(self, pitchIn, startIn):
        # value of -1 reserved for rests for implimentation in future
        # pitches as list to allow chords in future
        self.pitches = []
        if(type(pitchIn) == list):
            self.pitches = pitchIn
        else:
            self.pitches.append(pitchIn) #* -1 would be a rest
        self.start = startIn

class bar: #single track bar
    notes = [] # notes should be kept in order
    fitness = 0 #simularity score, 0 is no relation, 1 is identical
    ei = 0 #expected individuals in next pop
    srs = -1 # doesnt seem to do anything, too late in the project remove it and break something
    def __init__(self):
        self.notes = []

    def addNote(self, note, index = -1):
        if(index == -1):
            self.notes.append(note)
        else:
            if(index > len(self.notes)):
                print(f"index {index} out of range for notes, note not added")
            else:
                self.notes.insert(index, note)
    
    def printNotes(self):
        outstr = ""
        for i  in range(len(self.notes)):
            outstr += f"[note: {i}, pitch: {self.notes[i].pitches[0]}, start: {self.notes[i].start}], "
        print(outstr)
        return outstr
    
    def copyBarNotes(self, barIn):
        #this doesnt include ei or fitness
        notesIn = barIn.notes

        self.notes = []

        for n in notesIn:
            self.notes.append(note(n.pitches, n.start))