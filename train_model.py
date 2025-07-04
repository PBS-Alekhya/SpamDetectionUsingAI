# train_model.py
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from app.preprocessor import Preprocessor, NORMALIZATION_DICT, HINGLISH_STOP_WORDS
from sklearn.metrics import classification_report
import os



# Load and prepare data
df = pd.read_csv("data/dataset.csv")
df.dropna(subset=["post", "label"], inplace=True)

# Encode labels using label encoder
le = LabelEncoder()
y = le.fit_transform(df["label"])

# Split data into Train and Test data 
X_train, X_test, y_train, y_test = train_test_split(df["post"], y, test_size=0.2, random_state=100)

# Building pipeline
pipeline = Pipeline([
    ("preprocessor", Preprocessor(NORMALIZATION_DICT)),
    ("tfidf", TfidfVectorizer(
        max_features=7000,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b\w+\b|[^\w\s]"
    )),
    ("clf", LogisticRegression())
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
acc = pipeline.score(X_test, y_test)
print(f" Accuracy: {acc:.4f}")
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model pipeline
os.makedirs("app/model", exist_ok=True)
joblib.dump(pipeline, "app/model/model.joblib")
print(" Pipeline saved to app/model/model.joblib")
