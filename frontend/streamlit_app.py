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
