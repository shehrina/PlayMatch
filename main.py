from recommender import GameRecommender
import time

def print_recommendations(input_game, recommendations):
    print(f"\nRecommendations based on '{input_game}':")
    print("\n" + "="*50)
    
    for _, game in recommendations.iterrows():
        print(f"\nTitle: {game['title']}")
        print(f"Genre: {game['genre']}")
        print(f"Platform: {game['platform']}")
        print(f"Release Year: {int(game['release_year'])}")
        print(f"User Score: {game['user_score']:.1f}")
        print(f"Similarity: {game['similarity_score']:.2%}")
        print("-"*50)

def main():
    print("Loading Video Game Recommender System...")
    recommender = GameRecommender()
    
    while True:
        print("\n=== Video Game Recommender ===")
        print("1. Get recommendations for a game")
        print("2. Get a random game suggestion")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            game_title = input("\nEnter a game title: ")
            input_game, recommendations = recommender.get_recommendations(game_title)
            
            if recommendations is None:
                print(f"\nError: {input_game}")
                continue
                
            print_recommendations(input_game, recommendations)
            
        elif choice == '2':
            random_game = recommender.get_random_game()
            print(f"\nRandom game suggestion: {random_game}")
            
            if input("\nWould you like recommendations based on this game? (y/n): ").lower() == 'y':
                input_game, recommendations = recommender.get_recommendations(random_game)
                print_recommendations(input_game, recommendations)
                
        elif choice == '3':
            print("\nThank you for using the Video Game Recommender!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")
        
        time.sleep(1)

if __name__ == "__main__":
    main() 