import numpy as np
import os
import traceback

def generateStopWords(filepath):
	stopWords = set()
	with open(filepath) as text:
		for count, line in enumerate(text):	
			stopWords.add(line.replace("\n", ""))
	return stopWords

def addTreeBank(filePath, posVectors, environmentVectors, lexicalVectors, stopwords):
	text = open(filePath)

	parsedTree = ""
	for count, line in enumerate(text):
		if "(. .)" not in line and "(. ?)" not in line:
			parsedTree += line
			continue

		# the end of the parsedTree has been reached
		tokenized = list(filter(None, parsedTree.replace("\n", "").split(" ")))

		# saves words and their part of speech
		wordsToSave = {}
		for count, token in enumerate(tokenized):

			# if there is a lowercase letter, there's a word
			if any(letter.islower() for letter in token):
				pos = tokenized[count-1].replace("(", "").replace(" ", "")
				word = token.replace(")", "").replace(" ", "").lower()
				# print(pos, word)

				if word not in stopwords:
					wordsToSave[word] = pos
					if word not in environmentVectors:
						environmentVectors[word] = np.random.choice([-1, 1], size=10000)

		# prinpt(wordsToSave)
		# addes context vectors * part of speech vector
		saveToLexical = wordsToSave.copy()
		for word in wordsToSave:

			if word not in lexicalVectors:
				lexicalVectors[word] = np.zeros(10000)

			saveToLexical.pop(word)
			for contextWord in saveToLexical:
				# generate random vectors for part of speech
				if saveToLexical[contextWord] not in posVectors:
					posVectors[saveToLexical[contextWord]] = np.random.choice([-1, 1], size=10000)

				lexicalVectors[word] += environmentVectors[contextWord] * posVectors[saveToLexical[contextWord]]

			saveToLexical[word] = wordsToSave[word]

		parsedTree = ""

	text.close()
	return posVectors, environmentVectors, lexicalVectors

def grabAnalogy(concept1, concept2, analogousTo, lexicalVectors, environmentVectors, numResults=1):
	f = lexicalVectors[concept1] * lexicalVectors[concept2]
	analogyResults = {}
	for word in environmentVectors:
		if word != analogousTo:
			analogyResults[word] = np.dot(environmentVectors[word],	environmentVectors[analogousTo] * f)

	# for key, value in analogyResults.items():
	#     if value > 4000:
	#         print(key, value)

	# print(analogyResults)
	returnAnalogyResults = analogyResults.copy()
	results = []
	for i in range(numResults):
		word = max(analogyResults, key=analogyResults.get)

		results.append((word, analogyResults[word]))
		analogyResults.pop(word)

	return returnAnalogyResults, results

if __name__ == "__main__":
	stopWords = generateStopWords('stopwords.txt')
	analogyResults = {'cat': 0, 'likes': 0, 'meow': 0, 'dog': 0, 'night': 0, 'purr': 0}

	for i in range(1000):
		posVectors = {}
		environmentVectors = {}
		lexicalVectors = {}
		posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
		newAnalogyResults, result = grabAnalogy('dog', 'cat', 'bark', lexicalVectors, environmentVectors)
		for eachResult in newAnalogyResults:
			analogyResults[eachResult] += newAnalogyResults[eachResult]

	for eachResult in analogyResults:
		analogyResults[eachResult] = analogyResults[eachResult]/1000

	print(analogyResults)