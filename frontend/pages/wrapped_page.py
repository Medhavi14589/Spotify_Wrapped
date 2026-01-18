"""
Spotify Wrapped - Sequential Feature Display
Navigate through your personalized music analysis
"""
import base64
import streamlit as st
import sys
from pathlib import Path

from frontend.frontend_config import (
    SPOTIFY_CSS, 
    WRAPPED_CARD_CSS, 
    WRAPPED_CARD_CONFIG
)

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.api_client import APIClient
from utils.visualizations import Visualizer

def get_base64_image(image_path):
    """Convert local image to base64 for embedding"""
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return ""

# Page config
st.set_page_config(
    page_title="Your Wrapped",
    page_icon="🎵",
    layout="wide"
)

# Apply Spotify theme + Wrapped Card styling
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
    
    /* Import Circular and Dela Gothic One fonts */
    @import url('https://fonts.googleapis.com/css2?family=Dela+Gothic+One&display=swap');
    
    /* Wrapped Card Container */
    .wrapped-card {
        width: 450px;
        height: 800px;
        margin: 20px auto;
        border-radius: 20px;
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display: flex;
        flex-direction: column;
        padding: 40px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        position: relative;
    }   
    
    /* Text inside Wrapped Card */
    .wrapped-card h1,
    .wrapped-card h2,
    .wrapped-card h3,
    .wrapped-card p,
    .wrapped-card span {
        font-family: 'Circular', 'Helvetica Neue', sans-serif !important;
        text-align: center !important;
        color: white !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        margin: 10px 0;
    }
    
    /* Title text */
    .wrapped-card .card-title {
        font-family: 'Dela Gothic One', sans-serif !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        margin-bottom: 15px;
        line-height: 1.2;
    }
    
    /* Description text */
    .wrapped-card .card-description {
        font-family: 'Circular', sans-serif !important;
        font-size: 16px !important;
        font-weight: 500;
        opacity: 0.95;
    }
    
    /* Overlay for better text readability */
    .wrapped-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(180deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.5) 100%);
        border-radius: 20px;
        z-index: 1;
    }
    
    /* Ensure content is above overlay */
    .wrapped-card > * {
        position: relative;
        z-index: 2;
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
    
    # Background image URLs for each feature - REPLACE WITH YOUR PATHS
    background_images = {
        'top_songs': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw1.png'),
        'top_artists': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw2.png'),
        'playlist_age': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw3.png'),
        'listening_age': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw1.png'),
        'temporal': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw2.png'),
        'audio_features': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw3.png'),
        'mood_analysis': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw1.png'),
        'popularity': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw2.png'),
        'mood_radar': get_base64_image(r'E:\MIT\Spotify_wrapped2.0\Spotify_Wrapped_2\sw3.png')
    }
    
    feature_id = feature['id']
    bg_image = background_images.get(feature_id, '')
    
    # LISTENING AGE - All content inside card
    if feature_id == 'listening_age':
        data = api.get_listening_age()
        if data:
            age = data.get('listening_age', 0)
            avg_year = data.get('average_release_year', 'N/A')
            current_year = data.get('current_year', 'N/A')
            interpretation = data.get('interpretation', '')
            
            # Single consolidated HTML block
            html_content = f'''
    <div class="wrapped-card" style="background-image: url('{bg_image}'); justify-content: space-between; padding: 50px 30px;">
        <div style="text-align: center;">
            <h1 style="font-family: 'Dela Gothic One', sans-serif; font-size: 28px; font-weight: 900; margin-bottom: 15px; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">{feature['title']}</h1>
            <p style="font-family: 'Circular', sans-serif; font-size: 16px; font-weight: 500; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">{feature['description']}</p>
        </div>
        <div style="text-align: center; margin: 50px 0;">
            <div style="font-family: 'Dela Gothic One', sans-serif; font-size: 72px; font-weight: 900; color: #1DB954; text-shadow: 4px 4px 16px rgba(0, 0, 0, 0.9); line-height: 0.9;">{age}</div>
            <p style="font-family: 'Dela Gothic One', sans-serif; font-size: 24px; font-weight: 700; margin-top: 20px; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);">years</p>
            <p style="font-family: 'Circular', sans-serif; font-size: 16px; margin-top: 10px; color: rgba(255, 255, 255, 0.9); text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">Average song age</p>
        </div>
        <div style="background: rgba(0, 0, 0, 0.75); border-radius: 15px; padding: 25px; width: 100%; backdrop-filter: blur(10px);">
            <h4 style="font-family: 'Dela Gothic One', sans-serif; font-size: 18px; text-align: center; margin-bottom: 15px; color: white; letter-spacing: 1px;">DETAILS</h4>
            <p style="font-family: 'Circular', sans-serif; font-size: 15px; text-align: center; margin: 8px 0; color: rgba(255, 255, 255, 0.95);"><strong>Avg Release Year:</strong> {avg_year}</p>
            <p style="font-family: 'Circular', sans-serif; font-size: 15px; text-align: center; margin: 8px 0; color: rgba(255, 255, 255, 0.95);"><strong>Current Year:</strong> {current_year}</p>
        </div>
    </div>
    '''
            
            st.markdown(html_content, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.info(f"🎵 {interpretation}")
        
        return

    # PLAYLIST AGE - All content inside card
    elif feature_id == 'playlist_age':
        data = api.get_playlist_age()
        if data:
            age = data.get('playlist_age_years', 0)
            first_song = data.get('first_song_added', 'N/A')
            latest_song = data.get('latest_song_added', 'N/A')
            interpretation = data.get('interpretation', '')
            
            # Single consolidated HTML block
            html_content = f'''
    <div class="wrapped-card" style="background-image: url('{bg_image}'); justify-content: space-between; padding: 50px 30px;">
        <div style="text-align: center;">
            <h1 style="font-family: 'Dela Gothic One', sans-serif; font-size: 28px; font-weight: 900; margin-bottom: 15px; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">{feature['title']}</h1>
            <p style="font-family: 'Circular', sans-serif; font-size: 16px; font-weight: 500; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">{feature['description']}</p>
        </div>
        <div style="text-align: center; margin: 50px 0;">
            <div style="font-family: 'Dela Gothic One', sans-serif; font-size: 72px; font-weight: 900; color: #1DB954; text-shadow: 4px 4px 16px rgba(0, 0, 0, 0.9); line-height: 0.9;">{age:.1f}</div>
            <p style="font-family: 'Dela Gothic One', sans-serif; font-size: 24px; font-weight: 700; margin-top: 20px; color: white; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.9);">years</p>
            <p style="font-family: 'Circular', sans-serif; font-size: 16px; margin-top: 10px; color: rgba(255, 255, 255, 0.9); text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);">Time since first song</p>
        </div>
        <div style="background: rgba(0, 0, 0, 0.75); border-radius: 15px; padding: 25px; width: 100%; backdrop-filter: blur(10px);">
            <h4 style="font-family: 'Dela Gothic One', sans-serif; font-size: 18px; text-align: center; margin-bottom: 15px; color: white; letter-spacing: 1px;">TIMELINE</h4>
            <p style="font-family: 'Circular', sans-serif; font-size: 14px; text-align: center; margin: 8px 0; color: rgba(255, 255, 255, 0.95);"><strong>First Song:</strong><br/>{first_song}</p>
            <p style="font-family: 'Circular', sans-serif; font-size: 14px; text-align: center; margin: 8px 0; color: rgba(255, 255, 255, 0.95);"><strong>Latest Song:</strong><br/>{latest_song}</p>
        </div>
    </div>
    '''
            
            st.markdown(html_content, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.info(f"🎵 {interpretation}")
        
        return
    
    # ========================================================================
    # DEFAULT RENDERING: Card at top, content below
    # ========================================================================
    
    st.markdown(f"""
    <div class="wrapped-card" style="background-image: url('{bg_image}'); justify-content: flex-start; padding-top: 80px;">
        <h1 class="card-title">{feature['title']}</h1>
        <p class="card-description">{feature['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Content sections below the card
    
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
            
            st.markdown("### Artist Details")
            for artist in artists:
                col1, col2, col3 = st.columns([1, 6, 2])
                with col1:
                    st.markdown(f"**#{artist['rank']}**")
                with col2:
                    st.markdown(f"**{artist['artist']}**")
                with col3:
                    st.metric("Tracks", artist['track_count'])
    
    # Temporal Analysis
    elif feature_id == 'temporal':
        data = api.get_temporal_analysis()
        if data:
            monthly = data.get('monthly_trends', [])
            yearly = data.get('yearly_trends', [])
            
            fig = viz.plot_temporal_trends(yearly, monthly)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"📊 Analyzed {data.get('total_tracks', 0)} tracks over time")
    
    # Audio Features
    elif feature_id == 'audio_features':
        data = api.get_stats()
        if data:
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
            
            st.markdown("### Your Music Discovery Style")
            
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