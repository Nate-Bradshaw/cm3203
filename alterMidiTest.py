from mido import MidiFile, Message, MetaMessage

mid = MidiFile('Untitled_15.mid', clip=True)
track = mid.tracks[0]

# Find the end_of_track position
eot_index = next(
    (i for i, msg in enumerate(track) if msg.type == 'end_of_track'),
    None
)

new_notes = [
    Message('note_on',  note=60, velocity=64, time=0),
    Message('note_off', note=60, velocity=64, time=480),
    Message('note_on',  note=64, velocity=64, time=0),
    Message('note_off', note=64, velocity=64, time=480),
]

if eot_index is not None:
    for i, msg in enumerate(new_notes):
        track.insert(eot_index + i, msg)
else:
    for msg in new_notes:
        track.append(msg)

mid.save('Untitled_15_edited.mid')