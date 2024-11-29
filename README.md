# PlayMatch

A video game recommendation system built with Python and Streamlit that helps users discover new games based on their preferences.

## Description

PlayMatch is an interactive web application that provides personalized video game recommendations. Using a content-based recommendation system, it analyzes game features such as genre, platform, and user scores to suggest similar games that users might enjoy.

## Features

- **Game Recommendations**: Get personalized game suggestions based on your favorite titles
- **Random Game Discovery**: Explore new games with a random game generator
- **Browse Database**: Search and filter through our comprehensive game database
- **Interactive UI**: User-friendly interface with detailed game information
- **Multiple Platforms**: Covers games across various gaming platforms
- **Similarity Scores**: See how closely recommended games match your preferences

## Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- NumPy

## Demo

playmatch.streamlit.app/

## Installation

1. Clone the repository: 
git clone https://github.com/shehrina/PlayMatch.git
2. Install required packages: 
pip install -r requirements.txt
3. Run the application: 
streamlit run app.py


## Data

The application uses a cleaned dataset of video games containing information about:
- Game titles
- Genres
- Platforms
- Release years
- User scores
- Critic scores

## How It Works

The recommendation system uses content-based filtering to suggest similar games. It:
1. Analyzes game features (genre, platform, release year, etc.)
2. Creates a similarity matrix using cosine similarity
3. Recommends games based on feature similarity scores

## Author

Your Name
- GitHub: [@shehrina]
- LinkedIn: www.linkedin.com/in/shehrinahossain

## Acknowledgments

- Data source: https://www.kaggle.com/datasets/beridzeg45/video-games
