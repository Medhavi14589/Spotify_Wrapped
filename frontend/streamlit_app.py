<<<<<<< Updated upstream
import streamlit as st
import pandas as pd
from ml.mood_model import predict_mood_distribution
from ml.recommender import recommend_similar_tracks

@st.cache_data
def load_track_names():
    df = pd.read_csv("data/spotify_tracks_final.csv")
    return sorted(df["track_name"].unique())

track_names = load_track_names()

st.set_page_config(page_title= "SPOTIFY WRAPPED", page_icon="🎧🎶", layout="wide")

st.title("🎶🎶 Spotify Wrapped 🎶🎶")
st.markdown("#### Your personal music insights, powered by ML")

top_mood, mood_distribution = predict_mood_distribution()

st.subheader("🎧 Your Top Mood 🔥")
st.success(f"Your most common vibe is 🥁🥁.....\n **{top_mood}**")

st.subheader("📊 Mood Distribution")
st.bar_chart(pd.Series(mood_distribution))

st.markdown("## *🔥 NOW FOR THE FUN INSIGHTS 🔥*")

if top_mood == "Energetic":
    st.write("You love high-energy tracks — probably gym or hype playlists 💪")
elif top_mood == "Chill":
    st.write("You prefer calm, acoustic vibes — late night listener 🌙")
elif top_mood == "Happy":
    st.write("You enjoy upbeat, feel-good music — main character energy ✨")
else:
    st.write("You lean towards emotional tracks — deep feels 🎭")

st.divider()
st.subheader("🎶 Recommended for You")

selected_track = st.selectbox(
    "Pick a song you like:",
    track_names
)

if selected_track:
    recs = recommend_similar_tracks(selected_track, top_k=5)

    if len(recs) == 0:
        st.warning("No recommendations found.")
    else:
        st.write(f"Because you liked **{selected_track}** 👇")

        for i, rec in enumerate(recs, start=1):
            st.markdown(
                f"**{i}. {rec['track_name']}**  \n"
                f"*{rec['artists']}* — {rec['track_genre']}"
            )
=======
"""
Spotify Wrapped - Home Page
Upload your Spotify playlist CSV to get started
"""

import streamlit as st
import requests
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Spotify Wrapped",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Spotify theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #191414 0%, #1a1a1a 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1DB954 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Text */
    p, li, label {
        color: #FFFFFF !important;
    }
    
    /* Cards */
    .stAlert {
        background-color: #282828;
        border: 1px solid #1DB954;
        border-radius: 10px;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 30px;
        padding: 10px 30px;
        font-weight: bold;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #1ed760;
    }
    
    /* File uploader */
    .stFileUploader {
        background-color: #282828;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #000000;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:5000"

def upload_to_api(file):
    """Upload CSV file to Flask API"""
    try:
        files = {'file': file}
        response = requests.post(f"{API_BASE_URL}/upload", files=files)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json().get('error', 'Upload failed')
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API. Please ensure Flask backend is running on port 5000."
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    # Initialize session state
    if 'data_uploaded' not in st.session_state:
        st.session_state.data_uploaded = False
    if 'upload_info' not in st.session_state:
        st.session_state.upload_info = None
    
    # Header
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>🎵 Spotify Wrapped</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #b3b3b3;'>Discover your music personality</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Check if data is already uploaded
    if st.session_state.data_uploaded:
        st.success("✅ Your playlist data is loaded!")
        
        if st.session_state.upload_info:
            info = st.session_state.upload_info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Tracks", info.get('rows', 'N/A'))
            with col2:
                duration_hours = info.get('preview', {}).get('total_duration_ms', 0) / (1000 * 60 * 60)
                st.metric("Total Hours", f"{duration_hours:.1f}")
            with col3:
                st.metric("Columns", len(info.get('columns', [])))
        
        st.info("👈 Navigate to **Your Wrapped** in the sidebar to explore your music!")
        
        if st.button("Upload New Playlist"):
            st.session_state.data_uploaded = False
            st.session_state.upload_info = None
            st.rerun()
    
    else:
        # Instructions
        st.markdown("### 📋 How to Get Started")
        
        with st.expander("🔍 Step 1: Export Your Playlist", expanded=True):
            st.markdown("""
            1. Go to [Exportify](https://watsonbox.github.io/exportify/)
            2. Log in with your Spotify account
            3. Find your playlist and click **Export**
            4. Download the CSV file
            
            ⚠️ **Note**: Exportify is a third-party tool. Make sure your CSV includes audio features!
            """)
        
        with st.expander("📤 Step 2: Upload Your CSV"):
            st.markdown("""
            Upload your exported playlist CSV file below. We'll analyze:
            - Your top songs and artists
            - Listening patterns over time
            - Audio features and mood distribution
            - Personalized recommendations
            """)
        
        st.markdown("---")
        
        # File upload section
        st.markdown("### 🎵 Upload Your Playlist")
        
        uploaded_file = st.file_uploader(
            "Choose your Spotify CSV file",
            type=['csv'],
            help="Export your playlist using Exportify"
        )
        
        if uploaded_file is not None:
            st.info(f"📁 File: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
            
            if st.button("🚀 Analyze My Music", type="primary"):
                with st.spinner("🎵 Processing your playlist..."):
                    # Reset file pointer
                    uploaded_file.seek(0)
                    
                    # Upload to API
                    success, result = upload_to_api(uploaded_file)
                    
                    if success:
                        st.session_state.data_uploaded = True
                        st.session_state.upload_info = result
                        st.success("✅ Upload successful! Redirecting...")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ Upload failed: {result}")
    
    # Sidebar info
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        This app analyzes your Spotify playlist to reveal:
        - 🎤 Top artists and tracks
        - 📅 Listening age and patterns
        - 🎨 Mood and audio features
        - 🎯 Personalized recommendations
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Status")
        
        # Check API health
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                health = response.json()
                st.success("✅ API Connected")
                st.caption(f"Backend: v{health.get('version', 'unknown')}")
            else:
                st.error("⚠️ API Error")
        except:
            st.error("❌ API Offline")
            st.caption("Start Flask backend on port 5000")

if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
