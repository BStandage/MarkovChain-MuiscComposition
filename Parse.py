from mido import MidiFile
import itertools


class Parse:

    def __init__(self, filename):
        self.filename = filename
        self.tempo = None
        self.tpm = {}


    def parse(self):
        midi = MidiFile(self.filename)

        current_state = []
        prev_state = []

        for track in midi.tracks:
            for message in track:
                if message.type == "set_tempo":
                    self.tempo = message.tempo
                elif message.type == "note_on":
                    # note is played at the same time
                    if message.time == 0:
                        current_state.append(message.note)
                    # if the note is not played at the same time, then it is the next state from the previous state
                    # This means we must permute all possible transitions from notes in the previous state to notes
                    # in the current state and add them to the markov chain
                    else:
                        d = self.duration(message.time, midi.ticks_per_beat)
                        self.permute_transitions(prev_state, current_state, d)
                        prev_state = current_state
                        current_state = []

        return(self.to_probability_matrix())


    def permute_transitions(self, prev_state, current_state, duration):
        for x in list(itertools.product(prev_state, current_state)):
            # add x[0]:{x[1]: [time, count]} to the Markov Chain
            if x[0] not in self.tpm:
                self.tpm[x[0]] = {}
                self.tpm[x[0]][x[1]] = [duration, 1]

            # if the note has already been transitioned to, increase the transition count by 1
            # if the key is in the dict and the value is == dict[key]
            elif x[1] in self.tpm[x[0]] and self.tpm[x[0]][x[1]][0] == duration:
                self.tpm[x[0]][x[1]] = [duration, self.tpm[x[0]][x[1]][1] + 1]

            # if the note has not been transitioned to, add it to the dictionary with a count of 1
            else:
                self.tpm[x[0]][x[1]] = [duration, 1]


    # bucket to nearest 50ms
    def duration(self, ticks, tpb):
        ms = (ticks / tpb * self.tempo) / 1000
        return int(ms - (ms % 50) + 50)


    # convert a transition frequency matrix to a transition probability matrix
    def to_probability_matrix(self):
        total = 0
        transitions = 0

        for keys in self.tpm:
            for inner_keys in self.tpm[keys]:
                total += self.tpm[keys][inner_keys][1]
                transitions += 1
            for inner_keys in self.tpm[keys]:
                self.tpm[keys][inner_keys][1] /= total
            total = 0
            transitions = 0

        return (self.tpm)


if __name__ == '__main__':
    file = Parse('bach_846.mid')
    print(file.parse())