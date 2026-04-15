import os
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def generate_mock_data(n_samples=1000):
    """
    Generate synthetic vitals data.
    Features: HR (Heart Rate), SpO2 (Oxygen Saturation), SBP (Systolic BP)
    Target: 1 (High Risk / Code Blue), 0 (Stable)
    """
    np.random.seed(42)
    
    # Generate stable patients
    hr_stable = np.random.normal(70, 10, int(n_samples * 0.7))
    spo2_stable = np.random.normal(98, 2, int(n_samples * 0.7))
    sbp_stable = np.random.normal(120, 15, int(n_samples * 0.7))
    y_stable = np.zeros(int(n_samples * 0.7))
    
    # Generate crashing patients
    hr_crash = np.random.normal(130, 30, int(n_samples * 0.3))
    spo2_crash = np.random.normal(85, 8, int(n_samples * 0.3))
    sbp_crash = np.random.normal(70, 20, int(n_samples * 0.3))
    y_crash = np.ones(int(n_samples * 0.3))
    
    X = pd.DataFrame({
        'HR': np.concatenate([hr_stable, hr_crash]),
        'SpO2': np.concatenate([spo2_stable, spo2_crash]),
        'SBP': np.concatenate([sbp_stable, sbp_crash])
    })
    
    y = np.concatenate([y_stable, y_crash])
    
    return X, y

def train_and_export():
    print("Generating mock data...")
    X, y = generate_mock_data()
    
    print("Building pipeline...")
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', LogisticRegression(random_state=42))
    ])
    
    print("Training model...")
    pipeline.fit(X, y)
    
    # Ensure data directory exists
    model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(model_dir, exist_ok=True)
    
    # Export model
    model_path = os.path.join(model_dir, 'model.pkl')
    joblib.dump(pipeline, model_path)
    print(f"Model exported successfully to {model_path}")

if __name__ == '__main__':
    train_and_export()
