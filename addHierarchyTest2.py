import numpy as np
import os
import traceback

def generateStopWords(filepath):
	stopWords = set()
	with open(filepath) as text:
		for count, line in enumerate(text):	
			stopWords.add(line.replace("\n", ""))
	return stopWords

def addTreeBank(filePath, posVectors, environmentVectors, lexicalVectors, upVector, downVector):
	text = open(filePath)

	parsedTree = ""
	for count, line in enumerate(text):
		parsedTree += line

		if "(. .)" not in line and "(. ?)" not in line and "(: :)" not in line:
			continue

		print(parsedTree)
		# the end of the parsedTree has been reached
		depth = 0
		oldDepth = 0

		parsedTree = parsedTree.split("\n")

		# Saves a list of unique words and their count.
		wordFrequency = {}

		# For each nonunique word, returns the original word
		nonUniqueWords = {}

		# sequence is parenthesis pops / pushes
		sequence = []
		# list of all the words, pos, and 
		sentenceTuple = []

		for line in parsedTree:
			tokenizedLine = list(filter(None, line.replace("\n", "").replace(" )", ")").split(" ")))

			for count, item in enumerate(tokenizedLine):
				depth += item.count("(")
				depth -= item.count(")")
				
				if ")" in item:
					word = item.replace(")", "").replace(" ", "").lower()
					pos = tokenizedLine[count-1].replace("(", "").replace(" ", "")

					# makes sure words that aren't unique don't screw up the order later
					if word not in wordFrequency:
						wordFrequency[word] = 1
						appendedWord = word
					else:
						appendedWord = word + str(wordFrequency[word])
						wordFrequency[word] += 1
						nonUniqueWords[appendedWord] = word

					sentenceTuple.append((appendedWord, pos, sequence))

					# create 10,000 dimensional vectors
					if word not in environmentVectors:
						environmentVectors[word] = np.random.choice([-1, 1], size=10000)
					if word not in lexicalVectors:
						lexicalVectors[word] = np.zeros(10000)
					if pos not in posVectors:
						posVectors[pos] = np.random.choice([-1, 1], size=10000)

					#reset sequence for next
					sequence = []
					oldDepth = 0
				
				if depth > oldDepth:
					sequence.append(depth)
					oldDepth = depth

		# print(sentenceTuple)

		count = 0
		movementResults = {}
		print(sentenceTuple)

		# stores sequences first
		for i in range(1, len(sentenceTuple)):
			firstWord = sentenceTuple[i-1][0]
			firstSequence = sentenceTuple[i-1][2]

			secondWord = sentenceTuple[i][0]
			secondWordPos = sentenceTuple[i][1]
			secondSequence = sentenceTuple[i][2]

			count = firstSequence[-1] - secondSequence[0]
			movement = []
			movementVector = None
			upDownCount = 0

			for x in range(count):

				if movementVector == None:
					movementVector = upVector
					upDownCount += 1
				else:
					movementVector *= np.concatenate([upVector[upDownCount:], upVector[:upDownCount]])
					upDownCount += 1

				movement.append("up")
			for x in range(len(secondSequence) - 1):

				if movementVector == None:
					movementVector = downVector
					upDownCount += 1
				else:
					movementVector *= np.concatenate([downVector[upDownCount:], downVector[:upDownCount]])
					upDownCount += 1

				movement.append("down")

			movementResults[firstWord + " " + secondWord] = movement
			# add to high dimensional vectors also here.

			if firstWord in nonUniqueWords:
				firstWord = nonUniqueWords[firstWord]
			if secondWord in nonUniqueWords:
				secondWord = nonUniqueWords[secondWord]

			print("Saved lexicalVectors", firstWord, ":", secondWord)
			lexicalVectors[firstWord] += environmentVectors[secondWord] * posVectors[secondWordPos] * movementVector

		for i in range(len(sentenceTuple)):
			for j in range(len(sentenceTuple)):

				firstWord = sentenceTuple[i][0]
				secondWord = sentenceTuple[j][0]
				secondWordPos = sentenceTuple[j][1]

				# check that it's not the same word
				if firstWord == secondWord or (firstWord + " " + secondWord) in movementResults:
					continue

				# check if flipped exists
				elif secondWord + " " + firstWord in movementResults:
					newMovement = []
					for direction in movementResults[secondWord + " " + firstWord]:
						if direction == "up":
							newMovement = ['down'] + newMovement
						else:
							newMovement = ['up'] + newMovement

					movementResults[firstWord + " " + secondWord] = newMovement

					movementVector = None
					upDownCount = 0
					# saves into highly dimensional vectors
					for eachDirection in newMovement:	
						if eachDirection == "up":
							if movementVector == None:
								movementVector = upVector
								upDownCount += 1
							else:
								movementVector *= np.concatenate([upVector[upDownCount:], upVector[:upDownCount]])
								upDownCount += 1
						elif eachDirection == "down":
							if movementVector == None:
								movementVector = downVector
								upDownCount += 1
							else:
								movementVector *= np.concatenate([downVector[upDownCount:], downVector[:upDownCount]])
								upDownCount += 1

					firstWordOG = firstWord
					secondWordOG = secondWord
					if firstWord in nonUniqueWords:
						firstWordOG = nonUniqueWords[firstWord]
					if secondWord in nonUniqueWords:
						secondWordOG = nonUniqueWords[secondWord]

					lexicalVectors[firstWordOG] += environmentVectors[secondWordOG] * posVectors[secondWordPos] * movementVector

				else:
					# print(firstWord + " " + secondWord)
					savedSequence = []
					
					pairQueried1 = firstWord + " " + sentenceTuple[j-1][0]
					pairQueried2 = sentenceTuple[j-1][0] + " " + secondWord

					getSequence1 = movementResults[pairQueried1]
					if pairQueried2 in movementResults:
						getSequence2 = movementResults[pairQueried2]
					else:
						for i in range(wordFrequency[sentenceTuple[j][0]]):
							wordWithIndex = sentenceTuple[j][0] + str(i)
							if sentenceTuple[j-1][0] + " " + wordWithIndex in movementResults:
								getSequence2 = movementResults[sentenceTuple[j-1][0] + " " + wordWithIndex]
								break

					downCount = 0
					upCount = 0
					for count, upDown in enumerate(getSequence1):
						if upDown == "down":
							downCount += 1
					for count, upDown in enumerate(getSequence2):
						if upDown == "up":
							upCount += 1

					minUpDown = min(upCount, downCount)
					savedSequence = getSequence1[:-minUpDown] + getSequence2[minUpDown:]
					movementResults[firstWord + " " + secondWord] = savedSequence

					movementVector = None
					upDownCount = 0
					# saves into highly dimensional vectors
					for eachDirection in savedSequence:	
						if eachDirection == "up":
							if movementVector == None:
								movementVector = upVector
								upDownCount += 1
							else:
								movementVector *= np.concatenate([upVector[upDownCount:], upVector[:upDownCount]])
								upDownCount += 1
						elif eachDirection == "down":
							if movementVector == None:
								movementVector = downVector
								upDownCount += 1
							else:
								movementVector *= np.concatenate([downVector[upDownCount:], downVector[:upDownCount]])
								upDownCount += 1

					firstWordOG = firstWord
					secondWordOG = secondWord
					if firstWord in nonUniqueWords:
						firstWordOG = nonUniqueWords[firstWord]
					if secondWord in nonUniqueWords:
						secondWordOG = nonUniqueWords[secondWord]

					lexicalVectors[firstWordOG] += environmentVectors[secondWordOG] * posVectors[secondWordPos] * movementVector

		print("MOVEMENT RESULTS", movementResults)
		parsedTree = ""
	
	text.close()
	return posVectors, environmentVectors, lexicalVectors

def grabAnalogy(concept1, concept2, analogousTo, lexicalVectors, environmentVectors, numResults=1):
	f = lexicalVectors[concept1] * lexicalVectors[concept2]
	analogyResults = {}
	for word in environmentVectors:
		if word != analogousTo:
			analogyResults[word] = np.dot(environmentVectors[word],	environmentVectors[analogousTo] * f)

	print(analogyResults)
	results = []
	for i in range(numResults):
		word = max(analogyResults, key=analogyResults.get)

		results.append((word, analogyResults[word]))
		analogyResults.pop(word)

	return results

if __name__ == "__main__":
	posVectors = {}
	environmentVectors = {}
	lexicalVectors = {}
	upVector = np.random.choice([-1, 1], size=10000)
	downVector = np.random.choice([-1, 1], size=10000)

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test2.txt', posVectors, environmentVectors, lexicalVectors, upVector, downVector)

	posVectors, environmentVectors, lexicalVectors = addTreeBank('data/catDog.txt', posVectors, environmentVectors, lexicalVectors, upVector, downVector)
	result = grabAnalogy('dog', 'cat', 'purr', lexicalVectors, environmentVectors)
	print("analogy of cat:purr is dog:", result)
	print(lexicalVectors["dog"])