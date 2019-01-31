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
	# print(text)

	parsedTree = ""
	for count, line in enumerate(text):
		# print(line)
		parsedTree += line

		if "(. .)" not in line and "(. ?)" not in line:
			continue

		# print("hi")
		# the end of the parsedTree has been reached
		print(parsedTree)
		depth = 0

		parsedTree = parsedTree.split("\n")
		# print(parsedTree)

		sequence = []
		sentenceTuple = []
		for line in parsedTree:
			tokenizedLine = list(filter(None, line.replace("\n", "").split(" ")))
			# print(tokenizedLine)
			oldDepth = 0
			for count, item in enumerate(tokenizedLine):
				depth += item.count("(")
				depth -= item.count(")")
				# print(depthDict)
				
				word = item.replace(")", "").replace(" ", "").lower()
				if any(letter.islower() for letter in item) and word not in stopwords:
					pos = tokenizedLine[count-1].replace("(", "").replace(" ", "")
					# print(pos, word, oldDepth)
					sentenceTuple.append((word, pos, sequence))
					sequence = []
					print(word, oldDepth)

				if word not in stopwords:		
					sequence.append(depth)
				else:
					sequence = sequence[:-1]
				
				oldDepth = depth
				# if word not in stopwords:
				# 	wordsToSave[word] = pos
				# 	if word not in environmentVectors:
				# 		environmentVectors[word] = np.random.choice([-1, 1], size=10000)

		print(sentenceTuple)

		movement = []
		for i in range(len(sentenceTuple)):
			word = sentenceTuple[i][0]
			pos = sentenceTuple[i][1]
			sequencePosition = sentenceTuple[i][2]
			if word not in environmentVectors:
				environmentVectors[word] = np.random.choice([-1, 1], size=10000)

			firstOne = True
			for j in range(1, len(sentenceTuple)):
				# count is the difference between last parenthesi count and next count.

				count = sequencePosition[-1] - sentenceTuple[j][2][0]

				upCount = 0
				# how many steps you have to go up
				for x in range(count):
					if not firstOne:
						upCount += 1
					else:
						movement.append("up")
				# how many items left in the sequence... to go down.
				for x in range(len(sentenceTuple[j][2]) - 1):
					while upCount != 0:
						upCount -= 1
						
					movement.append("down")

				print(sentenceTuple[j][0], movement)
				# the last down is always useless because it just brings you to the word...
				movement = movement [:-1]
				firstOne = False
				# movement = []

			firstOne = True
			break

		exit()

		# tokenized = list(filter(None, parsedTree.replace("\n", "").split(" ")))
		# print(tokenized)
		# # exit()

		# # saves words and their part of speech
		# wordsToSave = {}
		# for count, token in enumerate(tokenized):

		# 	# if there is a lowercase letter, there's a word
		# 	if any(letter.islower() for letter in token):
		# 		pos = tokenized[count-1].replace("(", "").replace(" ", "")
		# 		word = token.replace(")", "").replace(" ", "").lower()
		# 		# print(pos, word)

		# 		if word not in stopwords:
		# 			wordsToSave[word] = pos
		# 			if word not in environmentVectors:
		# 				environmentVectors[word] = np.random.choice([-1, 1], size=10000)

		# # print(wordsToSave)
		# # addes context vectors * part of speech vector
		# saveToLexical = wordsToSave.copy()
		# for word in wordsToSave:

		# 	if word not in lexicalVectors:
		# 		lexicalVectors[word] = np.zeros(10000)

		# 	saveToLexical.pop(word)
		# 	for contextWord in saveToLexical:
		# 		# generate random vectors for part of speech
		# 		if saveToLexical[contextWord] not in posVectors:
		# 			posVectors[saveToLexical[contextWord]] = np.random.choice([-1, 1], size=10000)

		# 		lexicalVectors[word] += environmentVectors[contextWord] * posVectors[saveToLexical[contextWord]]

		# 	saveToLexical[word] = wordsToSave[word]

		# parsedTree = ""

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
	results = []
	for i in range(numResults):
		word = max(analogyResults, key=analogyResults.get)

		results.append((word, analogyResults[word]))
		analogyResults.pop(word)

	return results

if __name__ == "__main__":
	stopWords = generateStopWords('stopwords.txt')
	posVectors = {}
	environmentVectors = {}
	lexicalVectors = {}

	posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# results = grabAnalogy('industrial', 'senior', 'average', lexicalVectors, environmentVectors)
	# for result in results:
		# print(result)