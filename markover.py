import random
import sys
import math

class Markov(object):

    def __init__(self, open_file, ngram_size):
        self.ngram_size = ngram_size
        self.cache = {}
        self.open_file = open(open_file, 'r')
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.total_trans = self.word_size - 1 # the total number of transitions in the database will be word_size - 1 at this point
        self.database(ngram_size)

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        #data = data.lower()
        words = data.split()
        return words

    def quints(self, ngr):
        """ Generates ngrams from the given data string. So if our string were
        "What a lovely day", we'd generate (What, a, lovely) and then
        (a, lovely, day) and if longer so on and so forth
        """

        if len(self.words) < ngr:
            return
        for i in range(len(self.words) - ngr + 1):
            l = []
            for j in range(ngr):
                l.append(self.words[j+i])
            yield tuple(l)

    def database(self, ngram):
        for l in self.quints(ngram):
            key = l[:-1]
            if key in self.cache:
                self.cache[key].append(l[-1])
            else:
                self.cache[key] = [l[-1]]
    
    def score_text(self, text):
        score = 0.0
        trans_made = 0.0
        #make sure text has at least one element
        text=text.split()

        for idx, t in enumerate(text):
            words = text[0 + idx:self.ngram_size + idx] # the whole markov chain. E.g The, boy, is for a 3 len chain
            key = words[:-1] # the key for the dictionaty. E.G. the, boy for a 3 chain
            prob = 0.0
            val = [] # the values that correspond with the key
            try:
                count = 0 # figure out how many occourances of the value are in the cache. Score accordingly
                possible_transistions = 0.0
                val = self.cache[tuple(key)]
                for i in val:
                    possible_transistions += 1
                    if i == words[-1]:
                        count += 1
                prob = count / possible_transistions # the probability that a transition should happen is the # of times it does / the total possible transitions
            except KeyError:
                prob = 0 # no score, words never seen before
            score += prob
            trans_made +=1
        return score / (trans_made or 1)  # dont divide by zero so fear robot devil


    def generate_markov_text(self, size=25):
        ran_key = random.choice(self.cache.keys())
        words = list(ran_key)
        words.append('')  # the last element is the value
        gen_words = []
        for i in words[:-1]:
            gen_words.append(i)  # append the initial key

        for i in xrange(size):
            key = []
            for i in words[:-1]:
                key.append(i)
            key = tuple(key)
            words[-1] = random.choice(self.cache[key])
            gen_words.append(words[-1])  ## append new random word to output
            for i in range(len(words) - 1):  ## move it all on over
                words[i] = words[i+1]
        return ' '.join(gen_words)

    def unitTest(self):
        self.score_text("The licenses for most software are designed to take away your freedom to share and change it.  By contrast, the GNU General Public")
