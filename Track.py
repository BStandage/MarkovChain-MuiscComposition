from Parse import Parse
from Simulation import Simulation
from mido import MidiFile, Message, MidiTrack
import subprocess

class Track:


    # What characteristics does a track have?
    # - a list of messages in the track
    # - a name for the track
    # - a set of contraints based on the voice
    def __init__(self, name, voice, length):
        self.track = []
        self.name = name
        self.voice = voice
        self.length = length
        self.range = self.set_range()


    # Function: set_range
    # accept: self
    # return: A range of MIDI values for a given voice
    def set_range(self):
        if self.voice == 'soprano':
            return [60, 84]
        elif self.voice == 'alto':
            return [53, 77]
        elif self.voice == 'tenor':
            return [48, 72]
        elif self.voice == 'bass':
            return [40, 64]

    # Function: build_track
    # accept: self
    # return: None
    def build_track(self):
        file = Parse('bach_846.mid')
        #file = Parse('WTC_Part1/Fugue7.mid')
        tpm = file.parse()

        simulate = Simulation(tpm, self)
        simulate.next_state(simulate.get_init_note(), self.length)

    # shifts track in pitch, and the start time
    # consider shifting track so that the begining note always starts on the 1 of the next measure
    # if end time mod whole note != 0 then we need to put in rests so that the next voice does not begin in the middle
    # of a measure. Probably okay to begin at half measure too.
    def shift_track(self, t, s):
        self.track.append([Message('note_on', note=1, velocity=0, time=0), Message('note_off', note=1, velocity=0, time=t*(s-1))])
        for i in range(len(track1.track)):
            shifted_note = track1.track[i][0].note - 7*(s-1)
            self.track.append([Message('note_on', note=shifted_note, velocity=127, time=0),
                Message('note_off', note=shifted_note, velocity=0, time=track1.track[i][1].time)])



    @staticmethod
    # Function: write
    # accept: A list of tracks for each voice
    # return: a MIDI file
    def write(track_list, filename):
        mid = MidiFile()
        for track in track_list:
            t = mid.add_track(track.name)

            for message in track.track:
                t.append(message[0])
                t.append(message[1])

        new_mid = MidiFile()

        for track in mid.tracks:
            new_track = MidiTrack()
            new_mid.tracks.append(new_track)
            for msg in track:
                if msg.type == 'set_tempo':
                    msg.tempo = 250000

                new_track.append(msg)
        new_mid.save(filename)

if __name__ == '__main__':

    # build track with title, 'voice 1', voice: 'soprano' and length 100
    track1 = Track('voice 1', 'soprano', 16)
    track1.build_track()

    # print the total time of the track
    time = 0
    for i in track1.track:
        time += i[1].time

    cs = Track('cs', 'soprano', 12)
    cs.track.append(
        [Message('note_on', note=1, velocity=0, time=0), Message('note_off', note=1, velocity=0, time=time)])
    for i in range(len(track1.track)-1, 1, -1):
        shifted_note = track1.track[i][0].note
        cs.track.append([Message('note_on', note=shifted_note, velocity=127, time=0),
                           Message('note_off', note=shifted_note, velocity=0, time=track1.track[i][1].time)])




    track2 = Track('voice 2', 'alto', 32)
    #track2.build_track()
    track2.shift_track(time, 2)

    cs2 = Track('cs', 'soprano', 8)
    cs2.track.append(
        [Message('note_on', note=1, velocity=0, time=0), Message('note_off', note=1, velocity=0, time=time*2)])
    for i in range(len(track2.track) - 1, 1, -1):
        shifted_note = track2.track[i][0].note
        cs2.track.append([Message('note_on', note=shifted_note, velocity=127, time=0),
                          Message('note_off', note=shifted_note, velocity=0, time=track2.track[i][1].time)])

    track3 = Track('voice 3', 'tenor', 32)
    # track2.build_track()
    track3.shift_track(time, 3)

    track_list = [track1, track2, track3, cs, cs2]

    midifile = track1.write(track_list, 'testTrack12.mid')
    print('Complete!')
    print("FIRST NOTE: ", str(track1.track[0]))

    # This calls a script I wrote to automatically play midi files via the terminal
    subprocess.call(['playmidi /Users/audreystandage/PycharmProjects/MarkovChain-MusicComposition/testTrack12.mid'], shell=True)
