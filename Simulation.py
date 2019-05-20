from mido import MidiFile, MidiTrack, Message
import numpy as np



class Simulation:


    # Simulation Constructor
    def __init__(self, tpm, track):
        self.tpm = tpm
        self.track = track
        self.messages = []
        self.initial_note = self.get_init_note()
        self.state_space = self.state_space()


    # Function: to_midi_message
    # accept: a note and it's duration
    # return: a midi message
    # CHANGED DURATION TO 200ms
    def to_midi_message(self, n, d):
        return [Message('note_on', note=n, velocity=127, time=0),
                Message('note_off', note=n, velocity=0, time=200)]


    # We want to randomly begin the piece on the 1 or the 5
    # *NOT IMPLEMENTED*
    # Function: get_init_note
    # accept: self
    # return: initial note given a track simulation object
    def get_init_note(self):
        return [60]


    # Transition function simulations transition given current state
    # Function: transition
    # accept: a note
    # return: the most likely next note given the initial note
    def transition(self, note):
        transition_probabilities = []
        keys = []

        for i in self.tpm[note]:
            transition_probabilities.append(self.tpm[note][i][1])
            keys.append([i, self.tpm[note][i][0]])

        print(note)

        return keys[np.random.choice(len(keys), p=transition_probabilities)]


    # Recursively find the most probable transition note and fill the track
    # Function: next_state
    # accept: a note and a number of notes
    # return:
    # MUST CHANGE BASE CASE: Check if the length of the piece is n notes long
    # once it is, check for a resolving note and end the piece
    def next_state(self, initial_note, l):
        if l > 0:
            while True:
                next = self.transition(initial_note[0])
                difference = abs(initial_note[0] - next[0])
                # if there's a leap...
                if len(self.track.track) == 1 and difference > 2:
                    next[0] = initial_note[0] + 2
                    print('Added via Leap: ', next[0])
                    break
                elif len(self.track.track) > 1 and abs(self.track.track[len(self.track.track) - 2][0].note - initial_note[0]) > 2:
                    next[0] = self.leap_rule()
                    print('Added via Leap: ', next[0])
                    break
                # if not then generate most probable
                # *BUG* Generally these requirements are too strict and no note in the state space can be generated
                # Potential Fixes: 1. Build the transition probability matrix over notes only in the state space + 12n
                # 2. Force a next note if after too many tries (could cause overfitting)
                # 3. Keep the transition probability matrix as is, but increase each voices state space to two octaves
                elif self.not_trill(next[0]) and next[0] in self.state_space:
                    print('Added note: ', next[0])
                    break
                print('Failed Note: ', next[0])
                print('Why?:')
                print('No Trill?: ', self.not_trill(next[0]))
                print('In state space?: ', (next[0] in self.state_space))

            self.track.track.append(self.to_midi_message(next[0], next[1]))
            l -= 1
            self.next_state(next, l)
        else:
            return self.messages


    # accept: the most recently generated note
    # return: True if this note does not create a trill, False otherwise
    def not_trill(self, n):
        l = len(self.track.track)

        if l > 3:
            if (self.track.track[l - 1][0].note == self.track.track[l - 3][0].note
                and abs(self.track.track[l - 2][0].note - self.track.track[l - 1][0].note) == 1) and \
                            self.track.track[l - 2][0].note == n:
                return False
            else:
                return True
        else:
            return True


    # If a leap exists (a jump in MIDI notes greater than 2) then the next note must be a step
    # in the opposite direction.
    def leap_rule(self):
        l = len(self.track.track)

        leap_size = self.track.track[l - 2][0].note - self.track.track[l - 1][0].note

        if leap_size > 2:
            if self.track.track[l - 1][0].note - 2 in self.state_space:
                next = self.track.track[l - 1][0].note - 2
            else:
                next = self.track.track[l - 1][0].note - 1
        elif leap_size < -2:
            if self.track.track[l - 1][0].note + 2 in self.state_space:
                next = self.track.track[l - 1][0].note + 2
            else:
                next = self.track.track[l - 1][0].note + 1

        return next


    # Define a statespace for the track. This state space is normalized over the C major scale
    def state_space(self):
        state_space = []
        complement = [1, 3, 6, 8, 10]
        for i in range(13):
            if i not in complement:
                state_space.append(self.initial_note[0] + i)

        for i in range(1, len(state_space)):
            state_space.append(state_space[i] + 12)

        print(state_space)
        return state_space






if __name__ == '__main__':


    # Simulation object
    #simulate = Simulation(tpm, first_voice)
    #print(simulate.next_state([78, 50], 100))
    #print(simulate.messages)



    # CREATE A NEW CLASS TO BUILD CONVERT INTO MIDI FILE
    mid = MidiFile()
    track = mid.add_track("test")
    #mid.tracks.append(track)
    #for i in simulate.messages:
     #   track.append(i[0])
      #  track.append(i[1])


    print(mid)

    mid.save('test.mid')







## Consider making histograms transitions in every key, then normalize and compare
