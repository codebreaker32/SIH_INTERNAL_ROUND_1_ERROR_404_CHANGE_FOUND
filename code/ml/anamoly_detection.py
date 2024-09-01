import pickle
import pandas as pd

with open('diabetes_xgb.pkl', 'rb') as file:
    model = pickle.load(file)

data = pd.read_csv("patient_details.csv")
data.drop(columns=['Patient ID'], inplace=True)

new_data = data.iloc[-1, :].values.reshape(1, -1)

predictions = model.predict(new_data)
probabilities = model.predict_proba(new_data)

proba_diabetic = probabilities[0][1]

if 0.8 <= proba_diabetic < 0.9:
    anomaly_status = "ALERT! Extreme chances of being diabetic."
elif proba_diabetic >= 0.9:
    anomaly_status = "Very high chances of being diabetic."
else:
    anomaly_status = "Moderate or low chances of being diabetic."

print(f"Predicted probability of being diabetic: {proba_diabetic:.2f}")
print(f"Anomaly detection status: {anomaly_status}")
