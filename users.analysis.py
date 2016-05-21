# affinity analysis for news article features and user data associated with them

import numpy as np
from keen.client import KeenClient
from collections import defaultdict

# set keen.io keys
def get_keen_client():
	return KeenClient(
		project_id = "",
		write_key = "",
		read_key = ""
)

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

# print(X[:100]) # quantity of users and their data

# we'd like to be able to get our users who like an article to share that article
print("{0} people liked an article".format(num_article_likes)) # data condition match
print("{0} people shared an article".format(num_article_shares)) # data condition match

# compute the confidence and support for all possible rules:
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


def print_rule(the_premise, the_conclusion, the_support, the_confidence, features):
	premise_name = features[the_premise]
	conclusion_name = features[the_conclusion]
	print("Rule 1: If a person likes an {0} they will also share that {1}".format(premise_name, conclusion_name))
	print(" - Support: {0}".format(support[(the_premise, the_conclusion)]))
	print(" - Confidence: {0:.3f}".format(confidence[(the_premise, the_conclusion)]))
	# send data off to keen.io
	client = get_keen_client()
	client.add_event("affinity_analysis", {
		"likes": num_article_likes,
		"shares": num_article_shares,
		"support": the_support[(the_premise, the_conclusion)],
		"confidence": format(the_confidence[(the_premise, the_conclusion)], ".3f")
	})

premise = 0 # if a person liked an article,
conclusion = 1 # that person will also share that article.
print_rule(premise, conclusion, support, confidence, ("article", "article", "article", "article", "article"))
