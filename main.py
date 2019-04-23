import numpy as np
import os
import traceback

def generateStopWords(filepath):
	stopWords = set()
	with open(filepath) as text:
		for count, line in enumerate(text):	
			stopWords.add(line.replace("\n", ""))
	return stopWords



def addTreeBank(filePath, posVectors, environmentVectors, lexicalVectors, movementVectors):
	text = open(filePath)

	parsedTree = ""
	for count, line in enumerate(text):
		parsedTree += line

		if "(. .)" not in line and "(. ?)" not in line:
			continue

		print(parsedTree)
		print("end of parsedTree")
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
						environmentVectors[word] = np.random.choice([-1, 1], size=100000)
					if word not in lexicalVectors:
						lexicalVectors[word] = np.zeros(100000)
					if pos not in posVectors:
						posVectors[pos] = np.random.choice([-1, 1], size=100000)

					#reset sequence for next
					sequence = []
					oldDepth = 0
				
				if depth > oldDepth:
					sequence.append(depth)
					oldDepth = depth

		count = 0
		movementResults = {}
		# print(sentenceTuple)

		# stores sequences first
		for i in range(1, len(sentenceTuple)):
			firstWord = sentenceTuple[i-1][0]
			firstSequence = sentenceTuple[i-1][2]

			secondWord = sentenceTuple[i][0]
			secondWordPos = sentenceTuple[i][1]
			secondSequence = sentenceTuple[i][2]

			count = firstSequence[-1] - secondSequence[0]
			movement = ""

			for x in range(count):
				movement += "1"
			for x in range(len(secondSequence) - 1):
				movement += "0"

			movementResults[firstWord + " " + secondWord] = movement
			if movement not in movementVectors:
				movementVectors[movement] = np.random.choice([-1, 1], size=100000)
			movementVector = movementVectors[movement]

			if firstWord in nonUniqueWords:
				firstWord = nonUniqueWords[firstWord]
			if secondWord in nonUniqueWords:
				secondWord = nonUniqueWords[secondWord]

			# print("Saved lexicalVectors", firstWord, ":", secondWord)

			lexicalVectors[firstWord] += environmentVectors[secondWord] * posVectors[secondWordPos] * movementVector

		for i in range(len(sentenceTuple)):
			for j in range(len(sentenceTuple)):

				firstWord = sentenceTuple[i][0]
				secondWord = sentenceTuple[j][0]
				secondWordPos = sentenceTuple[j][1]

				movement = ""
				# check that it's not the same word
				if firstWord == secondWord or (firstWord + " " + secondWord) in movementResults:
					continue
				# check if flipped exists
				elif secondWord + " " + firstWord in movementResults:
					for direction in movementResults[secondWord + " " + firstWord]:
						if direction == "1":
							movement = "0" + movement
						else:
							movement = "1" + movement

					movementResults[firstWord + " " + secondWord] = movement
					if movement not in movementVectors:
						movementVectors[movement] = np.random.choice([-1, 1], size=100000)
					movementVector = movementVectors[movement]

					if firstWord in nonUniqueWords:
						firstWord = nonUniqueWords[firstWord]
					if secondWord in nonUniqueWords:
						secondWord = nonUniqueWords[secondWord]

					lexicalVectors[firstWord] += environmentVectors[secondWord] * posVectors[secondWordPos] * movementVector

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
					for upDown in getSequence1:
						if upDown == "0":
							downCount += 1
					for upDown in getSequence2:
						if upDown == "1":
							upCount += 1

					minUpDown = min(upCount, downCount)
					movement = getSequence1[:-minUpDown] + getSequence2[minUpDown:]
					movementResults[firstWord + " " + secondWord] = movement
					if movement not in movementVectors:
						movementVectors[movement] = np.random.choice([-1, 1], size=100000)
					movementVector = movementVectors[movement]

					if firstWord in nonUniqueWords:
						firstWord = nonUniqueWords[firstWord]
					if secondWord in nonUniqueWords:
						secondWord = nonUniqueWords[secondWord]

					lexicalVectors[firstWord] += environmentVectors[secondWord] * posVectors[secondWordPos] * movementVector

		# print("MOVEMENT RESULTS", movementResults)
		parsedTree = ""
	
	text.close()
	return posVectors, environmentVectors, lexicalVectors, movementVectors

def grabAnalogy(concept1, concept2, analogousTo, lexicalVectors, environmentVectors, numResults=1):
	concept1 = concept1.lower()
	concept2 = concept2.lower()
	analogousTo = analogousTo.lower()

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
	movementVectors = {}

	# posVectors, environmentVectors, lexicalVectors, movementVectors = addTreeBank('data/catDog.txt', posVectors, environmentVectors, lexicalVectors, movementVectors)
	# result = grabAnalogy('dog', 'cat', 'purr', lexicalVectors, environmentVectors)
	# print("analogy of cat:purr is dog:", result)

	posVectors, environmentVectors, lexicalVectors, movementVectors = addTreeBank('data/bnc_gold_test.txt', posVectors, environmentVectors, lexicalVectors, movementVectors)

	# result = grabAnalogy('Steve', 'George', 'McQueen', lexicalVectors, environmentVectors, 20)
	# print("analogy of Steve:McQueen is George:", result)

	# posVectors, environmentVectors, lexicalVectors, movementVectors = addTreeBank('data/test3.txt', posVectors, environmentVectors, lexicalVectors, movementVectors)


	print("Done loading treebanks!")
	print("----------------------------------------------\n\n\n")
	print("Format: concept1: idea1 :: concept2: idea2.")
	print("\n\n\n----------------------------------------------")

	keepRolling = True
	while keepRolling:
		concept1 = input("Please enter concept1: \n").lower()
		idea1 = input("Please enter idea1: \n").lower()
		concept2 = input("Please enter concept2: \n").lower()
		numResults = input("How many results?\n")

		try:
			results = grabAnalogy(concept1, concept2, idea1, lexicalVectors, environmentVectors, int(numResults))
			print(concept1 + ": " + idea1 + " :: " + concept2 + ": \n")
			for result in results:
				print(result)

		except Exception:
		    traceback.print_exc()
		
		print("\n")


	# with open('output/vectors.txt', 'w') as writeLexicon:
	# 	for vector in lexicalVectors:
	# 		string = str(vector)
	# 		for number in lexicalVectors[vector]:
	# 			string += " " + str(number)
	# 		writeLexicon.write(string + "\n")