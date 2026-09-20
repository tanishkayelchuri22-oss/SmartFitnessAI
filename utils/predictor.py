from utils.model_loader import best_model, tfidf, label_encoder

KEYWORDS = {
    "Cardio": [
        "running", "run", "jogging", "cycling", "bike",
        "swimming", "walking", "treadmill", "cardio"
    ],
    "Olympic Weightlifting": [
        "snatch", "clean and jerk", "clean jerk"
    ],
    "Plyometrics": [
        "box jump", "box jumps", "jumping", "burpees",
        "plyometric", "jump squat"
    ],
    "Powerlifting": [
        "deadlift", "bench press", "squat", "powerlifting"
    ],
    "Stretching": [
        "stretching", "stretch", "yoga", "flexibility"
    ],
    "Strongman": [
        "strongman", "farmer walk", "atlas stone",
        "log press", "tire flip"
    ],
    "Strength": [
        "pull up", "pull-up", "push up", "push-up",
        "strength training", "weight training"
    ]
}

def predict_exercise(text):
    text = text.lower().strip()

    if not text:
        raise ValueError("Workout description cannot be empty.")

    # Rule-based prediction
    for activity, words in KEYWORDS.items():
        if any(word in text for word in words):
            return activity, "Keyword match"

    # ML prediction
    features = tfidf.transform([text])

    if features.shape[1] != best_model.n_features_in_:
        raise ValueError(
            f"Feature mismatch: {features.shape[1]} vs "
            f"{best_model.n_features_in_}"
        )

    prediction = best_model.predict(features)[0]

    # Model probability
    probabilities = best_model.predict_proba(features)[0]
    confidence = probabilities.max() * 100

    exercise = label_encoder.inverse_transform([prediction])[0]

    return exercise, f"AI model ({confidence:.1f}% confidence)"