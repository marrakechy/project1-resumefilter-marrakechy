import re
import math


def tokenize(message):
    message = message.lower()
    words = re.findall(r'[a-z0-9]+', message)

    return set(words);

keywords = ['python', 'statistics', 'machine learning', 'data', 'analytics']


def getMessages(fname):
    with open(fname, encoding='utf-8') as infile:
        data = [msg.strip() for msg in infile]
    return data

def single_keyword_classifier(keyword, messages):
    classified_as_DS = sum(keyword in tokenize(message) for message in messages)
    return classified_as_DS

#calculate accuracy for each keyword:
DS_messages = getMessages("data/DSResumes.txt")
Other_messages = getMessages("data/OtherResumes.txt")

for keyword in keywords:
    DS_classified = single_keyword_classifier(keyword, DS_messages)
    Other_classified = len(Other_messages) - single_keyword_classifier(keyword, Other_messages)
    total_DS = len(DS_messages)
    total_Other = len(Other_messages)
    accuracy_DS = DS_classified / total_DS
    accuracy_Other = Other_classified / total_Other
    print(f"Keyword: {keyword}, accuracy on DS: {accuracy_DS:.2f}, accuracy on Other: {accuracy_Other:.2f}")


def multi_keyword_classifier(keywords, messages):
    classified_as_DS = sum(any(k in tokenize(message) for k in keywords) for message in messages)
    return classified_as_DS

DS_classified = multi_keyword_classifier(keywords, DS_messages)
Other_classified = len(Other_messages) - multi_keyword_classifier(keywords, Other_messages)
accuracy_DS = DS_classified / total_DS
accuracy_Other = Other_classified / total_Other
print(f"Multi-keyword Classifier, accuracy on DS: {accuracy_DS:.2f}, accuracy on Other: {accuracy_Other:.2f}")

def getMessages(fname):
    with open(fname, encoding='utf-8') as infile:
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
    spamTrain = getMessages("data/DSResumes.txt")
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


# def keyword_classifier(resume_list, keywords):
#     classified_as_DS = 0
#
#     for resume in resume_list:
#         if any(keyword in resume for keyword in keywords):
#             classified_as_DS += 1
#
#     return classified_as_DS
#
# #testing with sample keywords
# keywords = ['data', 'machine', 'learning', 'python', 'statistics']
# unknown_resumes = getMessages("data/UnknownResumes.txt")
# classified_as_DS = keyword_classifier(unknown_resumes, keywords)
# print("Keyword Classified as DS:", classified_as_DS)
#
#
# def extract_phone_numbers(text):
#     pattern = re.compile(r'(\+?(\d{1,3})?[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?(\d{3}[-.\s]?)\d{4}')
#     return pattern.findall(text)
#
# def extract_emails(text):
#     pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
#     return pattern.findall(text)
#
#
# def main():
# 	probs = Train()
# 	probs = filterProbs(probs, 100)
#
# 	# Naive Bayes Classification
# 	unknown_probs = classify(probs)
#
# 	# Keyword-based Classification
# 	classified_as_DS = keyword_classifier(unknown_resumes, keywords)
# 	print("Keyword Classified as DS:", classified_as_DS)
#
# 	# Extract Contact Info
# 	for index, prob in enumerate(unknown_probs):
# 		if prob > 0.5:  # DS Resume
# 			print("DS Resume - Phone Numbers:", extract_phone_numbers(unknown_resumes[index]))
# 		else:  # Other Resume
# 			print("Other Resume - Emails:", extract_emails(unknown_resumes[index]))
#
#
# if __name__ == "__main__":
# 	main()
