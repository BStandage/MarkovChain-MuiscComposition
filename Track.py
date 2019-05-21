from Parse import Parse
from Simulation import Simulation
from mido import MidiFile, Message
from copy import deepcopy

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


    # ADJUST RANGE OVER A SINGLE OCTIVE
    def set_range(self):
        if self.voice == 'soprano':
            return [60, 84]
        elif self.voice == 'alto':
            return [53, 77]
        elif self.voice == 'tenor':
            return [48, 72]
        elif self.voice == 'bass':
            return [40, 64]


    def build_track(self):
        file = Parse('bach_846.mid')
        tpm = file.parse()

        print(tpm)

        simulate = Simulation(tpm, self)
        simulate.next_state(simulate.get_init_note(), self.length)

        #print(self.track)


    def apply_weights(self, tpm):
        for key in tpm:
            for inner_key in tpm[key]:
                tpm[key][inner_key][1] = tpm[key][inner_key][1]*4

        print(tpm)


    #
    def shift_track(self):
        for i in range(0, 16):
            self.track.append([Message('note_on', note=0, velocity=0, time=0),
                Message('note_off', note=0, velocity=0, time=200)])
        for i in range(0, 15):
            shifted_note = track1.track[i][0].note - 20
            self.track.append([Message('note_on', note=shifted_note, velocity=127, time=0),
                Message('note_off', note=shifted_note, velocity=0, time=200)])



    @staticmethod
    def write(track_list, filename):
        mid = MidiFile()
        for track in track_list:
            t = mid.add_track(track.name)

            for message in track.track:
                t.append(message[0])
                t.append(message[1])


        mid.save(filename)

if __name__ == '__main__':

    # build track with title, 'voice 1', voice: 'soprano' and length 100
    track1 = Track('voice 1', 'soprano', 32)
    track1.build_track()


    #track2 = Track('voice 2', 'alto', 100)
    #track2.build_track()
    #track2.shift_track()


    track_list = [track1]

    print(track1.write(track_list, 'testTrack1.2.mid'))
    print('Complete!')


    # start track 2 after track 1 completes subject and counter subject
    # set the next n tracks to have the subject and counter subject of the first
    # delay each track to begin at the end of the counter subject of the previous track
    # shift the additional tracks to a certain degree (up a 5th for example)
