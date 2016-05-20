# affinity analysis for news article features and user data associated with them

from keen.client import KeenClient

# set keen.io keys

import numpy as np

dataset_filename = "users.dataset.txt"
X = np.loadtxt(dataset_filename) # TODO: look into making this JSON instead of text...

# ex: article that has a video, a like button, a share button, 
# dataset: 5 items == liked, shared, scrolledToBottom, videoFinished, adClicked 

# support: support is the number of times a rule occurs in a dataset. (count the total of occurences)
# confidence: how accurate they are. (how valid is the rule we're trying to enforce) 

# if a user likes an article, they also share that article

# first, how many rows contain our premise: that a person is liking an article
num_article_likes = 0
num_article_shares = 0
for sample in X:
	if sample[0] == 1: # person liked an article
		num_article_likes += 1
	if sample[1] == 1: # person shared an article
		num_article_shares += 1

print(X[:5]) # quantity of users and their data

# we'd like to be able to get our users who like an article to share that article
print("{0} people liked an article".format(num_article_likes)) # data condition match
print("{0} people shared an article".format(num_article_shares)) # data condition match

# compute the confidence and support for all possible rules:

from collections import defaultdict

valid_rules = defaultdict(int)
invalid_rules = defaultdict(int)
num_occurences = defaultdict(int)

for sample in X:
	# premise in range(4) is referring to out of 5 pieces of data per user, 
	# we want to see if it happened: 1 or not: 0
	for premise in range(4): # config proper range for data
		if sample[premise] == 0: continue
		num_occurences[premise] += 1
		for conclusion in range(4):
			if premise == conclusion: continue
			if sample[conclusion] == 1:
				valid_rules[(premise, conclusion)] += 1
			else:
				invalid_rules[(premise, conclusion)] += 1

support = valid_rules # how many times did this really happen?
confidence = defaultdict(float)
for premise, conclusion in valid_rules.keys():
	rule = (premise, conclusion)
	confidence[rule] = valid_rules[rule] / num_occurences[premise]

def print_rule(premise, conclusion, support, confidence, features):
	premise_name = features[premise]
	conclusion_name = features[conclusion]
	print("Rule 1: If a person likes an {0} they will also share that {1}".format(premise_name, conclusion_name))
	print(" - Support: {0}".format(support[(premise, conclusion)]))
	print(" - Confidence: {0:.3f}".format(confidence[(premise, conclusion)]))
	# send data off to keen.io
	# keen.add.event("affinity_analysis", {
	# 	"num_article_likes": num_article_likes
	# 	"num_article_shares": num_article_shares 
	# 	"analysis_rule": "If a person likes an article, they will also share that article"
	# 	"user_support": support[(premise, conclusion)]
	# 	"rule_confidence": format(confidence[(premise, conclusion)], ".3f")
	# })

premise = 0 # if a person liked an article,
conclusion = 1 # that person will also share that article.
print_rule(premise, conclusion, support, confidence, ("article", "article", "article", "article", "article"))
