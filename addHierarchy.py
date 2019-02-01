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

		# the end of the parsedTree has been reached
		print(parsedTree)
		depth = 0

		parsedTree = parsedTree.split("\n")

		sequence = []
		sentenceTuple = []
		for line in parsedTree:
			tokenizedLine = list(filter(None, line.replace("\n", "").split(" ")))
			# print(tokenizedLine)
			oldDepth = 0
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
					# print(word, oldDepth)
				sequence.append(depth)
				oldDepth = depth

		print(sentenceTuple)

		movementResults = []
		movementResultsDict = {}
		movement = []

		count = 0
		for i in range(len(sentenceTuple)):
			word = sentenceTuple[i][0]
			pos = sentenceTuple[i][1]
			sequence = sentenceTuple[i][2]

			print(word, pos, sequence)

			firstOne = True
			skip = False
			for j in range(len(sentenceTuple)):
				secondWord = sentenceTuple[j][0]
				print(word, secondWord)
				# not the same word, then skip
				if secondWord == word:
					continue
				secondSequence = sentenceTuple[j][2]

				# if second word comes before first word and is already stored.
				testFlipped = secondWord + " " + word
				if testFlipped in movementResultsDict:
					print("THIS SHOULD NOT HAVE TRIGGERED")
					newMovement = []
					for eachMotion in movementResultsDict[testFlipped]:
						if eachMotion == "up":
							newMovement = ['down'] + newMovement
						else:
							newMovement = ['up'] + newMovement

					# REPLACE THIS WITH THE 10K DIMENSIONAL VECTORS
					movementResults.append((word, secondWord, newMovement))

				# It hasn't been stored yet, need to generate
				else:
					# last depth - new depth
					count = sentenceTuple[j-1][2][-1] - sentenceTuple[j][2][0]
					# print(count)
					if count < 0:
						continue

					upCount = 0
					# how many steps you have to go up
					for x in range(count):
						if skip:
							skip = False
						else:
							movement.append("up")

					# len - 1 = how many times it goes down
					for x in range(len(secondSequence) - 1):
						movement.append("down")

					tmpMovement = movement.copy()
					movementResults.append((word, secondWord, tmpMovement))
					movementResultsDict[word + " " + secondWord] = movement

					# the last down is always unecessary
					movement = movement[:-1]
					skip = True
					# print(movement)

					# DELETE LATER
					# count += 1
					# print(movementResults)
					
					# if count == 4:
					# 	exit()
			
			movement = []
			print(movementResults)
			# print(movementResultsDict)
			print("\n")

			# exit()

		exit()

	text.close()
	return posVectors, environmentVectors, lexicalVectors

if __name__ == "__main__":
	stopWords = generateStopWords('stopwords.txt')
	posVectors = {}
	environmentVectors = {}
	lexicalVectors = {}

	posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# results = grabAnalogy('industrial', 'senior', 'average', lexicalVectors, environmentVectors)
	# for result in results:
		# print(result)