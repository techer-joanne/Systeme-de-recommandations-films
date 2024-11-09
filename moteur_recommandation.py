import nltk
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
import string
import streamlit as st

# Télécharger les ressources NLTK si nécessaire
nltk_packages = ['stopwords', 'punkt', 'wordnet']
for package in nltk_packages:
    try:
        nltk.data.find(f"corpora/{package}")
    except LookupError:
        nltk.download(package)

# Charger les stopwords après téléchargement
stop_words = set(stopwords.words('french'))

# Charger le modèle Spacy
nlp = spacy.load('fr_core_news_sm')
lemmatizer = WordNetLemmatizer()

# Fonction pour charger les données
@st.cache_data
def load_data():
    return pd.read_csv('df_final.csv')

# Fonction pour prétraiter le texte
@st.cache_data
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Retirer les chiffres
    text = text.translate(str.maketrans('', '', string.punctuation))  # Retirer la ponctuation
    text = text.strip()
    
    # Tokenisation
    tokens = word_tokenize(text)
    
    # Retirer les stopwords et lemmatiser
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return ' '.join(tokens)

# Charger les données et prétraiter le texte
df = load_data()
df['text_preprocessed'] = df['overview_french'].apply(preprocess_text)

# Fonction pour calculer les matrices de TF-IDF et de similarité
@st.cache_resource
def calculate_similarity(df):
    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(max_df=0.99, min_df=2)
    tfidf_matrix = vectorizer.fit_transform(df['text_preprocessed'])

    # Appliquer TruncatedSVD pour réduire la dimensionnalité
    svd = TruncatedSVD(n_components=100)
    tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)

    # Calculer la similarité cosinus entre tous les films
    cosine_sim = cosine_similarity(tfidf_matrix_reduced, tfidf_matrix_reduced)

    # Créer une matrice de similarité pour les genres
    df['Genres'] = df['Genres'].apply(lambda x: x.split('|'))
    genres_list = df['Genres'].tolist()
    unique_genres = list(set(genre for sublist in genres_list for genre in sublist))
    genre_matrix = pd.DataFrame(0, index=df.index, columns=unique_genres)

    for i, genres in enumerate(genres_list):
        genre_matrix.loc[i, genres] = 1

    cosine_sim_genres = cosine_similarity(genre_matrix, genre_matrix)

    # Ajouter la similarité sur les titres avec TfidfVectorizer
    vectorizer_titles_tfidf = TfidfVectorizer()
    tfidf_matrix_titles = vectorizer_titles_tfidf.fit_transform(df['Titre_Principal'])
    cosine_sim_titles_tfidf = cosine_similarity(tfidf_matrix_titles, tfidf_matrix_titles)

    # Combiner la similarité cosinus, la similarité des genres et la similarité des titres (TF-IDF)
    combined_sim_tfidf = (cosine_sim + cosine_sim_genres + cosine_sim_titles_tfidf) / 3

    return combined_sim_tfidf

combined_sim_tfidf = calculate_similarity(df)

# Fonction pour obtenir des recommandations
def get_recommendations_tfidf(title, cosine_sim=combined_sim_tfidf):
    try:
        idx = df[df['Titre_Principal'] == title].index[0]
    except IndexError:
        return f"Le film '{title}' n'a pas été trouvé dans la base de données."
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    
    return df.loc[movie_indices, ['tconst', 'Titre_Principal', 'poster_path']]

