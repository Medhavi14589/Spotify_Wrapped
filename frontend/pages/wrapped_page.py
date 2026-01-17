"""
Spotify Wrapped - Sequential Feature Display
Navigate through your personalized music analysis
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient
from utils.visualizations import Visualizer

# Page config
st.set_page_config(
    page_title="Your Wrapped",
    page_icon="🎵",
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
    .feature-card {
        background-color: #282828;
        border-radius: 10px;
        padding: 30px;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize API client and visualizer
api = APIClient()
viz = Visualizer()

# Feature definitions
FEATURES = [
    {
        'id': 'top_songs',
        'title': '🎵 Your Top Songs',
        'description': 'The tracks that define your music taste'
    },
    {
        'id': 'top_artists',
        'title': '🎤 Your Top Artists',
        'description': 'The artists you can\'t stop listening to'
    },
    {
        'id': 'playlist_age',
        'title': '📅 Playlist Age',
        'description': 'How long you\'ve been curating this collection'
    },
    {
        'id': 'listening_age',
        'title': '🕰️ Listening Age',
        'description': 'The era your music taste belongs to'
    },
    {
        'id': 'temporal',
        'title': '📈 Songs Added Over Time',
        'description': 'Your listening journey visualized'
    },
    {
        'id': 'audio_features',
        'title': '🎨 Audio Feature Profile',
        'description': 'The sonic characteristics of your music'
    },
    {
        'id': 'mood_analysis',
        'title': '😊 Overall Mood Analysis',
        'description': 'The emotional landscape of your playlist'
    },
    {
        'id': 'popularity',
        'title': '⭐ Popularity Classification',
        'description': 'Are you a mainstream or underground listener?'
    },
    {
        'id': 'mood_radar',
        'title': '🎯 Mood Radar Plot',
        'description': 'Your emotional music profile at a glance'
    }
]

def render_feature(feature_idx):
    """Render a specific feature based on index"""
    feature = FEATURES[feature_idx]
    
    st.markdown(f"<h1 style='text-align: center;'>{feature['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 18px; color: #b3b3b3;'>{feature['description']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    feature_id = feature['id']
    
    # Top Songs
    if feature_id == 'top_songs':
        data = api.get_top_tracks(n=10)
        if data:
            tracks = data.get('top_tracks', [])
            for track in tracks:
                col1, col2, col3 = st.columns([1, 6, 2])
                with col1:
                    st.markdown(f"**#{track['rank']}**")
                with col2:
                    st.markdown(f"**{track['track_name']}**")
                    st.caption(f"by {track.get('artist', 'Unknown')}")
                with col3:
                    st.metric("Popularity", track['popularity'])
    
    # Top Artists
    elif feature_id == 'top_artists':
        data = api.get_top_artists(n=10)
        if data:
            artists = data.get('top_artists', [])
            fig = viz.plot_top_artists(artists)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show list
            st.markdown("### Artist Details")
            for artist in artists:
                col1, col2, col3 = st.columns([1, 6, 2])
                with col1:
                    st.markdown(f"**#{artist['rank']}**")
                with col2:
                    st.markdown(f"**{artist['artist']}**")
                with col3:
                    st.metric("Tracks", artist['track_count'])
    
    # Playlist Age
    elif feature_id == 'playlist_age':
        data = api.get_playlist_age()
        if data:
            age = data.get('playlist_age_years', 0)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                st.metric("Playlist Age", f"{age:.1f} years", delta="Time since first song")
            
            st.info(f"🎵 {data.get('interpretation', '')}")
            
            st.markdown("#### Timeline")
            st.write(f"**First Song:** {data.get('first_song_added', 'N/A')}")
            st.write(f"**Latest Song:** {data.get('latest_song_added', 'N/A')}")
    
    # Listening Age
    elif feature_id == 'listening_age':
        data = api.get_listening_age()
        if data:
            age = data.get('listening_age', 0)
            
            col1, col2, col3 = st.columns(3)
            with col2:
                st.metric("Listening Age", f"{age} years", delta="Average song age")
            
            st.info(f"🎵 {data.get('interpretation', '')}")
            
            st.markdown("#### Details")
            st.write(f"**Average Release Year:** {data.get('average_release_year', 'N/A')}")
            st.write(f"**Current Year:** {data.get('current_year', 'N/A')}")
    
    # Temporal Analysis
    elif feature_id == 'temporal':
        data = api.get_temporal_analysis()
        if data:
            monthly = data.get('monthly_trends', [])
            yearly = data.get('yearly_trends', [])
            
            # Plot yearly trends
            fig = viz.plot_temporal_trends(yearly, monthly)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"📊 Analyzed {data.get('total_tracks', 0)} tracks over time")
    
    # Audio Features
    elif feature_id == 'audio_features':
        data = api.get_stats()
        if data:
            # Get audio feature averages (we'll need to calculate from raw data)
            # For now, show a radar of key features
            fig = viz.plot_audio_features_radar(data)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("### Key Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Popularity", data.get('popularity', {}).get('average', 0))
            with col2:
                st.metric("Total Duration", f"{data.get('total_duration', {}).get('hours', 0):.1f} hrs")
            with col3:
                st.metric("Explicit %", f"{data.get('explicit', {}).get('percentage', 0)}%")
    
    # Mood Analysis
    elif feature_id == 'mood_analysis':
        data = api.get_mood_distribution()
        if data:
            mood_dist = data.get('mood_distribution', {})
            fig = viz.plot_mood_distribution(mood_dist)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show percentages
            st.markdown("### Mood Breakdown")
            cols = st.columns(4)
            moods = ['Happy', 'Sad', 'Energetic', 'Chill']
            emojis = ['😊', '😢', '⚡', '😌']
            
            for i, mood in enumerate(moods):
                if mood in mood_dist:
                    with cols[i]:
                        st.metric(f"{emojis[i]} {mood}", f"{mood_dist[mood].get('percentage', 0):.1f}%")
    
    # Popularity Distribution
    elif feature_id == 'popularity':
        data = api.get_popularity_distribution()
        if data:
            dist = data.get('distribution', {})
            fig = viz.plot_popularity_distribution(dist)
            st.plotly_chart(fig, use_container_width=True)
            
            # Show classification
            st.markdown("### Your Music Discovery Style")
            total = data.get('total_tracks', 1)
            
            high = dist.get('High', {}).get('count', 0)
            medium = dist.get('Medium', {}).get('count', 0)
            low = dist.get('Low', {}).get('count', 0)
            
            if high > medium and high > low:
                st.success("🌟 You're a **Mainstream Listener** - You love popular hits!")
            elif low > high:
                st.info("🎧 You're an **Underground Explorer** - You discover hidden gems!")
            else:
                st.warning("🎵 You're a **Balanced Listener** - Mix of popular and underground!")
    
    # Mood Radar
    elif feature_id == 'mood_radar':
        data = api.get_mood_distribution()
        if data:
            mood_dist = data.get('mood_distribution', {})
            fig = viz.plot_mood_radar(mood_dist)
            st.plotly_chart(fig, use_container_width=True)
            
            # Dominant mood
            if mood_dist:
                dominant = max(mood_dist.items(), key=lambda x: x[1].get('percentage', 0))
                st.success(f"🎯 Your dominant mood is **{dominant[0]}** at {dominant[1].get('percentage', 0):.1f}%")

def main():
    # Check if data is uploaded
    if not st.session_state.get('data_uploaded', False):
        st.warning("⚠️ Please upload your playlist data first!")
        st.info("👈 Go back to Home and upload your CSV file")
        return
    
    # Initialize feature index
    if 'feature_index' not in st.session_state:
        st.session_state.feature_index = 0
    
    # Progress indicator
    progress = (st.session_state.feature_index + 1) / len(FEATURES)
    st.progress(progress)
    st.caption(f"Feature {st.session_state.feature_index + 1} of {len(FEATURES)}")
    
    # Render current feature
    render_feature(st.session_state.feature_index)
    
    st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.feature_index > 0:
            if st.button("⬅️ Previous"):
                st.session_state.feature_index -= 1
                st.rerun()
    
    with col3:
        if st.session_state.feature_index < len(FEATURES) - 1:
            if st.button("Next ➡️"):
                st.session_state.feature_index += 1
                st.rerun()
        else:
            st.success("🎉 You've completed your Wrapped!")
            if st.button("🔄 Start Over"):
                st.session_state.feature_index = 0
                st.rerun()

if __name__ == "__main__":
    main()
