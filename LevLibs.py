from re import U
from turtle import distance
from english_words import english_words_lower_alpha_set as words
import eng_to_ipa as ipa
import Levenshtein
import json

def createIPAJSON():
    ipaDict = {}
    for word in words:
        for ipaWord in ipa.ipa_list(word)[0]:
            ipaDict[ipaWord] = word

    # write out the json
    with open('ipaData.json', 'w') as out:
        json.dump(ipaDict, out)    

def getPhoneticlySimilarWordlist(userIPA, ipaDict):
    simWordlist = []
    for ipaWord in ipaDict:
        if Levenshtein.distance(userIPA, ipaWord) < 2:
            if userIPA[0] == ipaWord[0]: # and userIPA[-1] == ipaWord[-1]:
                simWordlist.append(ipaDict[ipaWord])
    return simWordlist

if __name__ == "__main__":
    #createIPAJSON()

    #1. translate all english words to IPA and store
    with open('ipaData.json', 'r') as inF:
        ipaDict = json.load(inF)

    #2. get user string
    userInput = "the quick brown fox jumped over the lazy dog"
    print(f"Origninal => {userInput}")

    #3. translate user string to IPA
    userIPA = ipa.convert(userInput)
    print(f"IPA => {userIPA}")

    #4. get a list of similar sounding words for each word in the sentence
    results = {}
    for userIPA, userWord in zip(userIPA.split(), userInput.split()):
        results[userWord] = getPhoneticlySimilarWordlist(userIPA, ipaDict)

    #5. put together a similar sounding sentence
    simSentences = []

    maxLen = 0
    for userWord in results:
        if maxLen < len(results[userWord]):
            maxLen = len(results[userWord])
    
    for sentanceCount in range(maxLen):
        newSentence = ""
        for userWord in results:
            try:
                newSentence = newSentence + results[userWord][sentanceCount] + " "
            except:
                newSentence =newSentence + userWord + " "
        simSentences.append(newSentence)

    print("\nSimilar sounding sentences?")
    for sentance in simSentences:
        print(sentance)


