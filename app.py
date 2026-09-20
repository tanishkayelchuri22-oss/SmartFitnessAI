import streamlit as st
from utils.predictor import predict_exercise
from utils.history import save_workout

st.set_page_config(
    page_title="Smart Fitness AI Coach",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ Smart Fitness AI Coach")
st.write("Welcome to your AI-powered fitness coaching assistant.")

st.info(
    "Enter a workout description and the AI will identify the "
    "corresponding exercise category."
)

# User details
st.sidebar.header("⚙️ User Settings")

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=30,
    max_value=200,
    value=70
)

duration = st.sidebar.number_input(
    "Workout duration (minutes)",
    min_value=1,
    max_value=300,
    value=30
)

st.subheader("🔍 Exercise / Workout Prediction")

user_input = st.text_input(
    "Enter your workout description:",
    placeholder="Example: running for 30 minutes"
)

if st.button("Predict Exercise"):

    if not user_input.strip():
        st.warning("Please enter a workout description.")

    else:
        try:
            exercise, method = predict_exercise(user_input)

            st.success(
                f"🏋️ Predicted Exercise/Activity: **{exercise}**"
            )

            st.info(f"🔎 Detection: **{method}**")

            # Activity-specific calorie calculation
            text = user_input.lower()

            if any(x in text for x in ["walking", "walk", "slow walk"]):
                met = 3.5

            elif any(x in text for x in ["running", "run", "jogging", "jog"]):
                met = 8.0

            elif any(x in text for x in ["cycling", "bike", "biking"]):
                met = 7.5

            elif any(x in text for x in ["swimming", "swim"]):
                met = 6.0

            elif exercise == "Strength":
                met = 6.0

            elif exercise == "Powerlifting":
                met = 6.0

            elif exercise == "Olympic Weightlifting":
                met = 6.0

            elif exercise == "Plyometrics":
                met = 8.0

            elif exercise == "Stretching":
                met = 3.0

            elif exercise == "Strongman":
                met = 7.0

            else:
                met = 5.0

            calories = met * 3.5 * weight / 200 * duration

            st.metric(
                "🔥 Estimated Calories Burned",
                f"{calories:.0f} Calories"
            )

            # Recommendations
            recommendations = {
                "Cardio": [
                    "Keep a steady pace.",
                    "Stay hydrated.",
                    "Include 5–10 minutes of cooldown."
                ],
                "Strength": [
                    "Focus on proper form.",
                    "Rest between sets.",
                    "Increase weight gradually."
                ],
                "Powerlifting": [
                    "Warm up thoroughly.",
                    "Prioritize technique.",
                    "Allow adequate recovery."
                ],
                "Olympic Weightlifting": [
                    "Practice technique with manageable weight.",
                    "Warm up shoulders and hips.",
                    "Avoid sacrificing form for weight."
                ],
                "Plyometrics": [
                    "Use proper landing technique.",
                    "Keep repetitions controlled.",
                    "Rest between explosive sets."
                ],
                "Stretching": [
                    "Hold stretches comfortably.",
                    "Avoid bouncing.",
                    "Breathe normally."
                ],
                "Strongman": [
                    "Use controlled movements.",
                    "Protect your lower back.",
                    "Take sufficient rest between heavy sets."
                ]
            }

            st.subheader("💡 AI Workout Recommendations")

            for item in recommendations.get(exercise, []):
                st.write("•", item)

        except Exception as e:
            st.error(f"Prediction error: {e}")