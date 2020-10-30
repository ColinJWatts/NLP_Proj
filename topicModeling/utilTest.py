import util
import sys

sys.path.append("..\\dataCollection")
from Librarian import Librarian

lib = Librarian()

corpus = util.cleanPunctuationFromAllDocs(lib.getCorpus())
vocab = util.createVocab(corpus)
vocab = util.removeSingletonsFromVocab(vocab, corpus)
lookup = util.createLookup(vocab)

print(len(vocab))