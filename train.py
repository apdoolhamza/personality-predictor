import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import joblib
import re

# Step 1: Load and prepare the dataset
df = pd.read_csv('mbti_dataset.csv')

# Clean the text
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z ]", "", text)  # remove non-letters
    text = text.lower()
    return text

df['clean_posts'] = df['posts'].apply(clean_text)

# Step 2: Add binary target columns for each MBTI letter group
df['IE'] = df['type'].apply(lambda x: 1 if x[0] == 'I' else 0)
df['NS'] = df['type'].apply(lambda x: 1 if x[1] == 'N' else 0)
df['TF'] = df['type'].apply(lambda x: 1 if x[2] == 'T' else 0)
df['JP'] = df['type'].apply(lambda x: 1 if x[3] == 'J' else 0)

# Step 3: Vectorize the text
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['clean_posts'])

# Step 4: Initialize and train each classifier
classifiers = {}
scores = {}

for trait, label in zip(['IE', 'NS', 'TF', 'JP'], ['I/E', 'N/S', 'T/F', 'J/P']):
    clf = LogisticRegression(max_iter=1000)
    score = cross_val_score(clf, X, df[trait], cv=5).mean()
    clf.fit(X, df[trait])
    classifiers[trait] = clf
    scores[trait] = score
    print(f"{label} Accuracy: {score:.2f}")

# Step 5: Save models
joblib.dump(vectorizer, 'models/vectorizer.joblib')
joblib.dump(classifiers['IE'], 'models/clf_ie.joblib')
joblib.dump(classifiers['NS'], 'models/clf_ns.joblib')
joblib.dump(classifiers['TF'], 'models/clf_tf.joblib')
joblib.dump(classifiers['JP'], 'models/clf_jp.joblib')

print("All models saved successfully.")
