import pickle
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import SafetySettingDict

with open('diabetes_xgb.pkl', 'rb') as file:
    model = pickle.load(file)

data = pd.read_csv("patient_details.csv")
data.drop(columns=['Patient ID'], inplace=True)

last_row = data.iloc[-1, :].values.reshape(1, -1)

prediction = model.predict(last_row)

genai.configure(api_key=" ")

model = genai.GenerativeModel('gemini-pro')

safety_settings = [
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
    SafetySettingDict(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
]

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

selected_prompt_template = diabetic_prompt_template if prediction[0] == 1 else prevention_prompt_template

row = data.iloc[-1]

formatted_prompt = selected_prompt_template.format(
    bmi=row["BMI"],
    age=row["Age"],
    preg=row["Pregnancies"],
    glu=row["Glucose"],
    bp=row["BloodPressure"],
    skin=row["SkinThickness"],
    insulin=row["Insulin"],
    func=row["DiabetesPedigreeFunction"],
)

response = model.generate_content(
    formatted_prompt,
    safety_settings=safety_settings,
    generation_config=genai.types.GenerationConfig(
        temperature=0.2,
        top_p=1,
        top_k=1,
        max_output_tokens=2048,
    )
)

print(response.text)
