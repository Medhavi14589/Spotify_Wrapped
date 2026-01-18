import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import pickle
import os
import ast
import warnings
warnings.filterwarnings('ignore')

class SpotifyMusicRecommender:
    def __init__(self, data_path=None):
        """Initialize the recommender system with the dataset."""
        if data_path:
            print("Loading dataset...")
            self.df = pd.read_csv(data_path)
            print(f"Loaded {len(self.df)} songs")
            
            # Audio features to use for similarity
            self.feature_cols = ['valence', 'acousticness', 'danceability', 'energy', 
                                'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo']
            
            # Prepare the data
            self.prepare_data()
    
    def prepare_data(self):
        """Prepare and scale the feature data."""
        print("Preparing features...")
        
        # Normalize column names to lowercase
        self.df.columns = self.df.columns.str.lower()
        
        # Extract features
        self.features = self.df[self.feature_cols].copy()
        
        # Handle any missing values
        self.features = self.features.fillna(self.features.mean())
        
        # Scale features
        self.scaler = StandardScaler()
        self.scaled_features = self.scaler.fit_transform(self.features)
        
        # Build KNN model
        print("Building KNN model...")
        self.knn = NearestNeighbors(n_neighbors=50, metric='euclidean')
        self.knn.fit(self.scaled_features)
    
    def save_model(self, model_dir='../ml/'):
        """
        Save the trained model, scaler, and data to files.
        
        Parameters:
        -----------
        model_dir : str
            Directory to save model files (default: '../ml/')
        """
        os.makedirs(model_dir, exist_ok=True)
        
        # Save KNN model
        knn_path = os.path.join(model_dir, 'recommender_knn.pkl')
        with open(knn_path, 'wb') as f:
            pickle.dump(self.knn, f)
        
        # Save scaler
        scaler_path = os.path.join(model_dir, 'recommender_scaler.pkl')
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save data
        data_dict = {
            'df': self.df,
            'feature_cols': self.feature_cols,
            'scaled_features': self.scaled_features
        }
        data_path = os.path.join(model_dir, 'recommender_data.pkl')
        with open(data_path, 'wb') as f:
            pickle.dump(data_dict, f)
        
        print(f"✅ Model saved to {model_dir}")
    
    @classmethod
    def load_model(cls, model_dir='../ml/'):
        """
        Load a pre-trained model from files.
        
        Parameters:
        -----------
        model_dir : str
            Directory containing model files (default: '../ml/')
        
        Returns:
        --------
        SpotifyMusicRecommender
            Loaded recommender instance ready to use
        """
        print(f"Loading pre-trained model from {model_dir}...")
        
        # Create instance without initializing
        instance = cls.__new__(cls)
        
        # Load KNN model
        knn_path = os.path.join(model_dir, 'recommender_knn.pkl')
        with open(knn_path, 'rb') as f:
            instance.knn = pickle.load(f)
        
        # Load scaler
        scaler_path = os.path.join(model_dir, 'recommender_scaler.pkl')
        with open(scaler_path, 'rb') as f:
            instance.scaler = pickle.load(f)
        
        # Load data
        data_path = os.path.join(model_dir, 'recommender_data.pkl')
        with open(data_path, 'rb') as f:
            data_dict = pickle.load(f)
        
        instance.df = data_dict['df']
        instance.feature_cols = data_dict['feature_cols']
        instance.scaled_features = data_dict['scaled_features']
        
        print(f"✅ Model loaded successfully ({len(instance.df)} tracks)")
        return instance
    
    def get_track_names(self):
        """Get list of all track names."""
        if 'track_name' in self.df.columns:
            return sorted(self.df['track_name'].unique().tolist())
        elif 'name' in self.df.columns:
            return sorted(self.df['name'].unique().tolist())
        else:
            raise ValueError("No track name column found")
    
    def get_random_songs(self, n=10):
        """Get n random songs for rating."""
        random_indices = np.random.choice(len(self.df), size=min(n, len(self.df)), replace=False)
        return self.df.iloc[random_indices].copy()
    
    def display_song(self, song, index=None):
        """Display song information in a readable format."""
        if index is not None:
            print(f"\n{index}.")
        
        # Try to get track name (handle different column names)
        track_name = song.get('track_name') or song.get('name', 'Unknown')
        
        # Parse artists if it's a string representation of a list
        artists = song.get('artists') or song.get('artist_name(s)', 'Unknown')
        if isinstance(artists, str):
            try:
                artists = ast.literal_eval(artists)
                if isinstance(artists, list):
                    artists = ', '.join(artists)
            except:
                pass
        
        print(f"  Song: {track_name}")
        print(f"  Artist(s): {artists}")
        
        if 'year' in song:
            print(f"  Year: {int(song['year'])}")
        
        if 'popularity' in song:
            print(f"  Popularity: {song['popularity']}")
    
    def recommend_by_track_name(self, track_name, n_recommendations=10):
        """
        Recommend songs similar to a given track name.
        
        Parameters:
        -----------
        track_name : str
            Name of the track
        n_recommendations : int
            Number of recommendations to return
        
        Returns:
        --------
        DataFrame
            Recommended tracks
        """
        # Find the track (case-insensitive)
        track_col = 'track_name' if 'track_name' in self.df.columns else 'name'
        mask = self.df[track_col].str.lower() == track_name.lower()
        
        if not mask.any():
            return pd.DataFrame()  # Track not found
        
        # Get the first matching track
        track_idx = self.df[mask].index[0]
        
        # Get scaled features for this track
        track_features = self.scaled_features[track_idx].reshape(1, -1)
        
        # Find similar songs
        distances, indices = self.knn.kneighbors(track_features, n_neighbors=n_recommendations+1)
        
        # Exclude the track itself (first result)
        recommendation_indices = indices[0][1:]
        
        # Get recommended songs
        recommended_songs = self.df.iloc[recommendation_indices].copy()
        recommended_songs['similarity_score'] = 1 - distances[0][1:]  # Convert distance to similarity
        
        return recommended_songs
    
    def get_user_ratings(self):
        """Get user ratings for 20 random songs."""
        print("\n" + "="*70)
        print("MUSIC RECOMMENDATION SYSTEM")
        print("="*70)
        print("\nYou will be shown 10 random songs.")
        print("Please rate each song on a scale of 1-5:")
        print("  1 = Don't like at all")
        print("  2 = Don't really like")
        print("  3 = It's okay")
        print("  4 = Like it")
        print("  5 = Love it")
        print("\nIf you haven't heard the song, give your best guess based on the artist/info!")
        print("="*70)
        
        random_songs = self.get_random_songs(20)
        ratings = []
        rated_songs = []
        
        for idx, (_, song) in enumerate(random_songs.iterrows(), 1):
            self.display_song(song, idx)
            
            while True:
                try:
                    rating = input("  Your rating (1-5): ").strip()
                    rating = int(rating)
                    if 1 <= rating <= 5:
                        ratings.append(rating)
                        rated_songs.append(song)
                        break
                    else:
                        print("  Please enter a number between 1 and 5.")
                except ValueError:
                    print("  Please enter a valid number.")
        
        return pd.DataFrame(rated_songs), np.array(ratings)
    
    def recommend_songs(self, rated_songs_df, ratings, n_recommendations=10):
        """Recommend songs based on user ratings using weighted KNN."""
        print("\n" + "="*70)
        print("GENERATING RECOMMENDATIONS...")
        print("="*70)
        
        # Get indices of rated songs
        rated_indices = rated_songs_df.index.tolist()
        
        # Normalize ratings to use as weights (higher rating = higher weight)
        weights = ratings / ratings.sum()
        
        # Get scaled features for rated songs
        rated_features = self.scaled_features[rated_indices]
        
        # Calculate weighted average of liked songs' features
        weighted_profile = np.average(rated_features, axis=0, weights=weights)
        
        # Find similar songs using KNN
        distances, indices = self.knn.kneighbors([weighted_profile], n_neighbors=100)
        
        # Filter out songs that were already rated
        recommendations = []
        for idx in indices[0]:
            if idx not in rated_indices:
                recommendations.append(idx)
            if len(recommendations) >= n_recommendations:
                break
        
        # Get recommended songs
        recommended_songs = self.df.iloc[recommendations]
        
        return recommended_songs
    
    def display_recommendations(self, recommended_songs):
        """Display the recommended songs."""
        print("\n🎵 YOUR PERSONALIZED RECOMMENDATIONS 🎵\n")
        
        for idx, (_, song) in enumerate(recommended_songs.iterrows(), 1):
            self.display_song(song, idx)
        
        print("\n" + "="*70)
        print("Enjoy your personalized music recommendations!")
        print("="*70)
    
    def run(self):
        """Run the complete recommendation system."""
        # Get user ratings
        rated_songs, ratings = self.get_user_ratings()
        
        # Generate recommendations
        recommendations = self.recommend_songs(rated_songs, ratings, n_recommendations=10)
        
        # Display recommendations
        self.display_recommendations(recommendations)
        
        return recommendations


def main():
    """Main function to run the recommender system."""
    data_path = "spotify_data.csv"
    
    # Initialize and run the recommender
    recommender = SpotifyMusicRecommender(data_path)
    recommendations = recommender.run()
    
    # Optionally save recommendations to a file
    print("\nWould you like to save your recommendations? (yes/no): ", end='')
    save_choice = input().strip().lower()
    
    if save_choice in ['yes', 'y']:
        output_path = 'recommendations.csv'
        recommendations.to_csv(output_path, index=False)
        print(f"\n✅ Recommendations saved to: {output_path}")


if __name__ == "__main__":
    main()
