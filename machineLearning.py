import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import classification_report

class LogDataModel:

    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.df['message'] = self.df['message'].apply(self.clean_text)
        self.vectorizer = TfidfVectorizer()

    @staticmethod
    def clean_text(text):
        return re.sub(r'[^\w\s]', '', text.lower())

    def split_data(self):
        self.train_data, self.test_data, self.train_labels, self.test_labels = train_test_split(
            self.df['message'],
            self.df['level'],
            test_size=0.2,
            random_state=42
        )

    def convert_text_to_vector(self):
        self.train_vectors = self.vectorizer.fit_transform(self.train_data)
        self.test_vectors = self.vectorizer.transform(self.test_data)

    def train_model(self):
        self.model = svm.SVC(kernel='linear')
        self.model.fit(self.train_vectors, self.train_labels)

    def evaluate_model(self):
        predictions = self.model.predict(self.test_vectors)
        print(classification_report(self.test_labels, predictions))

# Usage:

log_data_model = LogDataModel('output.csv')
log_data_model.split_data()
log_data_model.convert_text_to_vector()
log_data_model.train_model()
log_data_model.evaluate_model()
