import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import os

# Configuration de la page
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="📈", initial_sidebar_state="expanded")

# Titre du tableau de bord avec CSS personnalisé
st.markdown("""
    <style>
    .title { text-align: left; font-size: 50px; font-weight: normal;
             font-family: Arial, sans-serif; color: rgba(78, 140, 255, 0.9); margin-top: 10px; }
    </style>
    <h1 class="title">Tableau de Bord des Films</h1>
    """, unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Texte d'introduction
st.markdown("### Analyse avant nettoyage")
st.write("")

# Informations et chargement des images pour le carrousel
images_info = {
    'Distribution des Notes': 'distribution des note.png',
    'Évolution du Nombre de Films': 'évolution du nobre de film.png',
    'Durée Moyenne des Films': 'durée moyenne des film.png',
    'Fréquence des Genres': 'frenquence des genre.png',
    'Nombre de Films par langue': 'nombre de film par langue.png',
    'Répartition des Types de Films': 'répartition des type de film.png'
}

carousel_items = []
for name, path in images_info.items():
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        carousel_items.append(dict(title=name, img=f"data:image/png;base64,{img_base64}"))
    else:
        st.error(f"Le fichier {path} n'existe pas.")

# Gestion de l'index du carrousel dans l'état de session
if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = 0

def next_image():
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_items)

def prev_image():
    st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(carousel_items)

selected_image = carousel_items[st.session_state.carousel_index]

# Affichage du carrousel avec colonnes
col1, col2 = st.columns([1, 1])
with col1:
    st.image(selected_image['img'], use_column_width=True)
    st.button("Précédent", on_click=prev_image)
    st.button("Suivant", on_click=next_image)
with col2:
    st.write(f"### {selected_image['title']}")

# Fonction de chargement des données
@st.cache
def load_data(file_path='df_final.csv'):
    return pd.read_csv(file_path)

# Charger les données
data = load_data()

# Configuration de la barre latérale de filtre
st.sidebar.header('Filtrer les données')
years = st.sidebar.slider('Plage de dates', int(data['Annee_Debut'].min()), int(data['Annee_Debut'].max()), (2000, 2020))
genres = st.sidebar.multiselect('Genres', data['Genres'].str.split(',').explode().unique(), data['Genres'].str.split(',').explode().unique())

# Filtrer les données en fonction des sélections
filtered_data = data[(data['Annee_Debut'] >= years[0]) & (data['Annee_Debut'] <= years[1])]
filtered_data = filtered_data[filtered_data['Genres'].apply(lambda x: any(genre in x for genre in genres))]

# Graphique des Top 10 Genres
top_genres = filtered_data['Genres'].str.split(',', expand=True).stack().value_counts().nlargest(10).reset_index()
top_genres.columns = ['Genre', 'Nombre de Films']
fig_top_genres = px.bar(top_genres, x='Genre', y='Nombre de Films', title='Top 10 Genres par Nombre de Films')

# Graphique de la Durée Moyenne des Films
avg_duration = filtered_data.groupby('Annee_Debut')['Duree_Minutes'].mean().reset_index()
fig_avg_duration = px.line(avg_duration, x='Annee_Debut', y='Duree_Minutes', title='Durée Moyenne des Films au Fil des Années')

# Graphiques supplémentaires
fig_popularity = px.line(filtered_data, x='Annee_Debut', y='popularity', hover_name='Titre_Principal', title='Popularité des films')
fig_revenue = px.line(filtered_data, x='Annee_Debut', y='revenue', hover_name='Titre_Principal', title='Revenus des films')
fig_distribution_moyenne = px.histogram(filtered_data, x='moyenne', nbins=20, title='Distribution des Moyennes')
films_per_year = filtered_data['Annee_Debut'].value_counts().sort_index().reset_index()
films_per_year.columns = ['Annee_Debut', 'Nombre de Films']
fig_films_per_year = px.line(films_per_year, x='Annee_Debut', y='Nombre de Films', title="Évolution du nombre de films")

# Affichage des graphiques en colonnes
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig_top_genres, use_container_width=True)
col2.plotly_chart(fig_avg_duration, use_container_width=True)
col3.plotly_chart(fig_popularity, use_container_width=True)
st.plotly_chart(fig_revenue, use_container_width=True)
st.plotly_chart(fig_distribution_moyenne, use_container_width=True)
st.plotly_chart(fig_films_per_year, use_container_width=True)

# Lien vers l'application Streamlit en ligne
st.title("Accès au système de recommandation de film")
app_url = 'https://recommandation-de-film.streamlit.app/'
if st.button("Accéder à l'application en ligne"):
    st.success(f"Application disponible en ligne : [Ouvrir l'application]({app_url})")

