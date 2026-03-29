import os
import gdown
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from utils import preprocess_input

# 1. GOOGLE DRIVE FALLBACK IDs
# (These only trigger if the local files in ../models/ are missing)
MODEL_ID = "1brj880DvndZL2AUMmHsiDStYZINZ6eZo"
ENCODER_ID = "1taznZRWRpQWU50ShuLrQCtzJmWIWMZl8"
FEATURES_ID = "1E-5rqg-ACgGYl4EN-h98yBC32gOZbVoF"

# 2. PATH CONFIGURATION
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Matches your save logic: looks one folder up in 'models'
LOCAL_DIR = os.path.join(BASE_DIR, "..", "models")
# Cloud fallback: downloads to the current folder if local is missing
CLOUD_DIR = BASE_DIR

def get_file_path(filename, drive_id):
    local_path = os.path.join(LOCAL_DIR, filename)
    cloud_path = os.path.join(CLOUD_DIR, filename)
    
    # Check 1: Is it in the local ../models/ folder?
    if os.path.exists(local_path):
        return local_path
    
    # Check 2: Has it already been downloaded to the current folder?
    if os.path.exists(cloud_path):
        return cloud_path
    
    # Check 3: Download from Drive if both are missing
    print(f"File {filename} not found. Downloading from Drive...")
    url = f"https://drive.google.com/uc?export=download&id={drive_id}"
    gdown.download(url, cloud_path, quiet=False)
    return cloud_path

# --- LOAD SEQUENCE ---
try:
    m_path = get_file_path("best_model_top.pkl", MODEL_ID)
    e_path = get_file_path("encoder_top.pkl", ENCODER_ID)
    f_path = get_file_path("model_top_features.pkl", FEATURES_ID)

    # CRITICAL: mmap_mode='r' prevents the MemoryError on your 1.2GB model
    model = joblib.load(m_path, mmap_mode='r')
    encoder = joblib.load(e_path)
    model_features = joblib.load(f_path)
    print("✅ All models loaded successfully.")
except Exception as e:
    print(f"❌ Initialization Error: {e}")

# --- INTERNAL LOGIC FOR app.py ---
def predict_internal(data_dict):
    """Bypasses HTTP requests for better performance/reliability"""
    # Clean data via utils.py
    df = preprocess_input(data_dict, encoder, model_features)
    # Predict
    prediction = model.predict(df)[0]
    return float(prediction)

# --- FASTAPI SETUP (Optional/Standard) ---
app = FastAPI()

@app.post("/predict")
def predict_endpoint(data: dict):
    try:
        res = predict_internal(data)
        return {"prediction": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))