
# coding: utf-8

# # Distributional Similarity Practice
# 
# This practice sheet should help you gain a little familiarity with creating a distributional representation for a word, and how to query it later.
# 
# ## 1. Getting our Data
# 
# Our first step in creating a distributional representation for our vocabulary is to get our data set. This should be pretty familiar by now; find a resource with many sentences, and tokenize those sentences.
# 
# *(NOTE: You may need to first launch a python interpreter and run the following:)*
# 
#     >>> import nltk
#     >>> nltk.download('brown')

# In[2]:


import nltk
brown_sents = nltk.corpus.brown.sents()
print(brown_sents[0])


# ## 2. Designing Our Data Store
# 
# Now that we have the data that we'll be using for an input, we need to figure out the best way to store this data.
# 
# Our target structure will let us look up a pair of words, $\langle w_1, w_2 \rangle$ and see how many times $w_2$ occurred within some window $n$ of $w_1$.
# 
# A common, efficient way to store such information is to create a 2-dimensional matrix, where each row index is correlated to a unique vocabulary word which will be $w_1$, and every column index will represent $w_2$.
# 
# Let's go ahead and make a data structure that allows us to easily increment counts of collocations, as well as allow us to look up a unique ID for a word, whether we've seen it, or wheter it's a new vocab item. We can do this with a standard matrix, or with nested dictionaries, if we prefer.

# In[2]:


from collections import defaultdict

class CollocationMatrix(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._word_mapping = {}  # Where we'll store string->int mapping.        
    
    def word_id(self, word, store_new=False):
        """
        Return the integer ID for the given vocab item. If we haven't
        seen this vocab item before, give ia a new ID. We can do this just
        as 1, 2, 3... based on how many words we've seen before.
        """
        if word not in self._word_mapping:
            if store_new:
                self._word_mapping[word] = len(self._word_mapping)
                self[self._word_mapping[word]] = defaultdict(int)  # Also add a new row for this new word.
            else:
                return None
        return self._word_mapping[word]
    
    def add_pair(self, w_1, w_2):
        """
        Add a pair of colocated words into the coocurrence matrix.
        """
        w_id_1 = self.word_id(w_1, store_new=True)
        w_id_2 = self.word_id(w_2, store_new=True)
        self[w_id_1][w_id_2] += 1  # Increment the count for this collocation
        
    def get_pair(self, w_1, w_2):
        """
        Return the colocation for w_1, w_2
        """
        w_1_id = self.word_id(w_1)
        w_2_id = self.word_id(w_2)
        if w_1_id and w_2_id:
            return self[w_1_id][w_2_id]
        else:
            return 0
        
    def get_row(self, word):
        word_id = self.word_id(word)
        if word_id is not None:
            return self.get(word_id)
        else:
            return defaultdict(int)
    
    def get_row_sum(self, word):
        """
        Get the number of total contexts available for a given word        
        """
        return sum(self.get_row(word).values())
    
    def get_col_sum(self, word):
        """
        Get the number of total contexts a given word occurs in
        """
        f_id = self.word_id(word)
        return sum([self[w][f_id] for w in self.keys()])
    
    @property
    def total_sum(self):
        return sum([self.get_row_sum(w) for w in self._word_mapping.keys()])


# ## 3. Populating Our Colocation Data
# 
# Now that we've got the data to store our colocations in, we need to populate it!
# 
# This simple code steps through our sentences up to `sent_limit` using a window size of `window_size` and grabs the words within that window to add to to colocation matrix.
# 
# Note that no special treatment is made for word-initial or word-final tokens here, but it's possible to create such a modification!

# In[8]:


window_size = 3
sent_limit = 1000
matrix = CollocationMatrix()

for sent in brown_sents[:sent_limit]:
    for i, word in enumerate(sent):
        # Increment the count of words we've seen.
        for j in range(-window_size, window_size+1):
            # Skip counting the word itself.
            if j == 0:
                continue
                
            # At the beginning and end of the sentence,
            # you can either skip counting, or add a
            # unique "<START>" or "<END>" token to indicate
            # the word being colocated at the beginning or
            # end of sentences.            
            if len(sent) > i+j > 0:
                word_1 = sent[i].lower()
                word_2 = sent[i+j].lower()
                
                matrix.add_pair(word_1, word_2)                

def print_colocate(w_1, w_2):
    print('"{}" and "{}" seen together {} times.'.format(w_1, w_2,
                                                     matrix.get_pair(w_1, w_2)))
    
def print_count(word):
    print('"{}" has {} contexts in the data.'.format(word, 
                                                     matrix.get_row_sum(word)))

print_count('jury')                
print_colocate('jury', 'grand')
print_colocate('primary', 'election')
print_colocate('midterm', 'election')


# ## 3. Calculating PMI
# 
# Now, having collocation counts is handy, as we've discussed in class, but recall that "the" is going to collocate with all sorts of words, and so isn't all that helpful.
# 
# Instead, we should try calculating Pointwise Mutual Information (PMI), which tells us, in essence, how likely it is to see two things in the same place, compared to seeing them independently.
# 
# The formula is: $\log \frac{p(w,f)}{p(w)\cdot p(f)}$, where $p(w,f)$ is the probability of seeing context $f$ for word $w$ out of all possible contexts; $p(w)$, is the probability of seeing word $w$ in any context, and $p(f)$ is the probability for the context $f$ across all words.
# 
# If we have access to the counts for each of these factors individually:
# 
# * Sum of all contexts (`matrix.total_sum`)
# * All contexts for a given word (`matrix.get_row_sum(word)`)
# * All contexts a given word appears in (`matrix.get_col_sum(word)`)
# 
# Write a function that calculates PPMI for word $w$ and context word $f$.

# In[6]:


# Code to calculate PPMI for two words, using the
# colocation matrix calculated above.

import math

def calculate_ppmi(w, f):
    pass

