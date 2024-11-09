import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
from streamlit_carousel import carousel
import os
import subprocess
import webbrowser
import time

# Configurer la page en mode large
st.set_page_config(layout="wide",page_title="Dashbord", page_icon="📈", initial_sidebar_state="expanded")
# Ajouter un titre au tableau de bord
st.markdown("""
    <style>
    .title {
        text-align: left; 
        font-size: 50px; 
        font-weight: normal;
        font-family: Arial, sans-serif;
        -webkit-background-clip: text;
        color: rgba(78, 140, 255, 0.9); /* Couleur avec transparence */
        margin-top: 10px;  /* Monter le titre plus haut */
    }
    </style>
    <h1 class="title">Tableau de Bord des Films</h1>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("### Analyse avant nettoyage")
st.write("")
st.write("")
# Liste des chemins des images et leurs descriptions
images_info = {
    'Distribution des Notes': {
        'path': 'distribution des note.png',
        'description': 'Analyse de la distribution des notes moyennes des films. Ce graphique permet de comprendre la répartition des notes attribuées aux films et de détecter d\'éventuelles anomalies ou biais dans les notes.'
    },
    'Évolution du Nombre de Films': {
        'path': 'évolution du nobre de film.png',
        'description': 'Ce graphique aide à identifier les tendances de production de films au cours du temps et à repérer des périodes de production anormalement basses ou élevées.'
    },
    'Durée Moyenne des Films': {
        'path': 'durée moyenne des film.png',
        'description': 'Analyse de la durée moyenne des films par année. Ce graphique permet de voir  la durée des films et d\'identifier des anomalies dans les données de durée.'
    },
    'Fréquence des Genres': {
        'path': 'frenquence des genre.png',
        'description': 'Fréquence des différents genres de films. Ce graphique montre la popularité des différents genres et aide à repérer des genres sous-représentés ou sur-représentés.'
    },
    'Nombre de Films par langue': {
        'path': 'nombre de film par langue.png',
        'description': 'Ce graphique permet de comparer la production de films entre différents genres et de détecter des déséquilibres éventuels.'
    },
    'Répartition des Types de Films': {
        'path': 'répartition des type de film.png',
        'description': 'Ce graphique aide à comprendre la composition des données en termes de types de films et à vérifier la cohérence des types répertoriés. Ici nous avons choisi de garder les movies'
    }
}

# Préparer les items pour le carrousel d'images et de descriptions
carousel_items_images = []
carousel_items_descriptions = []

for name, info in images_info.items():
    if os.path.exists(info['path']):
        with open(info['path'], "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        carousel_items_images.append(
            dict(
                title=name,
                text='',  # Empty text to avoid overlap in carousel
                img=f"data:image/png;base64,{img_base64}"
            )
        )
        carousel_items_descriptions.append(
            dict(
                title=name,
                text=info['description'],
                img=''  # No image needed for the description
            )
        )
    else:
        st.error(f"Le fichier {info['path']} n'existe pas.")

# Initialiser l'état de l'application pour le carrousel
if 'carousel_index' not in st.session_state:
    st.session_state.carousel_index = 0

# Navigation du carrousel
def next_image():
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(carousel_items_images)

def prev_image():
    st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(carousel_items_images)

# Utiliser des colonnes pour afficher les carrousels
empty_col, col1, empty_col, col2,empty_col = st.columns([0.1,0.5,0.025, 0.4,0.25])


selected_image_index = st.session_state.carousel_index

# Définir les titres des boutons
prev_title = carousel_items_images[selected_image_index - 1]['title'] if selected_image_index > 0 else carousel_items_images[-1]['title']
next_title = carousel_items_images[(selected_image_index + 1) % len(carousel_items_images)]['title']

with col1:
    
    img_data = carousel_items_images[selected_image_index]
    st.image(img_data['img'], use_column_width=True)
    
    # Utiliser des colonnes pour aligner les boutons côte à côte
    button_col1, button_col2 = st.columns(2)
    button_col1.button(f'Précédent: {prev_title}', on_click=prev_image)
    button_col2.button(f'Suivant: {next_title}', on_click=next_image)

with col2:
    if selected_image_index is not None:
        st.markdown("### ")
        selected_description = carousel_items_descriptions[selected_image_index]
        st.markdown(f"**{selected_description['title']}**")
        st.write(selected_description['text'])



# Fonction pour charger les données
def load_data():
    file_path = 'df_final.csv'
    return pd.read_csv(file_path)
    

# Fonction pour mettre à jour la mise en page des figures
def update_figure_layout(fig, title):
    fig.update_layout(
        title=title,
        title_font_size=18,  # Réduire légèrement la taille du titre
        plot_bgcolor='rgba(0,0,0,0)',  # Fond transparent à l'intérieur du tracé
        paper_bgcolor='rgba(0,0,0,0)',  # Couleur de fond du graphique externe
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=60, b=40),  # Ajuster les marges pour économiser de l'espace
        xaxis=dict(showgrid=False, title_font_size=12),
        yaxis=dict(showgrid=False, title_font_size=12),
        height=250  # Ajustement de la hauteur des graphiques pour réduire la taille
    )
    return fig

# Charger les données
data = load_data()

# Configuration de la barre latérale
st.sidebar.header('Filtrer les données')
years = st.sidebar.slider('Sélectionnez une plage de dates', min_value=int(data['Annee_Debut'].min()), max_value=int(data['Annee_Debut'].max()), value=(2000, 2020), step=1)
genres = st.sidebar.multiselect('Sélectionnez les genres', options=data['Genres'].str.split(',').explode().unique(), default=data['Genres'].str.split(',').explode().unique())

# Filtrer les données en fonction des sélections
filtered_data = data[(data['Annee_Debut'] >= years[0]) & (data['Annee_Debut'] <= years[1])]
filtered_data = filtered_data[filtered_data['Genres'].apply(lambda x: any(genre in x for genre in genres))]

# Préparer les données
data_sorted = filtered_data.sort_values(by='Annee_Debut')
# Préparer les données pour le graphique des Top 5 Genres par Nombre de Films
top_genres = filtered_data['Genres'].str.split(',', expand=True).stack().value_counts().nlargest(10)
top_genres_df = top_genres.reset_index()
top_genres_df.columns = ['Genre', 'Nombre de Films']

# Créer le graphique des Top 5 Genres par Nombre de Films
fig_top_genres = px.bar(top_genres_df, x='Genre', y='Nombre de Films',
                        title='Top 10 Genres par Nombre de Films',
                        text='Nombre de Films',
                        labels={'Nombre de Films': 'Nombre de Films', 'Genre': ''})

fig_top_genres.update_traces(marker_color='rgba(130, 89, 182, 9)', textposition='auto', textfont_size=15,
                             hovertemplate='<b>%{x}</b><br>Nombre de Films: %{y}<extra></extra>')
fig_top_genres = update_figure_layout(fig_top_genres, 'Top 10 Genres par Nombre de Films')

# Préparer les données pour le graphique de la Durée Moyenne des Films au Fil des Années
avg_duration = filtered_data.groupby('Annee_Debut')['Duree_Minutes'].mean().reset_index()

# Créer le graphique de la Durée Moyenne des Films au Fil des Années
fig_avg_duration = px.line(avg_duration, x='Annee_Debut', y='Duree_Minutes',
                           title='Durée Moyenne des Films au Fil des Années',
                           labels={'Annee_Debut': '', 'Duree_Minutes': 'Durée Moyenne (min)'},
                           markers=True)

fig_avg_duration.update_traces(marker=dict(size=5, color='rgba(255, 193, 7, .9)'), line=dict(color='rgba(130, 130, 130, 9)'))
fig_avg_duration = update_figure_layout(fig_avg_duration, 'Durée Moyenne des Films au Fil des Années')


# Créer les graphiques avec des mises à jour de mise en page uniformes
fig_popularity = px.line(data_sorted, x='Annee_Debut', y='popularity', 
                         labels={'Annee_Debut': '', 'popularity': 'Popularité'},
                         hover_name='Titre_Principal')
fig_popularity = update_figure_layout(fig_popularity, 'Popularité des films au fil des années')

fig_revenue = px.line(data_sorted, x='Annee_Debut', y='revenue', 
                      labels={'Annee_Debut': '', 'revenue': 'Revenus'},
                      hover_name='Titre_Principal')
fig_revenue = update_figure_layout(fig_revenue, 'Revenus des films au fil des années')

# Créer le graphique de distribution des moyennes
fig_distribution_moyenne = px.histogram(data_sorted, x='moyenne',
                                        title='Distribution des Moyennes',
                                        labels={'moyenne': 'Moyenne des Votes'},
                                        nbins=20,  # Nombre de bins pour l'histogramme
                                        opacity=0.8,
                                        color_discrete_sequence=['indianred'])  # Couleur des barres

fig_distribution_moyenne.update_layout(bargap=0.1)  # Espacement entre les barres
fig_distribution_moyenne = update_figure_layout(fig_distribution_moyenne, 'Distribution des Moyennes')

# Préparer les données pour le graphique de l'évolution du nombre de films au fil des ans
films_per_year = filtered_data['Annee_Debut'].value_counts().sort_index().reset_index()
films_per_year.columns = ['Annee_Debut', 'Nombre de Films']

# Créer le graphique de l'évolution du nombre de films au fil des ans
fig_films_per_year = px.line(films_per_year, x='Annee_Debut', y='Nombre de Films',
                             title="Évolution du nombre de films au fil des Ans",
                             labels={'Annee_Debut': '', 'Nombre de Films': 'Nombre de Films'},
                             markers=True)

fig_films_per_year.update_traces(marker=dict(size=5, color='rgba(0, 123, 255, .9)'), line=dict(color='rgba(0, 123, 255, .9)'))
fig_films_per_year = update_figure_layout(fig_films_per_year, "Évolution du nombre de films au fil des Ans")




fig_custom = go.Figure()
fig_custom.add_trace(go.Scatter(
    x=data_sorted['Annee_Debut'], 
    y=data_sorted['moyenne'],
    mode='lines+markers',
    marker=dict(size=10, color='rgba(130, 89, 182, .8)'),
    line=dict(color='rgba(105, 105, 105, 0)')
))
fig_custom = update_figure_layout(fig_custom, 'Moyenne des votes par Année')
# Utiliser les colonnes correctes pour réaliser le tableau des réalisateurs et des acteurs
if 'primaryName_director' in filtered_data.columns and 'actor_names' in filtered_data.columns:
    directors = filtered_data['primaryName_director'].value_counts().head(5)
    actors = filtered_data['actor_names'].str.split(',').explode().value_counts().head(5)
    
    # Créer le tableau des réalisateurs
    fig_directors = go.Figure(data=[go.Table(
        header=dict(values=['Réalisateur', 'Nombre de Films'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[directors.index, directors.values],
                   fill_color='lavender',
                   align='left'))
    ])
    fig_directors.update_layout(title="Top 5 Réalisateurs par Nombre de Films")


# Appliquer les styles CSS globaux pour les conteneurs de graphiques
st.markdown("""
<style>
div.stPlotlyChart {
    border-radius: 10px;  /* Coins arrondis pour un look plus lisse */
    transition: transform .2s;  /* Transition douce */
    padding: 10px;  /* Ajustement de l'alignement */
    margin: 15px 10px;  /* Espacement entre les graphiques */
}
div.stPlotlyChart:hover {
    transform: scale(1.02);  /* Effet de zoom au survol */
    box-shadow: 5px 5px 10px rgba(105, 105, 130, 0.5);  /* Ombre floue */
}
</style>
""", unsafe_allow_html=True)
st.write("")
st.write("")
st.write("")
# Placer le titre avant les graphiques
st.markdown("### Analyse après nettoyage")
st.write("")
st.write("")
st.write("")
st.write("")
# Utiliser des conteneurs pour organiser les graphiques en colonnes et en lignes avec espacement
col1, empty_col1, col2, empty_col2, col3 = st.columns([1, 0.01, 1, 0.1, 1])  # Création de trois colonnes avec des espacements
with col1:
    st.plotly_chart(fig_popularity, use_container_width=True)
with col2:
    st.plotly_chart(fig_custom, use_container_width=True)
with col3:
    st.plotly_chart(fig_revenue, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_films_per_year, use_container_width=True)
    st.plotly_chart(fig_avg_duration, use_container_width=True)

with col2:
    st.plotly_chart(fig_top_genres, use_container_width=True)
    st.plotly_chart(fig_distribution_moyenne, use_container_width=True)
    pass
import seaborn as sns
import matplotlib.pyplot as plt

# Sélection des colonnes pour les analyses de corrélation
cols_to_analyze = ['popularity', 'revenue', 'vote_average', 'vote_count']

# Création du pairplot pour visualiser les relations entre les variables
pairplot = sns.pairplot(data[cols_to_analyze])
plt.suptitle('Pairplot de Corrélation', y=1.02)

# Création de la heatmap pour la matrice de corrélation
plt.figure(figsize=(10, 8))
correlation_matrix = data[cols_to_analyze].corr()
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Heatmap de la Matrice de Corrélation')

# Affichage des graphiques
plt.show()




def run_app_py():
    # Pas besoin de lancer Chrome sur Streamlit Cloud
    # Suppression de subprocess pour ouvrir le navigateur local
    url = 'https://recommandation-de-film.streamlit.app/'  # URL de l'application Streamlit déployée
    return url

st.title("Accès au système de recommandation de film")
if st.button("Accéder à l'application en ligne"):
    app_url = run_app_py()
    st.success(f"Application disponible en ligne à {app_url}")
    # Affichez le lien en tant que lien cliquable
    st.markdown(f"[Ouvrir l'application]({app_url})")

