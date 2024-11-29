import streamlit as st
from recommender import GameRecommender
import pandas as pd

# Custom CSS for gradient background, fonts, and styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        @font-face {
            font-family: 'Pixel Game';
            src: url('https://db.onlinewebfonts.com/t/b2e75c336df191233b3096682c9ee6be.eot');
            src: url('https://db.onlinewebfonts.com/t/b2e75c336df191233b3096682c9ee6be.woff2') format('woff2'),
                 url('https://db.onlinewebfonts.com/t/b2e75c336df191233b3096682c9ee6be.woff') format('woff');
        }
        
        .stApp {
            background: linear-gradient(
                45deg,
                rgba(0,32,0,1) 0%,
                rgba(0,15,30,1) 50%,
                rgba(25,0,35,1) 100%
            );
        }
        
        /* Style sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(
                45deg,
                rgba(0,32,0,1) 0%,
                rgba(0,15,30,1) 50%,
                rgba(25,0,35,1) 100%
            );
        }
        
        /* Title styling */
        h1 {
            font-family: 'Press Start 2P', cursive !important;
            text-shadow: 0 0 10px rgba(0,255,0,0.5);
            padding: 20px 0;
        }
        
        /* Subheader styling */
        h2 {
            font-family: 'Pixel Game', sans-serif !important;
            text-shadow: 0 0 8px rgba(0,255,0,0.3);
        }
        
        /* Make text more visible on dark background */
        .stMarkdown, .stText, p, label {
            color: rgba(255, 255, 255, 0.9) !important;
        }
        
        /* Style buttons */
        .stButton button {
            background: linear-gradient(
                90deg,
                rgba(55,125,55,0.8) 0%,
                rgba(55,85,125,0.8) 100%
            );
            color: white;
            border: none;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 15px rgba(0,255,0,0.5);
        }
        
        /* Style expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(
                90deg,
                rgba(55,125,55,0.2) 0%,
                rgba(55,85,125,0.2) 100%
            );
            border: none;
            border-left: 3px solid rgba(0,255,0,0.5);
        }
        
        /* Style success messages */
        .stSuccess {
            background: linear-gradient(
                90deg,
                rgba(55,125,55,0.2) 0%,
                rgba(55,85,125,0.2) 100%
            );
            border-left: 3px solid rgba(0,255,0,0.5);
        }
        
        /* Add some glow effects */
        .stApp div:hover {
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            box-shadow: 0 0 10px rgba(0,255,0,0.2);
        }

        /* Style radio buttons in sidebar */
        .stRadio > label {
            color: white !important;
        }
        
        /* Style sidebar text */
        .css-1d391kg, .css-1d391kg a {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize the recommender
@st.cache_resource
def load_recommender():
    return GameRecommender()

def main():
    st.title("PlayMatch")
    
    # Initialize recommender
    recommender = load_recommender()
    
    # Sidebar
    st.sidebar.header("Options")
    mode = st.sidebar.radio(
        "Choose Mode",
        ["Get Recommendations", "Random Game", "Browse Games"]
    )
    
    if mode == "Get Recommendations":
        st.header("Get Game Recommendations")
        
        # Create a text input for the game title
        game_title = st.text_input("Enter a game title:")
        n_recommendations = st.slider("Number of recommendations:", 1, 20, 5)
        
        if st.button("Get Recommendations"):
            if game_title:
                input_game, recommendations = recommender.get_recommendations(game_title, n_recommendations)
                
                if recommendations is None:
                    st.error(input_game)  # Show error message
                else:
                    st.success(f"Showing recommendations based on: {input_game}")
                    
                    # Display recommendations in a nice format
                    for _, game in recommendations.iterrows():
                        with st.expander(f"🎮 {game['title']} ({int(game['release_year'])})"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Genre:** {game['genre']}")
                                st.write(f"**Platform:** {game['platform']}")
                            with col2:
                                st.write(f"**User Score:** {game['user_score']:.1f}/10")
                                st.write(f"**Similarity:** {game['similarity_score']:.1%}")
            else:
                st.warning("Please enter a game title")
                
    elif mode == "Random Game":
        st.header("Discover Random Games")
        
        # Use session state to store the random game and recommendation state
        if 'random_game' not in st.session_state:
            st.session_state.random_game = None
            st.session_state.show_recommendations = False
            
        if st.button("Get Random Game"):
            st.session_state.random_game = recommender.get_random_game()
            st.session_state.show_recommendations = False  # Reset recommendations when new game is selected
            
        # Only show the random game and recommendation button if we have a game
        if st.session_state.random_game:
            st.success(f"Random game suggestion: {st.session_state.random_game}")
            
            # Add a button to show recommendations
            if st.button("Get Recommendations for this Game"):
                st.session_state.show_recommendations = True
            
            # Show recommendations if button was clicked
            if st.session_state.show_recommendations:
                input_game, recommendations = recommender.get_recommendations(st.session_state.random_game)
                
                st.subheader("Similar Games:")
                for _, game in recommendations.iterrows():
                    with st.expander(f"🎮 {game['title']} ({int(game['release_year'])})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Genre:** {game['genre']}")
                            st.write(f"**Platform:** {game['platform']}")
                        with col2:
                            st.write(f"**User Score:** {game['user_score']:.1f}/10")
                            st.write(f"**Similarity:** {game['similarity_score']:.1%}")
    
    else:  # Browse Games
        st.header("Browse Games Database")
        
        # Add search and filter options
        search_term = st.text_input("Search games:")
        
        # Get unique values for filtering
        genres = sorted(recommender.df['genre'].unique())
        platforms = sorted(recommender.df['platform'].unique())
        
        col1, col2 = st.columns(2)
        with col1:
            selected_genre = st.multiselect("Filter by genre:", genres)
        with col2:
            selected_platform = st.multiselect("Filter by platform:", platforms)
            
        # Filter the dataframe
        filtered_df = recommender.df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False)]
        if selected_genre:
            filtered_df = filtered_df[filtered_df['genre'].isin(selected_genre)]
        if selected_platform:
            filtered_df = filtered_df[filtered_df['platform'].isin(selected_platform)]
            
        # Display the filtered dataframe
        st.dataframe(
            filtered_df[['title', 'genre', 'platform', 'release_year', 'user_score']]
            .sort_values('user_score', ascending=False)
        )
        
        st.write(f"Showing {len(filtered_df)} games")

if __name__ == "__main__":
    main() 