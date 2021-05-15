import sys
import re

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "h":
        print("--encrypt    takes in a txt file as input with the last line being the key to encrypt with. "
              "Outputs encrypted text to file 'encrypted.txt'")
        print("--decrypt    takes in a txt file as input with the last line being the key to decrypt with. "
              "Outputs decrypted text to file 'decrypted.txt'")
        print("--guess      takes in a txt file as input with no key. "
              "Will try to guess decryption based on frequency analysis. "
              "Recommended input size of at least 2000 characters")
    elif sys.argv[1] == "--encrypt":
        with open(sys.argv[2], 'r') as file:
            myMessage = file.read()

        with open(sys.argv[2], 'r') as file:
            myKey = file.readlines()[-1]

        checkValidKey(myKey)

        translated = encryptMessage(myKey, myMessage)

        print(translated[:translated.rfind('\n')])
        print(myKey)

        original_stdout = sys.stdout
        with open('encrypted.txt', 'w') as f:
            sys.stdout = f
            print(translated[:translated.rfind('\n')])
            print(myKey, end='')
            sys.stdout = original_stdout

    elif sys.argv[1] == "--decrypt":
        with open(sys.argv[2], 'r') as file:
            myMessage = file.read()

        with open(sys.argv[2], 'r') as file:
            myKey = file.readlines()[-1]

        checkValidKey(myKey)

        translated = decryptMessage(myKey, myMessage)

        print(translated[:translated.rfind('\n')])

        original_stdout = sys.stdout
        with open('decrypted.txt', 'w') as f:
            sys.stdout = f
            print(translated[:translated.rfind('\n')])
            print(myKey, end='')
            sys.stdout = original_stdout

    elif sys.argv[1] == "--guess":
        with open(sys.argv[2], 'r') as file:
            myMessage = file.read().replace('\n', '')

        translated = myMessage

        # letters
        letterFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        letterFrequencyAnalysis(translated, letterFrequency)

        # 2-letter words
        wordFrequency2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        encryptedWords2 = findEncryptedWords2(translated)
        wordFrequencyAnalysis2(translated, encryptedWords2, wordFrequency2)

        # 3-letter words
        wordFrequency3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        encryptedWords3 = findEncryptedWords3(translated)
        wordFrequencyAnalysis3(translated, encryptedWords3, wordFrequency3)

        keyGuess = "??????????????????????????"
        keyGuess = guessKey(keyGuess, letterFrequency, encryptedWords3, wordFrequency3, encryptedWords2, wordFrequency2)
        while not keyGuess.count('?') == 0:
            keyGuess = guessKey(keyGuess, letterFrequency, encryptedWords3, wordFrequency3, encryptedWords2, wordFrequency2)

        decrypted = decryptMessage(keyGuess, translated)

        print("Guessed key: " + keyGuess)
        print("Attempted Decrypt: " + decrypted)

        # print key to output file
        original_stdout = sys.stdout
        with open('guessKey.txt', 'w') as f:
            sys.stdout = f
            print(keyGuess)
            sys.stdout = original_stdout
    else:
        sys.exit('Invalid option. Use --help')


def checkValidKey(key):
    keyList = list(key)
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList:
        sys.exit('This is not a valid monoalphabetic substitution cipher key!')


def encryptMessage(key, message):
    translated = ''
    charsA = LETTERS
    charsB = key
    for symbol in message:
        if symbol.upper() in charsA:
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol
    return translated


def decryptMessage(key, encrypted):
    decrypted = ""
    for x in encrypted:
        if x.upper() in key:
            index1 = key.find(x.upper())
            if x.isupper():
                decrypted += LETTERS[index1]
            else:
                decrypted += LETTERS[index1].lower()
        else:
            decrypted += x
    return decrypted


def letterFrequencyAnalysis(encrypted, frequencyArray):
    for x in encrypted:
        if x.upper() in LETTERS:
            letIndex = LETTERS.find(x.upper())
            frequencyArray[letIndex] += 1
    return encrypted


def findEncryptedWords3(encrypted):
    words = encrypted.split()
    encryptedWords = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                      "", "", ""]
    existingWord = False
    cur_index = 0
    for word in words:
        if len(word.strip(".,'()!?")) == 3:
            existingWord = False
            for encryptedWord in encryptedWords:
                if word.lower() == encryptedWord.lower():
                    existingWord = True
                    break
            if not existingWord and cur_index < 26:
                encryptedWords[cur_index] = word.strip(".,'()!?").lower()
                cur_index += 1
    # print(encryptedWords)
    return encryptedWords


def findEncryptedWords2(encrypted):
    words = encrypted.split()
    encryptedWords = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                      "", "", ""]
    existingWord = False
    cur_index = 0
    for word in words:
        if len(word.strip(".,'()!?")) == 2:
            existingWord = False
            for encryptedWord in encryptedWords:
                if word.lower() == encryptedWord.lower():
                    existingWord = True
                    break
            if not existingWord and cur_index < 26:
                encryptedWords[cur_index] = word.strip(".,'()!?").lower()
                cur_index += 1
    return encryptedWords


def wordFrequencyAnalysis3(encrypted, words, frequencyArray):
    ogWords = encrypted.split()
    for x in range(len(ogWords)):
        ogWords[x] = ogWords[x].strip(".,'()!?").lower()

    for word in ogWords:
        if word in words:
            frequencyArray[words.index(word)] += 1


def wordFrequencyAnalysis2(encrypted, words, frequencyArray):
    ogWords = encrypted.split()
    for x in range(len(ogWords)):
        ogWords[x] = ogWords[x].strip(".,'()!?").lower()

    for word in ogWords:
        if word in words:
            frequencyArray[words.index(word)] += 1


def guessKey(keyGuess, frequencyLetters, encryptedWords3, frequencyWords3, encryptedWords2, frequencyWords2):
    largIndLetters = largestIndeces(frequencyLetters)
    largeIndWords3 = largestIndeces(frequencyWords3)
    largeIndWords2 = largestIndeces(frequencyWords2)

    # print(frequencyLetters)
    # print(largIndLetters)
    # print(encryptedWords2)
    # print(frequencyWords2)
    # print(largeIndWords2)
    # print(encryptedWords3)
    # print(frequencyWords3)
    # print(largeIndWords3)
    # print(encryptedWords[largeIndWords[0]][2] + " " + LETTERS[largIndLetters[0]])

    # start by finding "THE"
    # if the last letter of the most common 3-letter word, is one of the most common letters, we're probably talking about "the"
    for x in range(3):
        for i in range(3):
            for j in range(3):
                if encryptedWords3[largeIndWords3[x]][2].upper() == LETTERS[largIndLetters[i]]:
                    if encryptedWords3[largeIndWords3[x]][0].upper() == LETTERS[largIndLetters[j]]:
                        keyGuess = makeGuess(keyGuess, LETTERS[largIndLetters[i]], "E")
                        keyGuess = makeGuess(keyGuess, LETTERS[largIndLetters[j]], "T")
                        keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[x]][1].upper(), "H")

    # Then we try to guess for one of the most common 2-letter words: "to"
    # We assume we've already guessed 't' correctly
    for i in range(3):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("T")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][1].upper(), "O")
            break

    # Then we guess for the 3-letter word "not"
    # we assume we already have 'o' and 't' correct
    for i in range(10):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("T")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("O")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "N")
            break

    # Then we guess fot the 2-letter word "of"
    # we assume we already have 'o', and we're hoping 'f' is quite uncommon
    for i in range(5):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("O")] and not \
                encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("N")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][1].upper(), "F")
            break

    # Then we guess for the 3-letter word "for"
    # we assume we already have 'f' and 'o' correct
    for i in range(10):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("F")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("O")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][2].upper(), "R")
            break

    # Then we guess fot the 2-letter word "in"
    # we assume we already have 'n'
    for i in range(10):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("N")] and not \
                encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("A")] and not \
                encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("O")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][0].upper(), "I")
            break

    # Then we guess for the 3-letter word "are"
    # we assume we already have 'e' correct
    for i in range(1, 7):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("E")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("R")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "A")
            break

    # Then we guess fot the 2-letter word "be"
    # we assume we already have 'e'
    for i in range(10):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("E")] and not \
                encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("H")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][0].upper(), "B")
            break

    # Then we guess for the 3-letter word "and"
    # we assume we already have 'a' correct
    for i in range(1, 7):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("A")] and not \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("R")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][1].upper(), "N")
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][2].upper(), "D")
            break

    # Then we guess for the 3-letter word "but"
    # we assume we already have 't' correct
    for i in range(1, 15):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("T")] and not \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("O")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "B")
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][1].upper(), "U")
            break

    # Then we guess for the 3-letter word "you"
    # we assume we already have 'o' correct
    for i in range(1, 15):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("O")] and not \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("R")] and not \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("T")] and not \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("D")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "Y")
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][2].upper(), "U")
            break

    # Then we guess for the 3-letter word "any" to assert y
    # we assume we already have 'o' correct
    for i in range(1, 15):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("A")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("N")] and not \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("D")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][2].upper(), "Y")
            break

    # Then we guess for the 3-letter word "who"
    # we assume we already have 'h' and 'o' correct
    for i in range(7):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("O")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("H")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "W")
            break

    # Then we guess for the 3-letter word "all"
    # we assume we already have 'a' correct, and check that 2nd and 3rd letters are the same
    for i in range(1, 7):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("A")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == encryptedWords3[largeIndWords3[i]][2].upper():
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][1].upper(), "L")
            break

    # Then we guess fot the 2-letter word "is"
    # we assume we already have 'i'
    for i in range(10):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][0].upper() == keyGuess[LETTERS.index("I")] and not \
                encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("N")] and not \
                encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("T")] and not \
                encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("F")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][1].upper(), "S")
            break

    # Then we guess fot the 2-letter word "my"
    # we assume we already have 'e'
    for i in range(26):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if encryptedWords2[largeIndWords2[i]][1].upper() == keyGuess[LETTERS.index("Y")]:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][0].upper(), "M")
            break

    # Then we guess for the 3-letter word "him"
    # we assume we already have 'h' and 'i' correct
    for i in range(26):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("H")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("I")] and not \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("S")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][2].upper(), "M")
            break

    # Then we guess for the 3-letter word "man"
    # this one is to verify our 'm' guess on the previous word, because M is hard to determine
    # we assume we already have 'a' and 'n' correct
    for i in range(26):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("A")] and \
                encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("N")]:
            if encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("M")]:
                break
            else:
                keyGuess = makeGuess(keyGuess, "?", "M")
            break

    # Then we guess for the 3-letter word "can"
    # we assume we already have 'a' and 'n' correct
    for i in range(26):
        if encryptedWords3[largeIndWords3[i]] == '':
            break
        if encryptedWords3[largeIndWords3[i]][2].upper() == keyGuess[LETTERS.index("N")] and \
                encryptedWords3[largeIndWords3[i]][1].upper() == keyGuess[LETTERS.index("A")] and not \
                encryptedWords3[largeIndWords3[i]][0].upper() == keyGuess[LETTERS.index("M")]:
            keyGuess = makeGuess(keyGuess, encryptedWords3[largeIndWords3[i]][0].upper(), "C")
            break

    # Then we guess for the 2-letter word "up". this is just kinda a wild guess lol
    for i in range(26):
        if encryptedWords2[largeIndWords2[i]] == '':
            break
        if (keyGuess.count(encryptedWords2[largeIndWords2[i]][0].upper()) == 0 or encryptedWords2[largeIndWords2[i]][
            0].upper() == keyGuess[LETTERS.index("U")]) and \
                keyGuess.count(encryptedWords2[largeIndWords2[i]][1].upper()) == 0:
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][0].upper(), "U")
            keyGuess = makeGuess(keyGuess, encryptedWords2[largeIndWords2[i]][0].upper(), "P")
            break

    # now we'll just fill a remaining letter by its individual frequency
    keyGuess = fillRemainingLetters(keyGuess, largIndLetters)

    return keyGuess


def makeGuess(keyGuess, encrypt, decrypt):
    if not keyGuess[LETTERS.index(decrypt)] == '?':  # prefer previous guesses
        return keyGuess
    keyGuess = keyGuess[:LETTERS.index(decrypt)] + encrypt + keyGuess[LETTERS.index(decrypt) + 1:]
    return keyGuess


def largestIndeces(arr):
    maxIndeces = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                  -1]
    for x in range(26):
        maxOfArr = 0
        maxIndex = 0
        for i in range(26):
            if arr[i] >= maxOfArr:
                if x == 0:
                    maxOfArr = arr[i]
                    maxIndex = i
                if arr[i] <= arr[maxIndeces[x - 1]] and maxIndeces.count(i) == 0:
                    maxOfArr = arr[i]
                    maxIndex = i
        maxIndeces[x] = maxIndex

    return maxIndeces


def fillRemainingLetters(keyGuess, largIndLetters):
    normalFrequency = ["E", "T", "A", "I", "N", "O", "S", "H", "R", "D", "L", "U", "C", "M", "F", "W", "Y", "G", "P",
                       "B", "V", "K", "Q", "J", "X", "Z"]
    fill = False
    for i in range(26):
        if keyGuess[LETTERS.index(normalFrequency[i])] == '?':  # if a high frequency letter is still not guessed
            for x in range(26):
                if keyGuess.count(LETTERS[largIndLetters[x]]) == 0:
                    keyGuess = keyGuess[:LETTERS.index(normalFrequency[i])] + LETTERS[largIndLetters[x]] + keyGuess[
                                                                                                           LETTERS.index(
                                                                                                               normalFrequency[
                                                                                                                   i]) + 1:]
                    # print("Guessing for: " + normalFrequency[i])
                    fill = True
                    break
        if fill:
            break
    return keyGuess


if __name__ == "__main__":
    main()
