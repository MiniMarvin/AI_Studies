import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """
    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        best_model = None
        base_val = float("inf")

        for n in range(self.min_n_components, self.max_n_components + 1):
            X = self.X
            length = self.lengths
            try:
                # gen the model
                model = GaussianHMM(n_components=n, n_iter=1000).fit(X, length)
                logL = model.score(X, length)

                # print(self.lengths)

                summer = 0
                for e in length:
                    summer += e

                ## p = n² + 2*n*N_d_points - 1
                p = n**2 + 2*n*len(X[0]) - 1
                score = -2*logL + p*math.log(summer)
                if  base_val > score:
                    best_model = model
                    base_val = score

            except: ## Occurs when a worng number is accessed
                pass

        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    https://pdfs.semanticscholar.org/ed3d/7c4a5f607201f3848d4c02dd9ba17c791fc2.pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_model = None
        group = []
        fit_group = []
        buff = float("-inf")

        ## Gen every model and it's score
        for n in range(self.min_n_components, self.max_n_components + 1):
            X = self.X
            length = self.lengths
            word_logL = 0
            others_logL = 0
            
            try:
                model = GaussianHMM(n_components=n, n_iter=1000).fit(X, length)
            except:
                continue

            ## Built with the reviewer support
            for w in self.words:
                x,l = self.hwords[w]
                logL = 0

                ## Compute the logL for the word
                try:
                    logL = model.score(x, l)
                except:
                    pass

                ## Set the logL to the DIC correct place
                if w == self.this_word:
                    word_logL = logL
                else:
                    others_logL += logL

            ## Compute the DIC score for the model
            scoreDIC = word_logL - float(others_logL)/float(len(self.words) - 1)
            group.append((model, scoreDIC))

        ## Select between every model the best one
        for model, val in group:
            if val > buff:
                best_model = model
                buff = val

        return best_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''
    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        best_model = None
        best_val = float("-inf")

        # split_method = KFold(n_splits=len(self.sequences))
        split_method = KFold(n_splits=min(3, len(self.sequences)))
        for n in range(self.min_n_components, self.max_n_components + 1): 
            sum_val = 0

            base_model = GaussianHMM(n_components=n, n_iter=1000)

            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
            # print("Train fold indices:{} Test fold indices:{}".format(cv_train_idx, cv_test_idx))  # view indices of the folds
                try:
                    ## Fit the model
                    X, length = combine_sequences(cv_train_idx, self.sequences)
                    model = base_model.fit(X, length)

                    ## Test the model
                    X, length = combine_sequences(cv_test_idx, self.sequences)
                    logL = model.score(X, length)

                    sum_val += logL
                    
                except: ## Occurs when some strange n is passed as a param
                    pass

            media = float(sum_val)/float(len(self.sequences))
            if best_val < media:
                best_model = model
                best_val = media

        return best_model
