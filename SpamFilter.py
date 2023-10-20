import re
import math


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
    spamTrain = getMessages("data/DSResume.txt")
    hamTrain = getMessages("data/OtherResumes.txt")
    print("Lengths:", len(spamTrain), len(hamTrain))

    wc = getWordCount(spamTrain, hamTrain)

    print(len(wc))

    k = .75
    minCount = .25

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
    lst = [(probSpam / (probSpam + probNotSpam), word)
           for word, probSpam, probNotSpam in word_probs]
    return sorted(lst)[-n:]


def leastSpammy(word_probs, n):
    lst = [(probNotSpam / (probSpam + probNotSpam), word)
           for word, probSpam, probNotSpam in word_probs]
    return sorted(lst)[-n:]


def filterProbs(wordProbs, n):
    most = [w for p, w in mostSpammy(wordProbs, n)]
    least = [w for p, w in leastSpammy(wordProbs, n)]
    return [(word, probSpam, probNotSpam)
            for word, probSpam, probNotSpam in wordProbs
            if word in most or word in least]


def getSpamProb(message, word_probs):
    logProbSpam = 0
    logProbNotSpam = 0
    # print(message)

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
    spamTest = getMessages("data/DSResumes.txt")
    hamTest = getMessages("data/OtherResumes.txt")

    goodHam = 0
    goodSpam = 0

    for msg in hamTest:
        if getSpamProb(msg, probs) <= .5:
            goodHam += 1

    for msg in spamTest:
        if getSpamProb(msg, probs) > .5:
            goodSpam += 1

    print("Classified as DS", goodHam, goodHam / len(hamTest))
    print("Classified as Other", goodSpam, goodSpam / len(spamTest))

classify()


def keyword_classifier(resume_list, keywords):
    classified_as_DS = 0

    for resume in resume_list:
        if any(keyword in resume for keyword in keywords):
            classified_as_DS += 1

    return classified_as_DS

#testing with sample keywords
keywords = ['data', 'machine', 'learning', 'python', 'statistics']
unknown_resumes = getMessages("data/UnknownResumes.txt")
classified_as_DS = keyword_classifier(unknown_resumes, keywords)
print("Keyword Classified as DS:", classified_as_DS)


def extract_phone_numbers(text):
    pattern = re.compile(r'(\+?(\d{1,3})?[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?)\d{4}')
    return pattern.findall(text)

def extract_emails(text):
    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return pattern.findall(text)


def main():
	probs = Train()
	probs = filterProbs(probs, 100)

	# Naive Bayes Classification
	unknown_probs = classify(probs)

	# Keyword-based Classification
	classified_as_DS = keyword_classifier(unknown_resumes, keywords)
	print("Keyword Classified as DS:", classified_as_DS)

	# Extract Contact Info
	for index, prob in enumerate(unknown_probs):
		if prob > 0.5:  # DS Resume
			print("DS Resume - Phone Numbers:", extract_phone_numbers(unknown_resumes[index]))
		else:  # Other Resume
			print("Other Resume - Emails:", extract_emails(unknown_resumes[index]))


if __name__ == "__main__":
	main()
