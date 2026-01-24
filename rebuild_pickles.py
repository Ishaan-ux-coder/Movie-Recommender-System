import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import ast
import pickle
import warnings

warnings.filterwarnings('ignore')

print("Downloading NLTK data...")
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4') # Often needed for lemmatizer

print("Reading CSV...")
try:
    df = pd.read_csv('movies_metadata.csv', low_memory=False)
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

print(f"Initial shape: {df.shape}")

# Filter relevant columns and known cleanups
# Note: The notebook drops duplicates at some point.
# df = df.drop_duplicates().reset_index(drop = True) # The notebook does this early on?
# Cell 7 in notebook: df = df.drop_duplicates().reset_index(drop = True)
# It only keeps columns? No, it keeps all.

# However, the notebook filters to rows where 'genres' is not null effectively? 
# df.isnull().sum() showed 0 genres nulls.

# Preprocessing from notebook
print("Preprocessing...")

# Fillna
df['overview'] = df['overview'].fillna('')
df['tagline'] = df['tagline'].fillna('')

# Genres parsing
def parse_genres(x):
    try:
        return " ".join([i['name'] for i in ast.literal_eval(x)])
    except:
        return ""

df['genres'] = df['genres'].apply(parse_genres)

# Create tags
df['tags'] = df['overview']+ " " + df['genres'] +" "+ df['tagline']

# NLTK Processing
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

print("Applying text preprocessing (this might take a while)...")
df['tags'] = df['tags'].apply(preprocess_text)

# Reset index just in case
df = df.reset_index(drop=True)

# Create indices map
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# TF-IDF
print("Computing TF-IDF...")
tfidf = TfidfVectorizer(max_features=50000, ngram_range=(1,2), stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['tags'])

print(f"TF-IDF shape: {tfidf_matrix.shape}")

# Save pickles
print("Saving pickles...")
try:
    with open('tfidf_matrix.pkl', 'wb') as f:
        pickle.dump(tfidf_matrix, f)
    
    with open('indices.pkl', 'wb') as f:
        pickle.dump(indices, f)
    
    df.to_pickle('df.pkl')
    
    with open('tfidf.pkl', 'wb') as f:
        pickle.dump(tfidf, f)
    
    # Also create movie_data.pkl as a copy of df.pkl just in case
    # although main.py uses df.pkl.
    # But earlier I manually created it.
    
    print("Success! Pickles regenerated.")

except Exception as e:
    print(f"Error saving pickles: {e}")
