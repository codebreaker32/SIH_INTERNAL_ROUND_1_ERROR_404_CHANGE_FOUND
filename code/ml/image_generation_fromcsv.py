import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import random
import string

csv_file = "diabetes.csv"

df = pd.read_csv(csv_file)

output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

class_dirs = {
    0: "Outcome_0",
    1: "Outcome_1"
}

for class_name in class_dirs.values():
    os.makedirs(os.path.join(output_dir, class_name), exist_ok=True)

def generate_patient_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def create_image_for_row(row_data, row_index):
    img = Image.new('RGB', (800, 400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
        font_bold = font
    
    patient_id = generate_patient_id()
    
    text = f"Patient Details - Row {row_index + 1}\n"
    text += f"Patient ID: {patient_id}\n\n"
    text += "\n".join([f"{col}: {row_data[col]}" for col in df.columns if col != "Outcome"])
    
    title = "Patient Medical Report"
    d.text((10, 10), title, font=font_bold, fill=(0, 0, 0))
    
    d.text((10, 60), text, font=font, fill=(0, 0, 0))
    
    border_color = (0, 0, 0)
    d.rectangle([(5, 5), (795, 395)], outline=border_color, width=5)
    
    outcome_value = row_data['Outcome']
    class_dir = os.path.join(output_dir, class_dirs[outcome_value])
    
    image_filename = os.path.join(class_dir, f"patient_details_row_{row_index + 1}.png")
    img.save(image_filename)
    
    return image_filename

generated_images = []
for index, row in df.iterrows():
    image_file = create_image_for_row(row, index)
    generated_images.append(image_file)

print(generated_images[:5])
