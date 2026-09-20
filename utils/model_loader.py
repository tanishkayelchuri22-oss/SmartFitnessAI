import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")

best_model = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
tfidf = joblib.load(os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

if best_model.n_features_in_ != len(tfidf.vocabulary_):
    raise ValueError(
        f"Feature mismatch: model expects {best_model.n_features_in_}, "
        f"but TF-IDF has {len(tfidf.vocabulary_)} features."
    )

print(f"Model features: {best_model.n_features_in_}")
print(f"TF-IDF features: {len(tfidf.vocabulary_)}")
print("All models loaded successfully!")