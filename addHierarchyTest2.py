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
		# print(parsedTree)
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

		count = 0
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

		for i in range(len(sentenceTuple)):

			for j in range(len(sentenceTuple)):

				firstWord = sentenceTuple[i][0]
				secondWord = sentenceTuple[j][0]

				# check that it's not the same word
				if firstWord == secondWord or (firstWord + " " + secondWord) in movementResults:
					continue

				elif secondWord + " " + firstWord in movementResults:
					newMovement = []

					for direction in movementResults[secondWord + " " + firstWord]:
						if direction == "up":
							newMovement = ['down'] + newMovement
						else:
							newMovement = ['up'] + newMovement

					movementResults[firstWord + " " + secondWord] = newMovement

				else:

					sequence1Base = False
					sequence2Base = False

					print(firstWord + " " + secondWord)
					savedSequence = []
					
					print(sentenceTuple[i][0] + " " + sentenceTuple[j-1][0])
					print(movementResults[sentenceTuple[i][0] + " " + sentenceTuple[j-1][0]])
					getSequence1 = movementResults[sentenceTuple[i][0] + " " + sentenceTuple[j-1][0]]

					print(sentenceTuple[j-1][0] + " " + sentenceTuple[j][0])
					print(movementResults[sentenceTuple[j-1][0] + " " + sentenceTuple[j][0]])
					getSequence2 = movementResults[sentenceTuple[j-1][0] + " " + sentenceTuple[j][0]]

					# saves the two cases where if one is up down, just store the other one.
					if getSequence1 == ['up', 'down']:
						if getSequence2 != ['up', 'down']:
							savedSequence = getSequence2
						# if both are up / down... then just store up/down here
						else:
							savedSequence = ['up', 'down']

						print("result", savedSequence)
						print("\n")

					elif getSequence1 != ['up', 'down'] and getSequence2 == ['up', 'down']:
							savedSequence = getSequence1

							print("result", savedSequence)
							print("\n")

					# now both of them are not up/down, so I need to concatenate them.
					else:
						downCount = 0
						for count, upDown in enumerate(getSequence1):
							if upDown == "down":
								downCount += 1

						upCount = 0
						for count, upDown in enumerate(getSequence2):
							if upDown == "up":
								upCount += 1

						minUpDown = min(upCount, downCount)
						print(minUpDown)

						# i.e. if downCount = 3, then 3 items need to be skipped, so start on 3rd index
						getSequence1 = getSequence1[:-minUpDown]
						print("chopped getSequence1", getSequence1)

						getSequence2 = getSequence2[minUpDown:]
						print("chopped getSequence2", getSequence2)

						savedSequence = getSequence1 + getSequence2

						print("result", savedSequence)
						print("\n")

						count += 1
						if count >= 7:
							exit()

					movementResults[firstWord + " " + secondWord] = savedSequence

					# count += 1
					# if count == 10:
					# 	exit()

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