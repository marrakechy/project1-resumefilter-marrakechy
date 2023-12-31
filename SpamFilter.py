import re
import math
import PyPDF2


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



def classify_with_multi_keywords(keywords, messages):
    classified_as_DS = sum(any(k in tokenize(message) for k in keywords) for message in messages)
    return classified_as_DS


def classify_unknown_with_multi_keywords():

    unknown_resumes = getMessages("data/UnknownResumes.txt")

    #ssing the multi-keyword classifier on unknown resumes
    DS_classified_unknown = classify_with_multi_keywords(keywords, unknown_resumes)
    Other_classified_unknown = len(unknown_resumes) - DS_classified_unknown

    print(f"Using Multi-keyword Classifier:")
    print(f"Total Resumes in UnknownResumes.txt: {len(unknown_resumes)}")
    print(f"Total Resumes classified as DS: {DS_classified_unknown}")
    print(f"Total Resumes classified as Other: {Other_classified_unknown}")

classify_unknown_with_multi_keywords()


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


def extract_phone_number(message):
    phone_patterns = [
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]?\d{4}'
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, message)
        if match:
            return match.group()
    return match.group() if match else None

def extract_email(message):
    email_pattern =  r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    match = re.search(email_pattern, message)
    if match:
        return match.group()
    return match.group() if match else None


def read_pdf_content(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        content = ""
        for page_num in range(len(reader.Pages)):
            content += reader.pages[page_num].extractText()
    return content


def classify_unknown_resumes():
    #train the classifier using DS and Other resumes
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

    #load unknown resumes
    unknown_resumes = getMessages("data/UnknownResumes.txt")

    ds_classified_without_phone = []
    other_classified_without_email = []
    not_extracted_resumes = []
    ds_count = 0
    other_count = 0

    for msg in unknown_resumes:
        #if the message is classified as DS
        if getSpamProb(msg, probs) > .5:
            ds_count += 1
            phone_number = extract_phone_number(msg)
            if not phone_number:
                ds_classified_without_phone.append(msg)
            else:
                print("Classified as DS with phone number:", phone_number)

        #if the message is classified as Other
        if getSpamProb(msg, probs) <= .5:
            other_count += 1
            email = extract_email(msg)
            if not email:
                other_classified_without_email.append(msg)
            else:
                print("classified as Other with email:", email)

    #identify resumes from which we couldn't extract the contact information
    not_extracted_resumes.extend(ds_classified_without_phone)
    not_extracted_resumes.extend(other_classified_without_email)

    print("Total Resumes in UnknownResumes.txt:", len(unknown_resumes))
    print("Total Resumes classified as DS:", ds_count)
    print("Total Resumes classified as Other:", other_count)
    print("Resumes classified as DS without phone numbers:", len(ds_classified_without_phone))
    print("Resumes classified as Other without emails:", len(other_classified_without_email))
    print("Resumes from which contact information couldn't be extracted:", len(not_extracted_resumes))

classify_unknown_resumes()

# def classify():
#     probs = Train()
#     probs = filterProbs(probs, 100)
#     print("Len Probs: ", len(probs))
#     spamTest = getMessages("data/DSResumes.txt")
#     hamTest = getMessages("data/OtherResumes.txt")
#
#     goodHam = 0
#     goodSpam = 0
#
#     for msg in hamTest:
#         if getSpamProb(msg, probs) <= .5:
#             goodHam += 1
#
#     for msg in spamTest:
#         if getSpamProb(msg, probs) > .5:
#             goodSpam += 1
#
#     print("Classified as DS", goodHam, goodHam / len(hamTest))
#     print("Classified as Other", goodSpam, goodSpam / len(spamTest))
#
# classify()







