import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Get the patient ID as input
patient_id = input("Enter the patient id: ")

# Load the CSV file into a DataFrame
df = pd.read_csv('diabetes_outcome.csv')

# Filter the DataFrame to get the row with the specified Patient Id
filtered_row = df[df['Patient_Id'] == patient_id]

# Check if the Patient Id exists in the DataFrame
if not filtered_row.empty:
    # Extract the data to plot (columns 0 to 6)
    data_to_plot = filtered_row.iloc[0, 0:7]
    
    # Set the background color to purple
    plt.figure(figsize=(10, 6), facecolor='purple')

    # Plotting the data with a light color for the bars
    sns.barplot(x=data_to_plot.index, y=data_to_plot.values, color='green')

    # Set the title using columns 7 and 8
    plt.title(f"Name : {filtered_row.iloc[0, 9]}  Age: {filtered_row.iloc[0, 7]}", color='black',fontweight='bold')

    # Adjusting the plot's labels and title color to stand out against the purple background
    plt.xlabel("", color='black')
    plt.ylabel("", color='black')
    plt.xticks(color='white', rotation=45, ha="right")  # Rotate x labels to fit and align to the right
    plt.yticks(color='white')

    
    plt.tight_layout()

   
    plt.show()
else:
    # Print an appropriate message if the Patient Id is not found
    print(f"Patient Id: {patient_id} not found in the dataset.")
