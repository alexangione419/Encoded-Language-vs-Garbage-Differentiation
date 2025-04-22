import data_prep.obfuscator as obfuscator
from scipy import optimize, special, stats
import numpy as np
import matplotlib.pyplot as plt




# returns a value indicating the fit of the text to Ziph's Law
def ziphsChecker(textFrequency: map):
    
    # sort the map by value
    wordFrequencies = np.array(sorted(textFrequency.values(), key=lambda x: x, reverse=True))
    #print(wordFrequencies)
    ranks = np.arange(1, len(wordFrequencies) + 1)


    total_count = wordFrequencies.sum()
    s_parameter = 1.1   
    # calculate the expected probabilities for each rank under Zipf’s law
    #  P(rank i) = 1 / (i^s) / (normalization constant)
    normalization = np.sum(1.0 / (ranks ** s_parameter))
    expected_probs = (1.0 / (ranks ** s_parameter)) / normalization

    expected_freqs = total_count * expected_probs

    # Chi-Square Goodness-of-Fit test using .
    chi2_stat, _ = stats.chisquare(f_obs=wordFrequencies, f_exp=expected_freqs)

    return chi2_stat

# a function to evaluate the fit of the text to heaps law
def heapsChecker(frequencyMap: map):
    numberOfUniqueWords = len(frequencyMap)
    numberOfTotalWords = sum(frequencyMap.values())
    assumbed_b = 0.5
    assumed_k = 60

    # heaps law is defined as 
    # V(N) = k * N^b where V(N) is the number of unique words, N is the number of total words
    # for the majority of natural languages, b is between 0.4 and 0.6, so we will assume it to be 0.5 to calculate k

    # to estimate the correct values of k and b, we can use
    estimated_K = numberOfUniqueWords / (numberOfTotalWords ** assumbed_b)
    estimated_B = np.log(numberOfUniqueWords/assumed_k) / np.log(numberOfTotalWords)

    return estimated_K, estimated_B 

# calculates the shannon entropy, or the propsed amount of information conatined within the text
def shannonEntropyChecker(frequencyMap: map):
    # shannon entropy is defined as H(X) = -sum(p(x) * log2(p(x))) for all x in X
    # where p(x) is the probability of x occuring in the text
    totalWords = sum(frequencyMap.values())
    sEntropy = 0
    for word in frequencyMap:
        probability = frequencyMap[word] / totalWords
        sEntropy += probability * np.log2(probability)
    
    return -sEntropy


# a function to evaluate a given text by calcualting values for
# Ziph's Law, Heap’s Law, Shannon Entropy
def textEvaluator(givenText: str):
    byteMap = {}

    # find the most common character and use it as the space
    for byte in givenText.split(" "):
        if byte in byteMap:
            byteMap[byte] = byteMap[byte]+1
        else:
            byteMap[byte] = 1

    space_character = max(byteMap, key=byteMap.get)

    # seperate the bytes into "words" by spaces
    brokenUpBySpace = givenText

    if space_character != "":
        brokenUpBySpace = givenText.split(space_character)
    
    tokenMap = {}
    for token in brokenUpBySpace:
        if token in tokenMap:
            tokenMap[token] = tokenMap[token]+1
        else:
            tokenMap[token] = 1

    ziphsFit = ziphsChecker(tokenMap)
    heapsFit1, heapsFit2 = heapsChecker(tokenMap)
    shannonEnt = shannonEntropyChecker(tokenMap)
    
    return [ziphsFit, heapsFit1, heapsFit2, shannonEnt]


