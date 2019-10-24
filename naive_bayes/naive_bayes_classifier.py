import glob
import math
import os

ALPHA = 0.05
V = 200000

"""
Counts the number of words in each email and returns a dictionary of word counts as well as the total count of words.
"""
def count_words(directory):
    words = {}
    count = 0
    for filename in glob.glob(directory):
        f = open(filename)
        for line in f.readlines():
            line = line.strip("\n")
            if line not in words:
                words[line] = 1
            else:
                words[line] += 1
            count += 1
    return words, count

"""
Runs the naive bayes model by adding to the total probability of ham and spam, respectively.
Returns a dictionary containing a mapping of the file name to the model classification and the truth.
Also returns the accuracy of the model.

"""

def run_model(directory, spam, prob_spam, prob_unseen_spam, ham, prob_ham, 
                prob_unseen_ham, truth_table):
    classification = {}
    differences = 0
    total_email = 0

    for email in glob.glob(directory):
        total_prob_ham = 0
        total_prob_spam = 0
        f = open(email)

        for word in f.readlines():
            word = word.strip("\n")
            if word not in ham:
                total_prob_ham += prob_unseen_ham
            else:
                total_prob_ham += ham[word]

            if word not in spam:
                total_prob_spam += prob_unseen_spam
            else:
                total_prob_spam += spam[word]

        email = email.split("/")
        email = email[len(email) - 1].strip(".words")

        if email in truth_table:
            truth = "Spam"
        else:
            truth = "Ham"

        if total_prob_ham > total_prob_spam:
            generated = "Ham"
            classification[email] = {"classification": generated, "truth": truth}
        else:
            generated = "Spam"
            classification[email] = {"classification": generated, "truth": truth}
        
        if generated != truth:
            differences += 1
        total_email += 1

    return classification, 1 - (differences/total_email)

"""
Extracts the names of the files that should be "Spam". 
Returns a set with the files that should be classified as "Spam."
"""
def populate_truth(directory):
    truth = set()

    for filename in glob.glob(directory):
        f = open(filename)
        for line in f.readlines():
            line = line.strip("\n")
            truth.add(line)
    return truth

"""
Calculates the probabilities necessary to implement the Naive Bayes classifier.
Adds the P(word|class) to the dictionary of words and returns P(class) and P(unseen_word) 
"""
def calculate_probabilities(total_words, total_class, words, is_ham=False):
    for word in words:
        curr_count = words[word] + ALPHA
        log_prob = math.log(curr_count/(total_class + (V * ALPHA)))
        words[word] = log_prob
    
    prob_class = math.log(total_class/total_words)
    prob_unseen_class = ALPHA/(total_class +(V*ALPHA))
    prob_unseen_class = math.log(prob_unseen_class)

    return prob_class, prob_unseen_class

"""
After the classifier is run, obtains the metrics of precision, recall, and f-score as well as the confusion matrix.
Returns confusion matrix and metrics as two separate dictionaries.
"""
def get_metrics(results):
    "Assuming Ham is positive and Spam is negative"
    positive = "Ham"
    negative = "Spam"
    confusion_matrix = {"TP": 0, "TN": 0, "FP": 0, "FN": 0}

    for val in results.values():
        if val["truth"] == positive:
            if val["classification"] == positive:
                confusion_matrix["TP"] += 1
            else:
                confusion_matrix["FN"] += 1

        else:
            if val["classification"] == negative:
                confusion_matrix["TN"] += 1
            else:
                confusion_matrix["FP"] += 1
    metrics = {}

    metrics["precision"] = confusion_matrix["TP"] / (confusion_matrix["TP"] + confusion_matrix["FP"])
    metrics["recall"] = confusion_matrix["TP"] / (confusion_matrix["TP"] + confusion_matrix["FN"])

    metrics["f_score"] = \
        (2 * metrics["recall"] * metrics["precision"]) / (metrics["precision"] + metrics["recall"])
  
    return confusion_matrix, metrics

def main():
    ham = "*/data/ham/*"
    spam = "*/data/spam/*"
    test = "*/data/test/*"
    truth_file = "*/data/truthfile*"

    dict_ham, total_ham = count_words(ham)
    dict_spam, total_spam = count_words(spam)
    total_words = total_ham + total_spam

    prob_ham, prob_unseen_ham = calculate_probabilities(total_words, total_ham, dict_ham, True)
    prob_spam, prob_unseen_spam = calculate_probabilities(total_words, total_spam, dict_spam)

    truth_table = populate_truth(truth_file)

    results, accuracy = run_model(test, dict_spam, prob_spam, prob_unseen_spam, 
                                    dict_ham, prob_ham, prob_unseen_ham, truth_table)
    
    print("Accuracy: " + str(accuracy))
    print(get_metrics(results))




main()

