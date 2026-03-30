import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from utils import preprocess_input

# 1. PATH CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DIR = os.path.join(BASE_DIR, "..", "models")

def get_local_file(filename):
    path = os.path.join(LOCAL_DIR, filename)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} not found in {LOCAL_DIR}")
    
    return path

# --- LOAD SEQUENCE ---
try:
    m_path = get_local_file("best_model_top.pkl")
    e_path = get_local_file("encoder_top.pkl")
    f_path = get_local_file("model_top_features.pkl")

    # mmap_mode for large model
    model = joblib.load(m_path, mmap_mode='r')
    encoder = joblib.load(e_path)
    model_features = joblib.load(f_path)

    print("✅ All models loaded successfully from local storage.")

except Exception as e:
    print(f"❌ Initialization Error: {e}")
    raise e  # important: crash early instead of silent failure

# --- INTERNAL LOGIC ---
def predict_internal(data_dict):
    df = preprocess_input(data_dict, encoder, model_features)
    prediction = model.predict(df)[0]
    return float(prediction)

# --- FASTAPI ---
app = FastAPI()

@app.post("/predict")
def predict_endpoint(data: dict):
    try:
        res = predict_internal(data)
        return {"prediction": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))