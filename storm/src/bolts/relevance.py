import os
from streamparse.bolt import Bolt

from sklearn.externals import joblib

BIGFORECAST_HOME = os.environ["BIGFORECAST_HOME"]

# relevance model is a pipeline which includes the countvectorizer
# and a model for classifying probability of relevance to oil price.

model_dir = BIGFORECAST_HOME + "/trained_models/"
model_name = "article_relevance_classification.pkl"
relevance_model = joblib.load(model_dir + model_name)

class relevance_check(Bolt):
  """
  This bolt checks the relevance of an article using a pre-trained model on the
  retuers and Bloomberg news set using predict_proba and attaches that relevance to
  the tuple which is returned.
  """

    def process(self, tup):
        text = tup.values[1] #DEV Figure out tuple structure
        relevance = relevance_model.predict_proba(text)

        tup.append(relevance)
        # Emit all the words
        self.emit(tup)

        # tuple acknowledgement is handled automatically
