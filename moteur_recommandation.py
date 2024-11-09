import nltk
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re
import string

# Vérifier et télécharger les ressources NLTK nécessaires
try:
    stop_words = set(stopwords.words('french'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('french'))

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Charger le DataFrame
df = pd.read_csv('df_final.csv')

# Prétraitement du texte
nlp = spacy.load('fr_core_news_sm')
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [stemmer.stem(word) for word in tokens]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

df['text_preprocessed'] = df['overview_french'].apply(preprocess_text)

# Le reste de votre code


# Créer une instance de TfidfVectorizer et transformer le texte prétraité en vecteurs TF-IDF
vectorizer = TfidfVectorizer(max_df=0.99, min_df=2)
tfidf_matrix = vectorizer.fit_transform(df['text_preprocessed'])

# Appliquer TruncatedSVD pour réduire la dimensionnalité
svd = TruncatedSVD(n_components=1000)
tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)

# Calculer la similarité cosinus entre tous les films
cosine_sim = cosine_similarity(tfidf_matrix_reduced, tfidf_matrix_reduced)

# Ajouter les genres au DataFrame pour la similarité
df['Genres'] = df['Genres'].apply(lambda x: x.split('|'))  # En supposant que les genres sont séparés par '|'

# Créer une matrice de similarité pour les genres
genres_list = df['Genres'].tolist()
unique_genres = list(set([genre for sublist in genres_list for genre in sublist]))
genre_matrix = pd.DataFrame(0, index=df.index, columns=unique_genres)

for i, genres in enumerate(genres_list):
    for genre in genres:
        genre_matrix.at[i, genre] = 1

# Ajouter la similarité sur les titres avec TfidfVectorizer
vectorizer_titles_tfidf = TfidfVectorizer()
tfidf_matrix_titles = vectorizer_titles_tfidf.fit_transform(df['Titre_Principal'])
cosine_sim_titles_tfidf = cosine_similarity(tfidf_matrix_titles, tfidf_matrix_titles)

# Combiner la similarité cosinus, la similarité des genres et la similarité des titres (TF-IDF)
cosine_sim_genres = cosine_similarity(genre_matrix, genre_matrix)
combined_sim_tfidf = (cosine_sim + cosine_sim_genres + cosine_sim_titles_tfidf) / 3

# Fonction pour obtenir des recommandations avec TF-IDF
def get_recommendations_tfidf(title, cosine_sim=combined_sim_tfidf):
    idx = df[df['Titre_Principal'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df.loc[movie_indices, ['tconst', 'Titre_Principal', 'poster_path']]
