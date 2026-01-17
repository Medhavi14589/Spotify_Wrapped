import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------
# Load precomputed data (once)
# ---------------------------------
BASE_DIR = os.path.dirname(__file__)

tracks_path = os.path.join(BASE_DIR, "..", "data", "spotify_tracks_final.csv")
features_path = os.path.join(BASE_DIR, "..", "data", "spotify_features_normalized.csv")

tracks_df = pd.read_csv(tracks_path)
features_df = pd.read_csv(features_path)

# Keep only numeric columns for similarity
numeric_features = features_df.select_dtypes(include=["number"])




# ---------------------------------
# Recommender function
# ---------------------------------
def recommend_similar_tracks(track_name, top_k=5):
    """
    Recommend tracks similar to a given track name
    using cosine similarity (computed on-demand).
    """
    if track_name not in tracks_df["track_name"].values:
        return []

    idx = tracks_df[tracks_df["track_name"] == track_name].index[0]

    # Compute similarity ONLY for selected track
    target_vector = numeric_features.iloc[idx].values.reshape(1, -1)
    similarity_scores = cosine_similarity(target_vector, numeric_features.values)[0]

    # Get top-k similar tracks
    top_indices = similarity_scores.argsort()[::-1][1:top_k+1]

    recommendations = tracks_df.loc[top_indices, ["track_name", "artists", "track_genre"]]

    return recommendations.to_dict(orient="records")
