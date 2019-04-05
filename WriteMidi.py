from mido import MidiFile, MidiTrack, Message


class WriteMidi:

    def __init__(self, tracks):
        self.tracks = tracks


    def write(self):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        # keep memory of which voice
        i = 0


