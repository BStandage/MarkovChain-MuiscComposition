from mido import MidiFile, MidiTrack, Message


class WriteMidi:

    def __init__(self, track, filename):
        self.track = track
        self.filename = filename


    def write(self):
        mid = MidiFile()
        track = mid.add_track(self.track.name)

        for i in self.track:
           track.append(i[0])
           track.append(i[1])

        mid.save(self.filename)


