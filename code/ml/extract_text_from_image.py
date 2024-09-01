import cv2
import numpy as np
import pytesseract
from PIL import Image
import pandas as pd
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img

def extract_patient_details(image_path):
    preprocessed_img = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(preprocessed_img, config=custom_config)
    
    patterns = {
        'Patient ID': r'Patient ID:\s*([A-Z0-9]+)',
        'Pregnancies': r'Pregnancies:\s*([\d.]+)',
        'Glucose': r'Glucose:\s*([\d.]+)',
        'BloodPressure': r'BloodPressure:\s*([\d.]+)',
        'SkinThickness': r'SkinThickness:\s*([\d.]+)',
        'Insulin': r'Insulin:\s*([\d.]+)',
        'BMI': r'BMI:\s*([\d.]+)',
        'DiabetesPedigreeFunction': r'DiabetesPedigreeFunction:\s*([\d.]+)',
        'Age': r'Age:\s*([\d.]+)',
    }
    
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text)
        extracted_data[field] = match.group(1) if match else None
    
    return extracted_data

image_path = "H:\projects\internal hack\images\Outcome_1\patient_details_row_23.png"
patient_details = extract_patient_details(image_path)

df = pd.DataFrame([patient_details])
csv_file_path = 'patient_details.csv'
df.to_csv(csv_file_path, index=False)

print(f"Patient details extracted and saved to {csv_file_path}")
