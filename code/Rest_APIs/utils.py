import pickle
import pandas as pd
import cv2
import numpy as np
import pytesseract
import re
import xgboost
from Data_user.models import DiabetesData
from rest_framework import serializers
from PIL import Image
import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'Rest_APIs', 'diabetes_xgb.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

def ml_generate_outcome(diabetes_data):
    data_dict = {
        'Pregnancies': [diabetes_data.pregnancies],
        'Glucose': [diabetes_data.glucose],
        'BloodPressure': [diabetes_data.blood_pressure],
        'SkinThickness': [diabetes_data.skin_thickness],
        'Insulin': [diabetes_data.insulin],
        'BMI': [diabetes_data.bmi],
        'DiabetesPedigreeFunction': [diabetes_data.diabetes_pedigree_function],
        'Age': [diabetes_data.age]
    }
    df = pd.DataFrame(data_dict)
    df['Pregnancies'] = pd.to_numeric(df['Pregnancies'], errors='coerce', downcast='integer')
    df['Glucose'] = pd.to_numeric(df['Glucose'], errors='coerce', downcast='integer')
    df['BloodPressure'] = pd.to_numeric(df['BloodPressure'], errors='coerce')
    df['SkinThickness'] = pd.to_numeric(df['SkinThickness'], errors='coerce', downcast='integer')
    df['Insulin'] = pd.to_numeric(df['Insulin'], errors='coerce')
    df['BMI'] = pd.to_numeric(df['BMI'], errors='coerce')
    df['DiabetesPedigreeFunction'] = pd.to_numeric(df['DiabetesPedigreeFunction'], errors='coerce')
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce', downcast='integer')
    df.fillna(0, inplace=True)
    prediction = model.predict(df)
    return prediction[0]

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def extract_patient_details_from_image(image):
    def preprocess_image(image):
        img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return img

    preprocessed_img = preprocess_image(image)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    
    patterns = {
        'patient_id': r'(?:Patient ID|PatientID|Patient Id|ID):?\s*([A-Za-z0-9]+)',
        'pregnancies': r'Pregnancies:\s*([\d.]+)',
        'glucose': r'Glucose:\s*([\d.]+)',
        'blood_pressure': r'(?:Blood Pressure|BloodPressure):\s*([\d.]+)',
        'skin_thickness': r'SkinThickness:\s*([\d.]+)',
        'insulin': r'Insulin:\s*([\d.]+)',
        'bmi': r'BMI:\s*([\d.]+)',
        'diabetes_pedigree_function': r'DiabetesPedigreeFunction:\s*([\d.]+)',
        'age': r'Age:\s*([\d.]+)',
    }

    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1)
            if field in ['pregnancies', 'glucose', 'blood_pressure', 'skin_thickness', 'insulin', 'age']:
                extracted_data[field] = float(value)
            elif field in ['bmi', 'diabetes_pedigree_function']:
                extracted_data[field] = float(value)
            else:
                extracted_data[field] = value
        else:
            extracted_data[field] = None

    if not extracted_data.get('patient_id'):
        raise serializers.ValidationError({"patient_id": "Could not extract patient ID from the image."})
    
    return extracted_data
