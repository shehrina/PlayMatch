import pandas as pd
import ast
from sklearn.preprocessing import LabelEncoder

# Load the dataset
file_path = "all_video_games(cleaned).csv"  
df = pd.read_csv(file_path)

# Extract platform information from the Platforms Info column
def extract_primary_platform(platforms_str):
    try:
        platforms = ast.literal_eval(platforms_str)
        return platforms[0]['Platform']
    except:
        return None

# Clean and prepare the data
print("Cleaning data...")
df['platform'] = df['Platforms Info'].apply(extract_primary_platform)
df['genre'] = df['Genres']
df['title'] = df['Title']
df['release_year'] = pd.to_datetime(df['Release Date'], errors='coerce').dt.year
df['user_score'] = pd.to_numeric(df['User Score'], errors='coerce')

# Fill missing values
df['genre'] = df['genre'].fillna('unknown')
df['user_score'] = df['user_score'].fillna(df['user_score'].mean())
df['release_year'] = df['release_year'].fillna(df['release_year'].median())
df['platform'] = df['platform'].fillna('unknown')

# Remove rows with any remaining NaN values
df = df.dropna()

# Normalize text data
df['genre'] = df['genre'].str.lower()
df['platform'] = df['platform'].str.lower()
df['title'] = df['title'].str.strip()

# One-hot encode genres
print("\nEncoding genres...")
genres_encoded = pd.get_dummies(df['genre'], prefix='genre')
df = pd.concat([df, genres_encoded], axis=1)

# Label encode platforms
print("\nEncoding platforms...")
le = LabelEncoder()
df['platform_encoded'] = le.fit_transform(df['platform'])

# Select relevant columns
cleaned_df = df[[
    'title', 
    'genre',
    'platform',
    'platform_encoded',
    'release_year',
    'user_score'
] + [col for col in df.columns if col.startswith('genre_')]]

# Final check for any remaining NaN values
cleaned_df = cleaned_df.dropna()

# Save the cleaned dataset
output_path = "cleaned_video_games.csv"
cleaned_df.to_csv(output_path, index=False)
print(f"Cleaned dataset saved to {output_path}")

# Print some statistics
print(f"\nDataset statistics:")
print(f"Total number of games: {len(cleaned_df)}")
print(f"Number of unique genres: {len(genres_encoded.columns)}")
print(f"Number of unique platforms: {len(cleaned_df['platform'].unique())}")
print(f"Year range: {int(cleaned_df['release_year'].min())} - {int(cleaned_df['release_year'].max())}")