import warnings
from asl_data import SinglesData

def train_all_words(features, model_selector):
    training = asl.build_training(features)  # Experiment here with different feature sets defined in part 1
    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    model_dict = {}
    for word in training.words:
        model = model_selector(sequences, Xlengths, word, 
                        n_constant=3).select()
        model_dict[word]=model
    return model_dict


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    ## extract the data from the test model
    Xlengths = test_set.get_all_Xlengths()

    for ct in Xlengths:
      ## Extract X dataset and it's length for every word in the set.
      X,lengths = Xlengths[ct]
      buff = dict()
      guess = ("", float("-inf"))
      
      ## iterate over every single model
      for word, model in models.items():
        try:
          logL = model.score(X, lengths)
          buff[word] = logL

          ## Update the guess
          if logL > guess[1]:
            guess = (word, logL)

        except: ## Avoid models which do not fit for some word
          pass

        

      probabilities.append(buff)
      guesses.append(guess[0])
    
    return probabilities, guesses
