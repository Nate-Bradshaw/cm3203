import mido
from mido import MidiFile, MidiTrack, Message

# Create a new MIDI file
mid = MidiFile()

# Create a track and add it to the file
piano_track = MidiTrack()
bass_track  = MidiTrack()
mid.tracks.append(piano_track)
mid.tracks.append(bass_track)

#! microseconds per tick = microseconds per quarter note / ticks per quarter note

# Set the tempo (microseconds per beat, default is 500000 = 120 BPM)
piano_track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))

# Set the instrument (program_change: 0 = Acoustic Grand Piano)
piano_track.append(Message('program_change', program=0, time=0))

# Add notes: note_on starts a note, note_off stops it
# note = MIDI note number (60 = Middle C)
# velocity = how hard the note is played (0-127)
# time = ticks since last message (480 ticks = 1 beat at default resolution)

piano_track.append(Message('note_on',  note=21, velocity=64, time=0))    # C4
#piano_track.append(Message('note_on',  note=62, velocity=64, time=0))  
#piano_track.append(Message('note_on',  note=64, velocity=64, time=0)) 
piano_track.append(Message('note_off', note=21, velocity=64, time=480))   # hold for 1 beat

##piano_track.append(Message('note_on',  note=62, velocity=64, time=0))     # D4
##piano_track.append(Message('note_off', note=62, velocity=64, time=480))
##
##piano_track.append(Message('note_on',  note=64, velocity=64, time=0))     # E4
##piano_track.append(Message('note_off', note=64, velocity=64, time=480))
##
### Sand the same for a bass track
##bass_track.append(mido.MetaMessage('set_tempo', tempo=500000, time=0))
##
##bass_track.append(Message('program_change', program=4, time=0))
##
##bass_track.append(Message('note_on',  note=36, velocity=64, time=0))
##bass_track.append(Message('note_off', note=36, velocity=64, time=480)) 
##
##bass_track.append(Message('note_on',  note=38, velocity=64, time=0))
##bass_track.append(Message('note_off', note=38, velocity=64, time=480))
##
##bass_track.append(Message('note_on',  note=36, velocity=64, time=0))
##bass_track.append(Message('note_off', note=36, velocity=64, time=480))

# Save the file
mid.save('output.mid')
print("MIDI file saved!")