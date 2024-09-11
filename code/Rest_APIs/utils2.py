import pickle
import google.generativeai as genai
from google.generativeai.types import SafetySettingDict
import os

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'Rest_APIs', 'diabetes_xgb.pkl')
with open(file_path, 'rb') as file:
    model = pickle.load(file)

genai.configure(api_key="")

safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
]

def generate_recommendation(validated_data):
    input_data = [
        validated_data['pregnancies'],
        validated_data['glucose'],
        validated_data['blood_pressure'],
        validated_data['skin_thickness'],
        validated_data['insulin'],
        validated_data['bmi'],
        validated_data['diabetes_pedigree_function'],
        validated_data['age']
    ]
    input_data_reshaped = [input_data]
    outcome_prediction = model.predict(input_data_reshaped)
    probabilities = model.predict_proba(input_data_reshaped)
    proba_diabetic = probabilities[0][1]

    if 0.8 <= proba_diabetic < 0.9:
        anomaly_status = "ALERT! Extreme chances of being diabetic."
    elif proba_diabetic >= 0.9:
        anomaly_status = "Very high chances of being diabetic."
    else:
        anomaly_status = "Moderate or low chances of being diabetic."

    diabetic_prompt_template = """You are an AI expert in medical domain. Give advice related to diet (with examples), exercises (with examples), routine etc. after analysing these characteristics:
    Patient Characteristics:
    - BMI: {bmi}
    - Age: {age}
    - Pregnancies: {preg}
    - Glucose: {glu}
    - Blood Pressure: {bp}
    - Skin Thickness: {skin}
    - Insulin: {insulin}
    - Diabetes Pedigree Function: {func}
    Don't use word I, instead use we.
    In the end, give some educational facts in a funny way related to health.
    Personalised Diabetes Management Advice:
    """

    prevention_prompt_template = """You are an AI expert in medical domain. Give advice related to diet (with examples), exercises (with examples), routine etc. after analysing these characteristics:
    Patient Characteristics:
    - BMI: {bmi}
    - Age: {age}
    - Pregnancies: {preg}
    - Glucose: {glu}
    - Blood Pressure: {bp}
    - Skin Thickness: {skin}
    - Insulin: {insulin}
    - Diabetes Pedigree Function: {func}
    Don't mention these factors' values.
    Don't use word I, instead use we.
    In the end, give some educational facts in a funny way related to health and diabetes.
    Personalised Diabetes Prevention Advice:
    """
    
    selected_prompt_template = diabetic_prompt_template if outcome_prediction[0] == 1 else prevention_prompt_template
    formatted_prompt = selected_prompt_template.format(
        bmi=validated_data['bmi'],
        age=validated_data['age'],
        preg=validated_data['pregnancies'],
        glu=validated_data['glucose'],
        bp=validated_data['blood_pressure'],
        skin=validated_data['skin_thickness'],
        insulin=validated_data['insulin'],
        func=validated_data['diabetes_pedigree_function'],
    )

    response = genai.GenerativeModel('gemini-pro').generate_content(
        formatted_prompt,
        safety_settings=safety_settings,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            top_p=1,
            top_k=1,
            max_output_tokens=2048,
        )
    )

    text = beautify_response_text(response.text)
    return text, outcome_prediction[0], anomaly_status, proba_diabetic

def beautify_response_text(text):
    text = text.replace("*  -", ":\n  -")
    text = text.replace("*", "")
    text = text.replace(":\n", ":\n\n")
    text = text.replace("\n\n\n", "\n\n")
    text = text.replace("Diet:", "\nDiet:\n" + "-"*50)
    text = text.replace("Exercises:", "\nExercises:\n" + "-"*50)
    text = text.replace("Routine:", "\nRoutine:\n" + "-"*50)
    text = text.replace("Educational Facts in a Funny Way:", "\nEducational Facts in a Funny Way:\n" + "-"*50)
    
    return text.strip()
