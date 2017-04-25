#-------------------------------------------------------------------------------------------------
# Adam Lefaivre - 001145679
# CPSC 5310 - Dr. Yllias Chali
# Programming Portion Assn. 2 - Random Sentence Generator
#-------------------------------------------------------------------------------------------------

from __future__ import print_function
import nltk
import random
import re
from nltk.corpus import gutenberg
from nltk.corpus import inaugural
from nltk import bigrams
from nltk import trigrams
from nltk.corpus import PlaintextCorpusReader
import os
import sys

def generateRandomSentencesUsingBigrams(corpus):

    #Get a set of all of the starting words to seed the generation of a random sentence.
    startingWords = []
    flag = False
    stopChars = [".", "!", "?"]
    dependencyChars = ["(", ")", "\"", "\"", "]", "[", "{", "}", "<", ">"]
    dependencyCharsUnicode = [unicode("("), unicode(")"), unicode("\""), unicode("\""), unicode("]"), unicode("["), unicode("{"), unicode("}"), unicode("<"), unicode(">")]
    stopCharsUnicode = [unicode("."), unicode("!"), unicode("?")]
    namePrefixes = ["Mr", "Ms", "Mrs","Dr"]
    namePrefixesUnicode = [unicode("Mr"), unicode("Ms"), unicode("Mrs"), unicode("Dr")]
    firstItem = True

    #Grab all of the starting words and store them
    for item in corpus:
        if firstItem:
            startingWords.append(item)
            firstItem = False
        if ((item in stopCharsUnicode) or (item in stopChars)):
            flag = True
            continue
        if flag:
            flag = False
            startingWords.append(item)

    #Now randomly pick the starting word from the set that we have generated (exclude Mr, Ms, etc.)
    setOfStartingWords = set(startingWords)
    newSetOfStartingWords = set()
    for item in setOfStartingWords:
        if (not (item in namePrefixesUnicode) or (item in namePrefixes)):
            newSetOfStartingWords.add(item)

    initWord = random.sample(newSetOfStartingWords, 1)
    initWord = initWord[0]
    if(isinstance(initWord, unicode)):
        initWord = unicode.decode(initWord)
    word = initWord

    #Start Creating a random sentence using bigrams
    #Model the corpus, using bigrams!
    bigrams = nltk.bigrams(corpus)

    #Create a conditional probability distribution given a conditional
    #frequency distribution.  We use the maximum likelihood estimate
    #to seed the generation of random words. We do this so that we
    #can generate random (yet, somewhat probable) next word of the sentence.
    #Recall that the MLE calculation is: P(Wn | Wn-1) = C(Wn-1, Wn)/C(Wn-1)
    condFreq = nltk.ConditionalFreqDist(bigrams)
    condProb = nltk.ConditionalProbDist(condFreq, nltk.MLEProbDist)
    print ("\n")
    print("The bigram model gives:")
    print ("\n")
    sentence = []
    sentence.append(initWord)
    counter = 1
    while ((word not in stopChars) and (word not in stopCharsUnicode) or (counter < 5)):
        word = condProb[word].generate()
        while(word in dependencyCharsUnicode) or (word in dependencyChars):
            word = condProb[word].generate()
        counter += 1
        sentence.append(word)

    #Try to model some punctuation representation in the printed output.
    #This can be done to a much greater extent, however it is not necessary for the
    #purposes of the program (i.e. I avoided worrying about capital words in the middle of
    #the sentence because this gets complex).
    isFirstWord = True
    punctuation = ["'", "'", "!", ";", ":", "\\", ",", ".", "/", "?", "@", "#", "$", "%", "^", "*", "_", "~"]
    apostropheEndings = ["s", "re", "ve", "t"]
    for word in sentence:
        if(isFirstWord):
            print(word, end='')
            isFirstWord = False
        elif(word in punctuation) or (word in apostropheEndings):
            print(word, end='')
        else:
            print(" ", end='')
            print(word, end='')
    print ("\n")

#Get input from user
inputControlOption = ''
inputControlOption = raw_input('Would you like to enter the corpus as a text file? Or, we can can use a corpus from the gutenberg corpora, or from the presidential inauguration corpora (type tx for textfile OR gt for gutenberg OR in for inauguration): ').lower()
inputControlOption = str(inputControlOption)
arr = ['tx', 'gt', 'in']

#If user input is wrong keep trying until text or string is received!
while inputControlOption not in arr:
    inputControlOption = raw_input('Wrong input, please try again (type tx for textfile OR gt for gutenberg OR in for inauguration): ').lower()

if (inputControlOption == 'tx'):
    pathToTextFile = raw_input('Please enter the name (including the path) for the textfile: ')
    while(not os.path.isfile(pathToTextFile)):
        pathToTextFile = raw_input('That file does not exist.  Please enter the name (including the path) for the textfile: ')

    path, file = os.path.split(pathToTextFile)
    corp = PlaintextCorpusReader(path, file)
    corpus = nltk.Text(corp.words())
    generateRandomSentencesUsingBigrams(corpus)

elif(inputControlOption == 'st'):
    corpus = raw_input('Please enter your corpus manually: ')
    generateRandomSentencesUsingBigrams(corpus)

elif (inputControlOption == 'gt'):
    whichGutenCorpora = ''
    gutenbergTextFiles = nltk.corpus.gutenberg.fileids()
    print ("The gutenberg textfiles include: ")
    for file in gutenbergTextFiles:
        print(file + " ")
    whichGutenCorpora = raw_input('Please enter the corpora from the gutenberg corpora, with the exact name as given in the list of corpora above: ')
    while whichGutenCorpora not in gutenbergTextFiles:
        print('Wrong input, the gutenberg corpora include: ')
        for file in gutenbergTextFiles:
            print(file + " ")
        print("\n")
        whichGutenCorpora = raw_input('Please enter the corpora from the gutenberg corpora, with the exact name as given in the list of corpora above: ')

    #Begin generating a sentence.
    corpus = nltk.corpus.gutenberg.words(whichGutenCorpora)
    generateRandomSentencesUsingBigrams(corpus)

elif (inputControlOption == 'in'):
    whichInaugCorpora = ''
    inaugTextFiles = nltk.corpus.inaugural.fileids()
    print ("The presidential inauguration textfiles include: ")
    for file in inaugTextFiles:
        print(file + " ")
    whichInaugCorpora = raw_input(
        'Please enter the corpora from the inauguration corpora, with the exact name as given in the list of corpora above: ')
    while whichInaugCorpora not in inaugTextFiles:
        print('Wrong input, the presidential inauguration corpora include: ')
        for file in inaugTextFiles:
            print(file + " ")
        print("\n")
        whichInaugCorpora = raw_input(
            'Please enter the corpora from the gutenberg corpora, with the exact name as given in the list of corpora above: ')

    #Generate a sentence using the maximum likelihood for the following word (i.e. bigram pair)
    corpus = nltk.corpus.inaugural.words(whichInaugCorpora)
    generateRandomSentencesUsingBigrams(corpus)


