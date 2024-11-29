import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

class GameRecommender:
    def __init__(self, data_path="cleaned_video_games.csv"):
        self.df = pd.read_csv(data_path)
        # Remove any rows with NaN values
        self.df = self.df.dropna()
        print(f"Loaded {len(self.df)} games")
        self.prepare_features()
        
    def prepare_features(self):
        # Create feature matrix
        genre_columns = [col for col in self.df.columns if col.startswith('genre_')]
        
        # Combine features
        features = ['platform_encoded', 'release_year', 'user_score'] + genre_columns
        
        # Scale numerical features
        scaler = MinMaxScaler()
        self.feature_matrix = self.df[features].copy()
        
        # Check for NaN values before scaling
        if self.feature_matrix.isnull().any().any():
            print("Warning: NaN values found in feature matrix")
            self.feature_matrix = self.feature_matrix.fillna(self.feature_matrix.mean())
            
        self.feature_matrix[['platform_encoded', 'release_year', 'user_score']] = scaler.fit_transform(
            self.feature_matrix[['platform_encoded', 'release_year', 'user_score']]
        )
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(self.feature_matrix)
    
    def get_recommendations(self, game_title, n_recommendations=5):
        # Find the game index
        game_title = game_title.strip().lower()
        matches = self.df[self.df['title'].str.lower() == game_title]
        
        if matches.empty:
            # Try fuzzy matching
            from difflib import get_close_matches
            titles = self.df['title'].str.lower().tolist()
            matches = get_close_matches(game_title, titles, n=1, cutoff=0.6)
            if not matches:
                return None, "Game not found. Please check the title and try again."
            game_title = matches[0]
            matches = self.df[self.df['title'].str.lower() == game_title]
        
        idx = matches.index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N recommendations
        sim_scores = sim_scores[1:n_recommendations+1]
        game_indices = [i[0] for i in sim_scores]
        
        recommendations = self.df.iloc[game_indices][['title', 'genre', 'platform', 'release_year', 'user_score']]
        recommendations['similarity_score'] = [score[1] for score in sim_scores]
        
        return self.df.iloc[idx]['title'], recommendations
    
    def get_random_game(self):
        """Return a random game from the dataset"""
        return self.df.sample(n=1)['title'].iloc[0]
