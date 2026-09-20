import streamlit as st
from datetime import datetime

from utils.predictor import predict_exercise
from utils.database import (
    init_db,
    create_user,
    login_user,
    save_workout,
    get_workouts
)

init_db()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "name" not in st.session_state:
    st.session_state.name = ""

st.set_page_config(
    page_title="Smart Fitness AI Coach",
    page_icon="🏋️",
    layout="wide"
)

# ---------------- LOGIN / SIGNUP ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🏋️ Smart Fitness AI Coach")
    st.write("AI-powered fitness coaching assistant")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input(
            "Password",
            type="password",
            key="login_pass"
        )

        if st.button("Login"):
            name = login_user(username, password)

            if name:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.name = name
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.subheader("Create Account")

        name = st.text_input("Full Name")
        username = st.text_input("Choose Username")
        password = st.text_input(
            "Create Password",
            type="password"
        )
        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Sign Up"):
            if not name or not username or not password:
                st.warning("Please fill all fields.")

            elif password != confirm:
                st.error("Passwords do not match.")

            elif len(password) < 6:
                st.warning("Password must contain at least 6 characters.")

            elif create_user(name, username, password):
                st.success("Account created successfully! Please login.")

            else:
                st.error("Username already exists.")

    st.stop()


# ---------------- LOGGED IN APP ----------------

st.sidebar.success(
    f" Welcome, {st.session_state.name}"
)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.pop("username", None)
    st.session_state.pop("name", None)
    st.rerun()

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


# ---------------- MAIN PAGE ----------------

st.title("🏋️ Smart Fitness AI Coach")

st.write(
    "Welcome to your AI-powered fitness coaching assistant."
)

st.info(
    "Enter a workout description and the AI will "
    "identify the corresponding exercise category."
)

st.subheader("🔍 Exercise / Workout Prediction")

user_input = st.text_input(
    "Enter your workout description:",
    placeholder="Example: running for 30 minutes"
)


# ---------------- PREDICTION ----------------

if st.button("Predict Exercise"):

    if not user_input.strip():
        st.warning("Please enter a workout description.")

    else:
        try:
            exercise, method = predict_exercise(user_input)

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

            st.session_state.last_workout = {
                "workout": user_input,
                "category": exercise,
                "method": method,
                "duration": duration,
                "weight": weight,
                "calories": calories
            }

        except Exception as e:
            st.error(f"Prediction error: {e}")


# ---------------- SHOW RESULT ----------------

if "last_workout" in st.session_state:

    w = st.session_state.last_workout

    st.success(
        f"🏋️ Predicted Exercise/Activity: **{w['category']}**"
    )

    st.info(
        f"🔎 Detection: **{w['method']}**"
    )

    st.metric(
        "🔥 Calories Burned",
        f"{w['calories']:.0f} Calories"
    )

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
            "Take sufficient rest."
        ]
    }

    st.subheader("💡 AI Workout Recommendations")

    for item in recommendations.get(w["category"], []):
        st.write("•", item)

    st.divider()

    if st.button("💾 Save Workout"):

        save_workout(
            st.session_state.username,
            w["workout"],
            w["category"],
            w["duration"],
            w["weight"],
            w["calories"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        st.success("✅ Workout saved to your history!")


# ---------------- WORKOUT HISTORY ----------------

st.divider()

st.subheader("📋 My Workout History")

history = get_workouts(st.session_state.username)

if history:

    for row in history:
        date, workout, category, duration, weight, calories = row

        with st.container(border=True):

            st.write(f"📅 **{date}**")
            st.write(f"🏋️ **Workout:** {workout}")
            st.write(f"🔹 **Category:** {category}")
            st.write(f"⏱️ **Duration:** {duration} min")
            st.write(f"⚖️ **Weight:** {weight} kg")
            st.write(f"🔥 **Calories:** {calories:.0f}")

else:
    st.info("No workouts saved yet.")

          
