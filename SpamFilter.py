import re
import math
import os


def tokenize(message):

	message = message.lower()
	words = re.findall(r'[a-z0-9]+', message)
	return set(words);

def getMessages(fname):
	with open(fname) as infile:
		data = [msg.strip() for msg in infile]
	return data

def getWordCount(spam, ham):
	# spam is list of spam messages
	# ham is list of ham messages
	# return dictionary: {word: [spamCnt, hamCnt]}
	wordCount = {}
	for msg in spam:
		for word in tokenize(msg):
			try:
				wordCount[word][0] += 1
			except KeyError:
				wordCount[word] = [1, 0]
	for msg in ham:
		for word in tokenize(msg):
			try:
				wordCount[word][1] += 1
			except KeyError:
				wordCount[word] = [0, 1]
	return wordCount

def Train():
	spamTrain = getMessages("data/SpamText_train.txt")
	hamTrain = getMessages("data/hamText_train.txt")
	print("Lengths:", len(spamTrain), len(hamTrain))

	wc = getWordCount(spamTrain, hamTrain)

	print(len(wc))

	k = .5
	minCount = 5

	''' 
	Make a list of tuples:  
		word
		probability word appears in spam messsage
		probability word appears in ham message
		
		k ensures we don't have zero value (just a little noise)
		
		only include if the word occurs in at least 
		minCount messages.
		
	'''

	probs = [(w,
			  (spam + k) / (len(spamTrain) + 2 * k),
			  (ham + k) / (len(hamTrain) + 2 * k))
			 for w, (spam, ham) in wc.items()
			 if spam > minCount or ham > minCount]
	return probs

def mostSpammy(word_probs, n):
	lst = [(probSpam/(probSpam+probNotSpam), word)
		for word, probSpam, probNotSpam in word_probs]
	return sorted(lst)[-n:]

def leastSpammy(word_probs,n):
	lst = [(probNotSpam / (probSpam + probNotSpam), word)
		   for word, probSpam, probNotSpam in word_probs]
	return sorted(lst)[-n:]

def filterProbs(wordProbs, n):
	most = [w for p,w in mostSpammy(wordProbs,n)]
	least = [w for p,w in leastSpammy(wordProbs,n)]
	return [(word, probSpam, probNotSpam)
			for word, probSpam, probNotSpam in wordProbs
			if word in most or word in least]

def getSpamProb(message, word_probs):
	logProbSpam = 0
	logProbNotSpam = 0
	#print(message)

	'''
	We want to avoid an 'underflow' -- when the number becomes so small
	it get rounded to 0.   Multiplying a lot of small numbers is a great
	way to get an underflow.   We avoid this by adding logs.  Remember
	log(ab) = log(a) + log(b)
	and
	exp(log(a)) = a
	
	'''

	for word, probSpam, probNotSpam in word_probs:
			if word in message:
				logProbSpam += math.log(probSpam)
				logProbNotSpam += math.log(probNotSpam)
			else:
				logProbSpam += math.log(1 - probSpam)
				logProbNotSpam += math.log(1 - probNotSpam)
	probSpam = math.exp(logProbSpam)
	probNotSpam = math.exp(logProbNotSpam)

	return probSpam / (probSpam + probNotSpam)

def classify():
	probs = Train()
	probs = filterProbs(probs, 100)
	print("Len Probs: ", len(probs))
	spamTest = getMessages("data/spamText_test.txt")
	hamTest = getMessages("data/hamText_test.txt")

	goodHam = 0
	goodSpam = 0

	for msg in hamTest:
		if getSpamProb(msg, probs) <= .5:
			goodHam +=1

	for msg in spamTest:
		if getSpamProb(msg, probs) > .5:
			goodSpam +=1

	print("Good Ham", goodHam, goodHam/len(hamTest))
	print("Good Spam", goodSpam, goodSpam / len(spamTest))

classify()

def split_train_test(data, split_ratio=0.75):
	train_num = int(len(data) * split_ratio)
	return data[:train_num], data[train_num:]

def keyword_classifier(text, keywords):
	for keyword in keywords:
		if keyword in text:
			return "DS"
	return "Other"

def extract_phone(text):
	pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
	match = pattern.search(text)
	return match.group() if match else None

def extract_email(text):
	pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')
	match = pattern.search(text)
	return match.group() if match else None


def save_to_file(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            if item:  # Ensure we're not saving None values
                f.write("%s\n" % item)

if __name__ == "__main__":
	# Load and split data
	ds_texts = getMessages("DSResumes.txt")
	other_texts = getMessages("OtherResumes.txt")

	ds_train, ds_test = split_train_test(ds_texts)
	other_train, other_test = split_train_test(other_texts)

	word_counts = getWordCount(ds_train, other_train)
	probs = Train()

	ds_keywords = ["Machine learning", "Data Science", "Natural Language Processing"]
	classified_as_ds = []
	classified_as_other = []

	for resume in known_texts:
		if keyword_classifier(resume, ds_keywords) == "DS":
			classified_as_ds.append(resume)
		else:
			classified_as_other.append(resume)


	ds_phone_numbers = [extract_phone(resume) for resume in classified_as_ds]
	other_emails = [extract_email(resume) for resume in classified_as_other]

	save_to_file("ds_phone_numbers.txt", ds_phone_numbers)
	save_to_file("other_emails.txt", other_emails)


