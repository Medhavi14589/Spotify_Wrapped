from flask import Flask, jsonify
from ml.mood_model import predict_mood_distribution

# ---------------------------------
# Create Flask app
# ---------------------------------
app = Flask(__name__)

# ---------------------------------
# Health Check Route
# ---------------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "ml_ready": True
    })

# ---------------------------------
# Mood Prediction Route
# ---------------------------------
@app.route("/predict-mood", methods=["POST"])
def predict_mood():
    try:
        top_mood, mood_distribution = predict_mood_distribution()
        return jsonify({
            "top_mood": top_mood,
            "mood_distribution": mood_distribution
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------
# Main Entry Point
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=True)
