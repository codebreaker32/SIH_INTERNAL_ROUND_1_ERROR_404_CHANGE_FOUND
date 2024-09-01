import pickle
import pandas as pd
import shap

with open('diabetes_xgb.pkl', 'rb') as file:
    model = pickle.load(file)

data = pd.read_csv("patient_details.csv")
data.drop(columns=['Patient ID'], inplace=True)

new_data = data.iloc[-1, :].values.reshape(1, -1)

predictions = model.predict(new_data)

explainer = shap.TreeExplainer(model)

shap_values = explainer.shap_values(new_data)

shap_explanation = shap_values[0]

explanation_text = []

for feature, shap_value in zip(data.columns, shap_explanation):
    if shap_value > 0:
        explanation_text.append(f"The patient's {feature} increased the likelihood of being diabetic.")
    elif shap_value < 0:
        explanation_text.append(f"The patient's {feature} decreased the likelihood of being diabetic.")
    else:
        explanation_text.append(f"The patient's {feature} had no effect on the likelihood of being diabetic.")

if predictions[0] == 1:
    explanation_text.append("Overall, the model predicts that the patient is diabetic.")
else:
    explanation_text.append("Overall, the model predicts that the patient is healthy.")

for line in explanation_text:
    print(line)
