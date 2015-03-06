class WordNet:
    def __init__(self, SynsetFile, HyponymsFile):
        self.idMap = {} # Dictionary mapping id, words, repr(synset) to synsets
        self.wordsMap = {} # Dictionary mapping words to synsets
        self.hyponymsMap = {} # Dictionary mapping hyponyms to synsets

        # Read the SynsetFile and construct idMap, wordsMap
        with open(SynsetFile, 'r') as f:
            for line in f:
                # Splits string and removes whitespace
                line = [word.strip() for word in line.split(',')]
                
                # Synset Values
                SynsetID, SynsetWords, SynsetDef = int(line[0]), line[1].split(), line[2]
                self.idMap[SynsetID] = SynsetWords

                for word in SynsetWords:
                    if word in self.wordsMap:
                        self.wordsMap[word].append(SynsetWords)
                    else:
                        self.wordsMap[word] = [SynsetWords]

        # Read the HyponymsFile and construct hyponymsMap
        with open(HyponymsFile, 'r') as f:
            for line in f:
                # Splits string and removes whitespace
                line = [int(word.strip()) for word in line.split(',')]

                # Hyponym Values
                Hypernym, HyponymIDs = self.idMap[line[0]], line[1:]
                HyponymsList = []
                for HyponymID in HyponymIDs:
                    HyponymsList.append(self.idMap[HyponymID])
                self.hyponymsMap[repr(Hypernym)] = HyponymsList

    # Return True if a noun is a word in some synset
    def isNoun(self, noun):
        return noun in self.wordsMap

    # Return a list of all nouns
    def nouns(self):
        return list(self.wordsMap.keys())

    # Returns a list of all hyponyms and synonyms of WORD
    def hyponyms(self, noun):
        def recursiveHyponym(s):
            hyponymsLst = []
            if repr(s) not in self.hyponymsMap:
                return hyponymsLst
            hyponymsOfS = self.hyponymsMap[repr(s)]
            for hyponym in hyponymsOfS:
                for word in hyponym:
                    hyponymsLst.append(word)
                for word in recursiveHyponym(hyponym):
                    hyponymsLst.append(word)
            return hyponymsLst
        wordsLst = []
        if noun in self.wordsMap:
            synsetsWithWord = self.wordsMap[noun]
        else:
            return noun + " is not in the WordNet database!"
        for synset in synsetsWithWord:
            for word in synset:
                if word not in wordsLst:
                    wordsLst.append(word)
            for word in recursiveHyponym(synset):
                if word not in wordsLst:
                    wordsLst.append(word)
        return wordsLst

# Running the Program
WordNetPy = WordNet('synsets.txt', 'hyponyms.txt')
print("Welcome to WordNetPy, a tool to find the hyponyms of a word!")
while(True):
    inputWord = input('Enter a word for which you want the hyponyms: ')
    if inputWord == "Display All":
        i = 1
        for word in WordNetPy.wordsMap:
            print(str(i) + ": " + word)
            i += 1
    if inputWord == "quit":
        break;
    else:
        words = WordNetPy.hyponyms(inputWord)
        if type(words) is str:
            print(words)
        else:
            for i in range(len(words)):
                print(str(i+1) + ": " + str(words[i]))
