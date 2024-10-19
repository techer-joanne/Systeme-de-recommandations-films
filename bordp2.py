import streamlit as st
import pandas as pd
import plotly.express as px
import time
import altair as alt



import streamlit as st
st.set_page_config(
    layout="wide", page_title="Movies recommandation", page_icon="📽️"
)
# Créer une fonction pour vérifier les identifiants de l'utilisateur (ceci est juste un exemple)
def verifier_identifiants(nom_utilisateur, mot_de_passe):
    # Dans une vraie application, vous vérifieriez les identifiants contre une base de données ou un service d'authentification.
    # Pour l'instant, nous accepterons simplement tout nom d'utilisateur et mot de passe non vide.
    return nom_utilisateur != "" and mot_de_passe != ""

# Afficher le formulaire de connexion
def afficher_formulaire_connexion():
    st.sidebar.title("Connexion")
    nom_utilisateur = st.sidebar.text_input("Nom d'utilisateur")
    mot_de_passe = st.sidebar.text_input("Mot de passe", type="password")
    
    if st.sidebar.button("Se connecter"):
        if verifier_identifiants(nom_utilisateur, mot_de_passe):
            st.session_state['authentifie'] = True
            st.success("Vous êtes connecté !")
        else:
            st.error("Nom d'utilisateur ou mot de passe invalide")

# Vérifier si l'utilisateur est déjà authentifié
if 'authentifie' not in st.session_state:
    st.session_state['authentifie'] = False

# Logique principale de l'application
if st.session_state['authentifie']:
    st.title("") #Bienvenue sur le tableau de bord !
    # Le code de votre application ici
else:
    afficher_formulaire_connexion()

st.title("tableau de bord")
# HTML pour intégrer le tableau de bord Power BI
html_code = f"""
<iframe title="projet_1 wild_code" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=d5c6b505-7659-4b41-9bac-f30515c366e7&autoAuth=true&ctid=cf81581f-cf8c-405d-97e3-34a295c8d882" frameborder="0" allowFullScreen="true"></iframe>
"""

# Utilisation de st.markdown pour intégrer le tableau de bord
st.markdown(html_code, unsafe_allow_html=True)


def top_5_films_page():
    st.header("Top 5 des films en France aujourd'hui")
    
    # Exemple de données pour les films
    films = [
        {"titre": "Film 1", "description": "Description ici...", "image": "path_to_image1.jpg"},
        {"titre": "Film 2", "description": "Description ici...", "image": "path_to_image2.jpg"},
        {"titre": "Film 3", "description": "Description ici...", "image": "path_to_image3.jpg"},
        {"titre": "Film 4", "description": "Description ici...", "image": "path_to_image4.jpg"},
        {"titre": "Film 5", "description": "Description ici...", "image": "path_to_image5.jpg"}
    ]

    cols = st.columns(5)  # Création de 5 colonnes pour les 5 films
    for i, film in enumerate(films):
        with cols[i]:
            st.image(film['image'], caption=film['titre'])  # Afficher l'image avec un titre comme légende
            st.write(film['description'])  # Afficher la description du film
st.markdown("""
<style>
    .js-plotly-plot .plotly {
        border-radius: 20px 20px 20px 20px;  # Controls the roundness of the corners
    }
    .plot-container {
        border-radius: 0px;  # Ensure the container also has rounded corners
        transition: transform .2s;
        background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
        padding: 0 5px 5px 5px;  # Ajustement de l'alignement
        box-shadow: 0 20px 8px rgba(0, 0, 0, 0.5);
    }
    .plot-container:hover {
        transform: scale(1.05);  # Maintain hover effect
        background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
    }
</style>
""", unsafe_allow_html=True)




# Add custom CSS for rounded corners and shadow, ensuring it complements existing CSS
st.markdown("""
<style>
    .js-plotly-plot .plotly {
        border-radius: 10px 5px 20px 15px;  # Controls the roundness of the corners
    }
    .plot-container {
        border-radius: 0px;  # Ensure the container also has rounded corners
        transition: transform .2s;
        background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
        padding: 0 5px 5px 5px;  # Ajustement de l'alignement
        box-shadow: 0 20px 8px rgba(0, 0, 0, 0);
    }
    .plot-container:hover {
        transform: scale(1.05);  # Maintain hover effect
    }
</style>
""", unsafe_allow_html=True)




# Apply CSS to Streamlit container to ensure rounded corners and center alignment
st.markdown("""
<div style="overflow: hidden; border-radius: 10px 5px 20px 15px;">
    <style>
        .main .block-container {
            border-radius: 0px;
            background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
            padding: 0 5px 5px 5px;  # Ajustement de l'alignement
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
    </style>
</div>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    .js-plotly-plot .plotly {
        border-radius: 20px 20px 20px 20px;  # Controls the roundness of the corners
    }
    .plot-container {
        border-radius: 0px;  # Ensure the container also has rounded corners
        transition: transform .2s;
        background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
        padding: 0 5px 5px 5px;  # Ajustement de l'alignement
        box-shadow: 0 20px 8px rgba(0, 0, 0, 0.5);
    }
    .plot-container:hover {
        transform: scale(1.05);  # Maintain hover effect
        background: linear-gradient(to right, #6a11cb, #2575fc);  # Dégradé de couleur ajouté
    }
</style>
""", unsafe_allow_html=True)



# ou cas ou digne fait 

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your data
def load_data():
    return pd.read_csv('df_final.csv')

data = load_data()

# Create a Plotly figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['Annee_Debut'], 
    y=data['moyenne'],
    mode='lines+markers',
    marker=dict(size=10, color='rgba(130, 89, 182, .8)'),
    line=dict(color='rgba(231, 76, 60, .8)')
))

# Update layout for the figure
fig.update_layout(
    title='Revenus par Année',
    plot_bgcolor='rgba(0,0,0,.0)',  # Transparent background inside the plot
    paper_bgcolor='rgba(0,0,0,0)',# Background color of the outer graph
    font=dict(color='white'),
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

# Display the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Display the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Utilisez st.markdown pour injecter des styles CSS
st.markdown("""
<style>
.plot-container {
    border-radius: 10px;  /* Des coins arrondis pour un look plus lisse */
    transition: transform .2s;
    background: linear-gradient(
        to right, 
        #C0C0C0 -80%, 
        #223156 95%, 
        #223156 100%
    );  /* Dégradé de couleur argenté */
    padding: 10px;  /* Ajustement de l'alignement */
    
}
.plot-container:hover {
    transform: scale(1.05);  /* Effet de zoom au survol */
    box-shadow: 5px 5px 15px rgba(105, 105, 130, 1);  /* Flou gris clair */        
}
</style>
""", unsafe_allow_html=True)

# Votre code pour afficher les graphiques ici
# Exemple :
# st.plotly_chart(fig, use_container_width=True)
# Ajouter un titre au tableau de bord
st.markdown("""
    <style>
    .title {
        text-align: left; 
        font-size: 30px; 
        font-weight: normal;
        font-family: Arial, sans-serif;
        -webkit-background-clip: text;
        color: rgba(78, 140, 255, 0.3); /* Couleur avec transparence */
        margin-top: -75px;  /* Monter le titre plus haut */
    }
    </style>
    <h1 class="title">Tableau de Bord des Films</h1>
    """, unsafe_allow_html=True)
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
top_genres = filtered_data['Genres'].str.split(',', expand=True).stack().value_counts().nlargest(5)
top_genres_df = top_genres.reset_index()
top_genres_df.columns = ['Genre', 'Nombre de Films']

# Créer le graphique des Top 5 Genres par Nombre de Films
fig_top_genres = px.bar(top_genres_df, x='Genre', y='Nombre de Films',
                        title='Top 5 Genres par Nombre de Films',
                        text='Nombre de Films',
                        labels={'Nombre de Films': 'Nombre de Films', 'Genre': 'Genre'})

fig_top_genres.update_traces(marker_color='rgba(130, 89, 182, .8)', textposition='outside')
fig_top_genres = update_figure_layout(fig_top_genres, 'Top 5 Genres par Nombre de Films')

# Préparer les données pour le graphique de la Durée Moyenne des Films au Fil des Années
avg_duration = filtered_data.groupby('Annee_Debut')['Duree_Minutes'].mean().reset_index()

# Créer le graphique de la Durée Moyenne des Films au Fil des Années
fig_avg_duration = px.line(avg_duration, x='Annee_Debut', y='Duree_Minutes',
                           title='Durée Moyenne des Films au Fil des Années',
                           labels={'Annee_Debut': 'Année', 'Duree_Minutes': 'Durée Moyenne (min)'},
                           markers=True)

fig_avg_duration.update_traces(marker=dict(size=8, color='rgba(255, 193, 7, .9)'), line=dict(color='rgba(130, 130, 130, .5)'))
fig_avg_duration = update_figure_layout(fig_avg_duration, 'Durée Moyenne des Films au Fil des Années')
# Créer les graphiques avec des mises à jour de mise en page uniformes
fig_popularity = px.line(data_sorted, x='Annee_Debut', y='popularity', 
                         labels={'Annee_Debut': 'Année', 'popularity': 'Popularité'},
                         hover_name='Titre_Principal')
fig_popularity = update_figure_layout(fig_popularity, 'Popularité des films au fil des années')

fig_revenue = px.line(data_sorted, x='Annee_Debut', y='revenue', 
                      labels={'Annee_Debut': 'Année', 'revenue': 'Revenus'},
                      hover_name='Titre_Principal')
fig_revenue = update_figure_layout(fig_revenue, 'Revenus des films au fil des années')

fig_vote_average = px.line(data_sorted, x='Annee_Debut', y='vote_average', 
                           labels={'Annee_Debut': 'Année', 'vote_average': 'Moyenne des votes'},
                           hover_name='Titre_Principal')
fig_vote_average = update_figure_layout(fig_vote_average, 'Moyenne des votes des films au fil des années')

fig_popularity_vote_ratio = px.line(data_sorted, x='Annee_Debut', y='popularity_vote_ratio', 
                                    labels={'Annee_Debut': 'Année', 'popularity_vote_ratio': 'Ratio de popularité par vote'},
                                    hover_name='Titre_Principal')
fig_popularity_vote_ratio = update_figure_layout(fig_popularity_vote_ratio, 'Ratio de popularité par vote au fil des années')

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

    # Créer le tableau des acteurs
    fig_actors = go.Figure(data=[go.Table(
        header=dict(values=['Acteur', 'Nombre de Films'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[actors.index, actors.values],
                   fill_color='lavender',
                   align='left'))
    ])
    fig_actors.update_layout(title="Top 5 Acteurs par Nombre de Films")

# Appliquer les styles CSS globaux pour les conteneurs de graphiques
st.markdown("""
<style>
div.stPlotlyChart {
    border-radius: 10px;  /* Coins arrondis pour un look plus lisse */
    transition: transform .2s;  /* Transition douce */
    background: linear-gradient(
        to right, 
        rgba(192, 192, 192, 0.8) 1%,  /* Couleur argentée avec transparence */
        rgba(34, 49, 86, 0.8) 95%,  /* Couleur plus foncée avec transparence */
        rgba(34, 49, 86, 0.8) 100%  /* Couleur plus foncée avec transparence */
    );  /* Dégradé de couleur */
    padding: 10px;  /* Ajustement de l'alignement */
    margin: 15px 10px;  /* Espacement entre les graphiques */
}
div.stPlotlyChart:hover {
    transform: scale(1.05);  /* Effet de zoom au survol */
    box-shadow: 5px 5px 10px rgba(105, 105, 130, 0.5);  /* Ombre floue */
}
</style>
""", unsafe_allow_html=True)

# Utiliser des conteneurs pour organiser les graphiques en colonnes et en lignes avec espacement
col1, empty_col, col2,empty_col,col3= st.columns([0.8, 0.1, 1, 0.1, 0.9])  # Ajouter une colonne vide pour l'espacement

with col1:
    st.plotly_chart(fig_top_genres, use_container_width=True)
    st.plotly_chart(fig_popularity, use_container_width=True)
with col2:
    st.plotly_chart(fig_avg_duration, use_container_width=True)
    st.plotly_chart(fig_revenue, use_container_width=True)
with col3:
    st.plotly_chart(fig_popularity, use_container_width=True)
    st.plotly_chart(fig_revenue, use_container_width=True)

# Ajouter un espace vertical
st.write("")
st.write("")

# Ajouter un graphique plein sur toute la largeur en bas
st.plotly_chart(fig_custom, use_container_width=True)
col1, col2 = st.columns(2)














import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import streamlit as st
from PIL import Image
from streamlit_carousel import carousel
import os

# Configurer la page en mode large
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
# Ajouter un titre au tableau de bord
st.markdown("""
    <style>
    .title {
        text-align: left; 
        font-size: 30px; 
        font-weight: normal;
        font-family: Arial, sans-serif;
        -webkit-background-clip: text;
        color: rgba(78, 140, 255, 0.3); /* Couleur avec transparence */
        margin-top: -75px;  /* Monter le titre plus haut */
    }
    </style>
    <h1 class="title">Tableau de Bord des Films</h1>
    """, unsafe_allow_html=True)


# Liste des chemins des images et leurs descriptions
images_info = {
    'Distribution des Notes': {
        'path': 'distribution des note.png',
        'description': 'Analyse de la distribution des notes moyennes des films. Ce graphique permet de comprendre la répartition des notes attribuées aux films et de détecter d\'éventuelles anomalies ou biais dans les notes.'
    },
    'Évolution du Nombre de Films': {
        'path': 'évolution du nobre de film.png',
        'description': 'Évolution du nombre de films au fil des ans. Ce graphique aide à identifier les tendances de production de films au cours du temps et à repérer des périodes de production anormalement basses ou élevées.'
    },
    'Durée Moyenne des Films': {
        'path': 'durée moyenne des film.png',
        'description': 'Analyse de la durée moyenne des films par année. Ce graphique permet de voir comment la durée des films a évolué dans le temps et d\'identifier des anomalies dans les données de durée.'
    },
    'Fréquence des Genres': {
        'path': 'frenquence des genre.png',
        'description': 'Fréquence des différents genres de films. Ce graphique montre la popularité des différents genres et aide à repérer des genres sous-représentés ou sur-représentés.'
    },
    'Nombre de Films par Genre': {
        'path': 'nombre de fim par genre.png',
        'description': 'Nombre de films par genre. Ce graphique permet de comparer la production de films entre différents genres et de détecter des déséquilibres éventuels.'
    },
    'Répartition des Types de Films': {
        'path': 'répartition des type de film.png',
        'description': 'Répartition des types de films (documentaires, fictions, etc.). Ce graphique aide à comprendre la composition des données en termes de types de films et à vérifier la cohérence des types répertoriés.'
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
col1, col2 = st.columns([1.2, 1])

selected_image_index = st.session_state.carousel_index

# Définir les titres des boutons
prev_title = carousel_items_images[selected_image_index - 1]['title'] if selected_image_index > 0 else carousel_items_images[-1]['title']
next_title = carousel_items_images[(selected_image_index + 1) % len(carousel_items_images)]['title']

with col1:
    st.markdown("### Analyse avant nettoyage")
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
top_genres = filtered_data['Genres'].str.split(',', expand=True).stack().value_counts().nlargest(5)
top_genres_df = top_genres.reset_index()
top_genres_df.columns = ['Genre', 'Nombre de Films']

# Créer le graphique des Top 5 Genres par Nombre de Films
fig_top_genres = px.bar(top_genres_df, x='Genre', y='Nombre de Films',
                        title='Top 5 Genres par Nombre de Films',
                        text='Nombre de Films',
                        labels={'Nombre de Films': 'Nombre de Films', 'Genre': ''})

fig_top_genres.update_traces(marker_color='rgba(130, 89, 182, 9)', textposition='auto', textfont_size=15)
fig_top_genres = update_figure_layout(fig_top_genres, 'Top 5 Genres par Nombre de Films')

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
    background: linear-gradient(
        to right, 
        rgba(192, 192, 192, 0.8) -90%,  /* Couleur argentée avec transparence */
        rgba(34, 49, 86, 0.8) 95%,  /* Couleur plus foncée avec transparence */
        rgba(34, 49, 86, 0.8) 100%  /* Couleur plus foncée avec transparence */
    );  /* Dégradé de couleur */
    padding: 10px;  /* Ajustement de l'alignement */
    margin: 15px 10px;  /* Espacement entre les graphiques */
}
div.stPlotlyChart:hover {
    transform: scale(1.02);  /* Effet de zoom au survol */
    box-shadow: 5px 5px 10px rgba(105, 105, 130, 0.5);  /* Ombre floue */
}
</style>
""", unsafe_allow_html=True)
# Utiliser des conteneurs pour organiser les graphiques en colonnes et en lignes avec espacement
col1, empty_col, col2 = st.columns([0.8, 0.1, 0.8])  # Ajouter une colonne vide pour l'espacement
with col1:
    st.markdown("### Analyse après nettoyage")
    st.plotly_chart(fig_top_genres, use_container_width=True)
    st.plotly_chart(fig_popularity, use_container_width=True)

with col2:
    st.write("")
    st.write("")
    st.write("")
    st.plotly_chart(fig_avg_duration, use_container_width=True)
    st.plotly_chart(fig_revenue, use_container_width=True)

# Ajouter un espace vertical
st.write("")
st.write("")

# Ajouter un graphique plein sur toute la largeur en bas
st.plotly_chart(fig_custom, use_container_width=True)
col1, col2 = st.columns(2)
# Lire le fichier film_ml.parquet




