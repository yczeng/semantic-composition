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
		print(line)
		parsedTree += line

		if "(. .)" not in line and "(. ?)" not in line:
			continue

		# the end of the parsedTree has been reached
		print(parsedTree)
		depth = 0
		oldDepth = 0

		parsedTree = parsedTree.split("\n")

		sequence = []
		sentenceTuple = []
		for line in parsedTree:
			tokenizedLine = list(filter(None, line.replace("\n", "").replace(" )", ")").split(" ")))
			# print(tokenizedLine)
			for count, item in enumerate(tokenizedLine):
				depth += item.count("(")
				depth -= item.count(")")
				
				word = item.replace(")", "").replace(" ", "").lower()
				if any(letter.islower() for letter in item):
					pos = tokenizedLine[count-1].replace("(", "").replace(" ", "")
					sentenceTuple.append((word, pos, sequence))

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

		print(sentenceTuple)

		# goal instead of getting everything at once, just get the words to work in sequence with each other

		movementResults = {}
		for i in range(1, len(sentenceTuple)):
			firstWord = sentenceTuple[i-1][0]
			firstSequence = sentenceTuple[i-1][2]

			secondWord = sentenceTuple[i][0]
			secondSequence = sentenceTuple[i][2]

			count = firstSequence[-1] - secondSequence[0]
			movement = []

			for x in range(count):
				movement.append("up")
			for x in range(len(secondSequence) - 1):
				movement.append("down")

			movementResults[firstWord + " " + secondWord] = movement

		print(movementResults)
		exit()
		text.close()
	return posVectors, environmentVectors, lexicalVectors

if __name__ == "__main__":
	stopWords = generateStopWords('stopwords.txt')
	posVectors = {}
	environmentVectors = {}
	lexicalVectors = {}

	posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)