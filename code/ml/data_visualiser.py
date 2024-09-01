import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

patient_id = input("Enter the patient id: ")

df = pd.read_csv('diabetes_outcome.csv')

filtered_row = df[df['Patient_Id'] == patient_id]

if not filtered_row.empty:
    data_to_plot = filtered_row.iloc[0, 0:7]
    
   
    plt.figure(figsize=(10, 6), facecolor='purple')

    # Plotting the data with a light color for the bars
    sns.barplot(x=data_to_plot.index, y=data_to_plot.values, color='green')

    # Set the title using columns 7 and 8
    plt.title(f"Name : {filtered_row.iloc[0, 9]}  Age: {filtered_row.iloc[0, 7]}", color='black',fontweight='bold')

  
    plt.xlabel("", color='black')
    plt.ylabel("", color='black')
    plt.xticks(color='white', rotation=45, ha="right")
    plt.yticks(color='white')

    
    plt.tight_layout()

   
    plt.show()
else:
    # Print an appropriate message if the Patient Id is not found
    print(f"Patient Id: {patient_id} not found in the dataset.")
