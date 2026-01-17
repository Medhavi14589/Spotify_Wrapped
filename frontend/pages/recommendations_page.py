"""
Spotify Wrapped - Recommendation Engine
Get personalized track recommendations based on similarity
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient

# Page config
st.set_page_config(
    page_title="Recommendations",
    page_icon="🎯",
    layout="wide"
)

# Apply Spotify theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #191414 0%, #1a1a1a 100%);
    }
    h1, h2, h3 { color: #1DB954 !important; }
    p, li, label { color: #FFFFFF !important; }
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 30px;
        padding: 10px 30px;
        font-weight: bold;
    }
    .stButton>button:hover { background-color: #1ed760; }
    .track-card {
        background-color: #282828;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #1DB954;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client
api = APIClient()

def main():
    st.markdown("<h1 style='text-align: center;'>🎯 Music Recommendations</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #b3b3b3;'>Discover similar tracks based on AI-powered recommendations</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize session state
    if 'selected_track' not in st.session_state:
        st.session_state.selected_track = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'track_names' not in st.session_state:
        st.session_state.track_names = None
    
    # Sidebar - Track selection
    with st.sidebar:
        st.markdown("### 🎵 Select a Track")
        
        # Load track names
        if st.session_state.track_names is None:
            with st.spinner("Loading tracks..."):
                track_data = api.get_track_names()
                if track_data:
                    st.session_state.track_names = track_data.get('track_names', [])
        
        if st.session_state.track_names:
            st.success(f"✅ {len(st.session_state.track_names)} tracks available")
            
            # Search box
            search_query = st.text_input("🔍 Search for a track", placeholder="Type to search...")
            
            # Filter tracks based on search
            if search_query:
                filtered_tracks = [t for t in st.session_state.track_names if search_query.lower() in t.lower()]
            else:
                filtered_tracks = st.session_state.track_names[:100]  # Show first 100
            
            selected = st.selectbox(
                "Choose a track:",
                options=filtered_tracks,
                help="Select a track to get recommendations"
            )
            
            st.session_state.selected_track = selected
            
            # Number of recommendations
            num_recs = st.slider("Number of recommendations", 5, 20, 10)
            
            # Get recommendations button
            if st.button("🎯 Get Recommendations", type="primary"):
                with st.spinner("Finding similar tracks..."):
                    recs = api.get_recommendations(st.session_state.selected_track, top_k=num_recs)
                    st.session_state.recommendations = recs
        else:
            st.error("❌ Could not load tracks")
            st.info("Make sure the Flask backend is running")
        
        st.markdown("---")
        
        # Random songs section
        st.markdown("### 🎲 Feeling Lucky?")
        if st.button("Get Random Songs"):
            with st.spinner("Selecting random tracks..."):
                random_data = api.get_random_songs(n=10)
                if random_data:
                    st.session_state.random_songs = random_data.get('random_songs', [])
    
    # Main content area
    if st.session_state.selected_track:
        st.markdown(f"### 🎵 Selected Track")
        st.info(f"**{st.session_state.selected_track}**")
        
        if st.session_state.recommendations:
            recs_data = st.session_state.recommendations
            
            if 'error' in recs_data:
                st.error(f"❌ {recs_data['error']}")
            else:
                recommendations = recs_data.get('recommendations', [])
                
                if recommendations:
                    st.markdown(f"### ✨ Top {len(recommendations)} Similar Tracks")
                    st.caption(f"Based on: {recs_data.get('source', 'Unknown')}")
                    
                    # Display recommendations
                    for i, rec in enumerate(recommendations, 1):
                        with st.container():
                            st.markdown(f"""
                            <div class='track-card'>
                                <h3>#{i} {rec['track_name']}</h3>
                                <p><strong>Artist:</strong> {rec['artists']}</p>
                                <p><strong>Genre:</strong> {rec.get('track_genre', 'N/A')}</p>
                                <p><strong>Similarity Score:</strong> {rec.get('similarity_score', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Additional info if available
                            col1, col2 = st.columns(2)
                            with col1:
                                if 'popularity' in rec:
                                    st.metric("Popularity", rec['popularity'])
                            with col2:
                                if 'year' in rec:
                                    st.metric("Year", rec['year'])
                            
                            st.markdown("---")
                else:
                    st.warning("No recommendations found")
        else:
            st.info("👈 Select a track from the sidebar and click 'Get Recommendations'")
    
    # Random songs section
    if 'random_songs' in st.session_state and st.session_state.random_songs:
        st.markdown("---")
        st.markdown("### 🎲 Random Tracks to Explore")
        
        cols = st.columns(2)
        for i, song in enumerate(st.session_state.random_songs):
            with cols[i % 2]:
                st.markdown(f"""
                <div class='track-card'>
                    <h4>{song['track_name']}</h4>
                    <p><strong>Artist:</strong> {song['artists']}</p>
                    <p><strong>Genre:</strong> {song.get('track_genre', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Info section
    st.markdown("---")
    with st.expander("ℹ️ How Recommendations Work"):
        st.markdown("""
        Our recommendation engine uses:
        - **K-Nearest Neighbors (KNN)** algorithm
        - **Audio features** like danceability, energy, valence, acousticness, tempo
        - **Euclidean distance** to find similar tracks
        - **Pre-trained model** on a large music dataset
        
        The similarity score shows how close tracks are in the feature space.
        Higher scores = more similar tracks!
        """)

if __name__ == "__main__":
    main()
