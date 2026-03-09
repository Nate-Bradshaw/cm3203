from mido import MidiFile

mid = MidiFile('Untitled_15.mid', clip=True)
print(mid)

#for track in mid.tracks[0]:
#    print("="*15)
#    print(track)
#