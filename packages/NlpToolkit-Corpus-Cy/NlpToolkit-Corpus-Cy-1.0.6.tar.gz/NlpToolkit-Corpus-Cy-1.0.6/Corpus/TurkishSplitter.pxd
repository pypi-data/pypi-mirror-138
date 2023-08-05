from Corpus.SentenceSplitter cimport SentenceSplitter


cdef class TurkishSplitter(SentenceSplitter):

    cpdef str upperCaseLetters(self)
    cpdef str lowerCaseLetters(self)
    cpdef list shortCuts(self)
