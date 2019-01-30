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

		parsedTree += line
		if "(. .)" not in line and "(: ;)" not in line and "(. ?)" not in line:
			continue

		# the end of the parsedTree has been reached
		tokenized = list(filter(None, parsedTree.replace("\n", "").split(" ")))

		# saves words and their part of speech
		wordsToSave = [] # FLAG... need to maintain order
		for count, token in enumerate(tokenized):

			# if there is a lowercase letter, there's a word
			if any(letter.islower() for letter in token):
				pos = tokenized[count-1].replace("(", "").replace(" ", "")
				word = token.replace(")", "").replace(" ", "").lower()
				# print(pos, word)

				if word not in stopwords:
					wordsToSave.append((word, pos)) # FLAG... need to maintain order
					if word not in environmentVectors:
						environmentVectors[word] = np.random.choice([-1, 1], size=10000)

		# print(wordsToSave)
		# addes context vectors * part of speech vector
		for index in range(len(wordsToSave)):
			word = wordsToSave[index][0]

			if word not in lexicalVectors:
				lexicalVectors[word] = np.zeros(10000)


			windowSize = 100
			# try getting the left hand side word into lexicalVector
			try:
				for n in range(windowSize):
					leftHandWord = wordsToSave[index-windowSize][0]
					leftHandPos = wordsToSave[index-windowSize][1]

					if leftHandPos not in posVectors:
						posVectors[leftHandPos] = np.random.choice([-1, 1], size=10000)

					lexicalVectors[word] += environmentVectors[leftHandWord] * posVectors[leftHandPos]
			except:
				pass

			# try getting the right hand side into lexicalVector
			try:
				for n in range(windowSize):
					rightHandWord = wordsToSave[index+windowSize][0]
					rightHandPos = wordsToSave[index+windowSize][1]

					if rightHandPos not in posVectors:
						posVectors[rightHandPos] = np.random.choice([-1, 1], size=10000)

					lexicalVectors[word] += environmentVectors[rightHandWord] * posVectors[rightHandPos]
			except:
				pass

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

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/test.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# result = grabAnalogy('dog', 'cat', 'purr', lexicalVectors, environmentVectors)
	# print("analogy of cat:purr is dog:", result)

	# posVectors, environmentVectors, lexicalVectors = addTreeBank('data/wsjExerpt.txt', posVectors, environmentVectors, lexicalVectors, stopWords)
	# results = grabAnalogy('trader', 'official', 'veteran', lexicalVectors, environmentVectors, 4)
	# print("analogy of industrial:average is points:")
	# for result in results:
	# 	print(result)

	posVectors, environmentVectors, lexicalVectors = addTreeBank('data/bnc_1000_gold_trees_09', posVectors, environmentVectors, lexicalVectors, stopWords)

	# count = 0
	# for folder in os.listdir("data/wsj"):
	# 	for file in os.listdir("data/wsj/" + str(folder)):
	# 		posVectors, environmentVectors, lexicalVectors = addTreeBank("data/wsj/" + str(folder) + "/" + file, posVectors, environmentVectors, lexicalVectors, stopWords)
	# 		print("done with", "data/wsj/" + str(folder) + "/" + file)
	# 	print("\n\nFOLDER", folder, "done\n\n")
	# 	count += 1
	# 	if count == 3:
	# 		break

	addTreeBank('data/bnc_1000_gold_trees_09', posVectors, environmentVectors, lexicalVectors, stopWords)

	results = {}
	f = lexicalVectors["composers"]

	for word in environmentVectors:
		results[word] = np.dot(environmentVectors[word],	lexicalVectors["composers"] * posVectors["NN"])

	newResults = []
	for i in range(10):
		word = max(results, key=results.get)

		newResults.append((word, results[word]))
		results.pop(word)

	print(newResults)

	# print("Done loading treebanks!")
	# print("----------------------------------------------\n\n\n")
	# print("Format: concept1: idea1 :: concept2: idea2.")
	# print("\n\n\n----------------------------------------------")

	# keepRolling = True
	# transpose = False

	# while keepRolling:
	# 	concept1 = input("Please enter concept1: \n").lower()
	# 	idea1 = input("Please enter idea1: \n").lower()
	# 	concept2 = input("Please enter concept2: \n").lower()
	# 	numResults = input("How many results?\n")

	# 	try:
	# 		results = grabAnalogy(concept1, concept2, idea1, lexicalVectors, environmentVectors, int(numResults))
	# 		print(concept1 + ": " + idea1 + " :: " + concept2 + ": \n")
	# 		for result in results:
	# 			print(result)

	# 	except Exception:
	# 	    traceback.print_exc()
		
	# 	print("\n")


	# with open('output/vectors.txt', 'w') as writeLexicon:
	# 	for vector in lexicalVectors:
	# 		string = str(vector)
	# 		for number in lexicalVectors[vector]:
	# 			string += " " + str(number)
	# 		writeLexicon.write(string + "\n")