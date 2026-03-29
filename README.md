# 🛒 Walmart Sales Prediction Project

This project implements an end-to-end machine learning pipeline to predict weekly sales. It includes data preprocessing, feature engineering, model selection, and optimization using feature importance.

---

## 📁 Project Structure

- `datacleaning.ipynb` → Data ingestion, merging, preprocessing  
- `modeltraining.ipynb` → Model training, evaluation, optimization  
- `models/`
  - `best_model_top.pkl`
  - `encoder_top.pkl`
  - `model_top_features.pkl`
  - `raw_top_features.pkl`

---

## 🛠️ Data Cleaning & Preprocessing

The dataset is built by combining:
- `features.csv`
- `stores.csv`
- `train.csv`

### Key Steps

- **Dataset Merging**
  - Joined on `Store`, `Date`, `IsHoliday` (left join)

- **Missing Value Handling**
  - Filled `MarkDown` columns with `0`
  - Applied forward fill (`ffill`) for:
    - CPI
    - Unemployment (grouped by Store)

- **Feature Engineering**
  - Extracted:
    - Year
    - Month
    - Week (from Date column)

- **Data Transformation**
  - Converted `IsHoliday` to integer (0/1)

---

## 🤖 Model Training & Evaluation

### Data Splitting

- Chronological split (80/20)
- Ensures validation on future data (real-world scenario)

---

## 📊 Model Performance

| Model              | MAE     | RMSE     | R²     |
|-------------------|---------|----------|--------|
| Random Forest     | 1813.39 | 3764.04  | 0.9706 |
| XGBoost           | 3459.77 | 5676.10  | 0.9332 |
| Linear Regression | 14542.03| 20898.35 | 0.0950 |

**Insight:**  
Random Forest performs the best, capturing ~97% of the variance.

---

## ⚙️ Feature Importance & Optimization

Top important features identified using permutation importance:

- Dept
- Size
- Store
- CPI
- Week
- Unemployment
- Type

The model was retrained using only these features.

**Final Performance:**
- R² Score: **0.9711**

---

## 🚀 Deployment Artifacts

Saved in `models/` for production use:

- `best_model_top.pkl` → Trained model  
- `encoder_top.pkl` → One-hot encoder  
- `model_top_features.pkl` → Processed features  
- `raw_top_features.pkl` → Input features  

---

## 🧠 Tech Stack

- Python  
- Pandas, NumPy  
- Scikit-learn  
- XGBoost  
- Jupyter Notebook  

---

## 📌 Future Improvements

- Hyperparameter tuning (GridSearch, Optuna)
- Time-series models (ARIMA, Prophet)
- Streamlit / FastAPI deployment
- Real-time prediction pipeline

---

## ⭐ Summary

A complete ML pipeline for sales forecasting with strong performance using Random Forest and feature optimization.