from collections import defaultdict

class CollocationMatrix(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._word_mapping = {}  # Where we'll store string->int mapping.   
        self._id_mapping = [] # Where we'll store int->string mapping.
    
    def word_id(self, word, store_new=False):
        """
        Return the integer ID for the given vocab item. If we haven't
        seen this vocab item before, give ia a new ID. We can do this just
        as 1, 2, 3... based on how many words we've seen before.
        """
        if word not in self._word_mapping:
            if store_new:
                self._word_mapping[word] = len(self._word_mapping)
                self._id_mapping.append(word)
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
        if w_1_id is not None and w_2_id is not None:
            return self[w_1_id][w_2_id]
        else:
            return 0
        
    def get_row(self, word):
        word_id = self.word_id(word)
        if word_id is not None:
            return self.get(word_id)
        else:
            return defaultdict(int)
    
    __row_sum = None
    def get_row_sum(self, word):
        """
        Get the number of total contexts available for a given word        
        """

        # Create the cache if it doesn't exist.
        if self.__row_sum is None:
            self.__row_sum = []
            # Fill the cache with Nones.
            for i in range(len(self._id_mapping)):
                self.__row_sum.append(None)
        
        f_id = self.word_id(word)
        # Check if the cache for the requested word is None: 
        if self.__row_sum[f_id] is None:
            self.__row_sum[f_id] = sum(self.get_row(word).values())
        return self.__row_sum[f_id]
    
    __col_sum = None
    def get_col_sum(self, word):
        """
        Get the number of total contexts a given word occurs in
        """

        # Create the cache if it doesn't exist.
        if self.__col_sum is None:
            self.__col_sum = []
            # Fill the cache with Nones.
            for i in range(len(self._id_mapping)):
                self.__col_sum.append(None)
        
        f_id = self.word_id(word)
        # Check if the cache for the requested word is None: 
        if self.__col_sum[f_id] is None:
            self.__col_sum[f_id] = sum([self[w][f_id] for w in self.keys()])
        return self.__col_sum[f_id]
    
    __total_sum = None
    @property
    def total_sum(self):
        if self.__total_sum is None:
            self.__total_sum = sum([self.get_row_sum(w) for w in self._word_mapping.keys()])
        return self.__total_sum
