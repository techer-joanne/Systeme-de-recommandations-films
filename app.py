import streamlit as st
import pandas as pd
from moteur_recommandation import get_recommendations_tfidf

# Configuration de la page en mode large
st.set_page_config(layout="wide", page_title="Movies recommandation", page_icon="🎬")

# CSS pour la mise en page avec le backdrop en arrière-plan
page_css = """
<style>
    .backdrop {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: cover;
        background-position: center;
        filter: blur(2px);
        z-index: -0;
    }
    .content {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        color: white;
        padding: 20px;
    }
    .poster {
        margin-right: 20px;
    }
    .info {
        max-width: 600px;
    }
    .zoom-effect img {
        border-radius: 10px;
        transition: transform .2s, box-shadow .2s;
        border: 1px solid #D3D3D3;
        box-shadow: 0 0 20px rgba(211, 211, 211, 0);
    }
    .zoom-effect img:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(211, 211, 211, 0.5);
    }
</style>
"""
st.markdown(page_css, unsafe_allow_html=True)

# Charger les données avec mise en cache
@st.cache_data
def load_data():
    df = pd.read_csv('df_final.csv')
    df['overview_french'] = df['overview_french'].fillna('')
    df['tconst'] = df['tconst'].astype(str)
    return df

# Charger les données
df = load_data()

# Afficher les détails du film si un ID de film est présent dans les paramètres d'URL
query_params = st.query_params
movie_id = query_params.get("movie_id", None)



if movie_id:
    # Page des détails du film
    movie_data = df[df['tconst'] == movie_id]

    # Débogage : Afficher les données du film récupéré
    st.write(f"Données du film récupéré : {movie_data}")

    if not movie_data.empty:
        movie_data = movie_data.iloc[0]  # Assure de récupérer une seule ligne
        backdrop_url = movie_data['backdrop_path']
        st.markdown(f'<div class="backdrop" style="background-image: url({backdrop_url});"></div>', unsafe_allow_html=True)
        
        # Affichage des détails du film
        st.markdown('<div class="content">', unsafe_allow_html=True)
        
        # Utilisation de colonnes pour la mise en page
        col1, col2, col3  = st.columns([1, 1.8, 0.8])
        
        with col1:
            st.image(movie_data['poster_path'], width=400)
        
        with col2:
            st.header(movie_data['Titre_Principal'])
            st.write(f"**Description**: {movie_data['overview_french']}")
            st.write(f"**Note**: {movie_data['moyenne']}")
            st.write(f"**Année**: {movie_data['Annee_Debut']}")
            st.write(f"**Durée**: {movie_data['Duree_Minutes']} minutes")
            st.write(f"**Genres**: {movie_data['Genres']}")
            st.write(f"**Acteurs**: {movie_data['actor_names']}")
            st.write(f"**Réalisateur**: {movie_data['primaryName_director']}")
            st.write(f"**Producteur**: {movie_data['primaryName_producer']}")
            st.write(f"**Scénariste**: {movie_data['primaryName_writer']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Affichage des recommandations
        recommendations = get_recommendations_tfidf(movie_data['Titre_Principal'])
        if recommendations is not None:
            st.header("Recommandations")
            num_cols = 5
            num_rows = len(recommendations) // num_cols + (len(recommendations) % num_cols > 0)
            for i in range(num_rows):
                cols = st.columns(num_cols)
                start_index = i * num_cols
                end_index = min((i + 1) * num_cols, len(recommendations))
                for col, index in zip(cols, range(start_index, end_index)):
                    rec_movie_data = recommendations.iloc[index]
                    with col:
                        if 'tconst' in rec_movie_data:
                            rec_tconst = rec_movie_data['tconst']
                            link = f"/?movie_id={rec_tconst}"
                            st.markdown(
                                f'<a href="{link}" target="_blank">'
                                f'<div class="zoom-effect">'
                                f'<img src="{rec_movie_data["poster_path"]}" width="100%">'
                                f'</div>'
                                f'</a>',
                                unsafe_allow_html=True
                            )
                            st.write(rec_movie_data['Titre_Principal'])
                        else:
                            st.write("Données de film manquantes pour 'tconst'.")
        else:
            st.write('Aucune recommandation trouvée pour ce film.')
    else:
        st.write("Film non trouvé pour cet identifiant.")
else:
    # Page d'accueil avec la vidéo
    video_html = """
    <style>
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
        .videoWrapper {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -0; /* Assure que la vidéo reste en arrière-plan */
        }
        iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover; /* Couvre tout l'espace sans respecter le ratio */
        }
        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.3); /* Superposition semi-transparente */
            z-index: 0;
        }
    </style>
    <div class="videoWrapper">
        <iframe src="https://www.youtube.com/embed/bYBMGMryhdM?autoplay=1&mute=1&loop=1&playlist=bYBMGMryhdM&controls=0&modestbranding=1&rel=0"
            frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            allowfullscreen></iframe>
    </div>
    <div class="overlay"></div>
    """
    st.markdown(video_html, unsafe_allow_html=True)

    # Sélection du film
    col1, col2, col3 = st.columns([0.8, 3, 0.8])
    
    with col1:
        st.write("")  # Colonne vide pour l'espacement
    
    with col2:
        selected_movie = st.selectbox('', df['Titre_Principal'].unique())
        if st.button('Recommander'):
            recommendations = get_recommendations_tfidf(selected_movie)
            if recommendations is not None:
                num_cols = 5
                num_rows = len(recommendations) // num_cols + (len(recommendations) % num_cols > 0)
                for i in range(num_rows):
                    cols = st.columns(num_cols)
                    start_index = i * num_cols
                    end_index = min((i + 1) * num_cols, len(recommendations))
                    for col, index in zip(cols, range(start_index, end_index)):
                        movie_data = recommendations.iloc[index]
                        with col:
                            if 'tconst' in movie_data:
                                tconst = movie_data['tconst']
                                link = f"/?movie_id={tconst}"
                                st.markdown(
                                    f'<a href="{link}" target="_blank">'
                                    f'<div class="zoom-effect">'
                                    f'<img src="{movie_data["poster_path"]}" width="100%">'
                                    f'</div>'
                                    f'</a>',
                                    unsafe_allow_html=True
                                )

                            else:
                                st.write("Données de film manquantes pour 'tconst'.")
            else:
                st.write('Aucune recommandation trouvée pour ce film.')
    
    with col3:
        st.write("")  # Colonne vide pour l'espacement
