**CLINICAL PRESCRIPTION INFORMATION EXTRACTION: INTEGRATING PADDLE OCR AND NER FOR PATIENT AND MEDICATION DETAILS RECOGNITION**

**IMPLEMENTATION OF OCR**
"""

!pip install paddlepaddle
!pip install paddlepaddle-gpu
!pip install paddleocr
import paddleocr
!git clone
from paddleocr import PaddleOCR, draw_ocr # main OCR dependencies
import cv2 #opencv
import os # folder directory navigation

ocr_model = PaddleOCR(lang='en')
img_path ='/content/img1.jpg'

# Perform OCR on the image
result = ocr_model.ocr(img_path)

# Print the entire OCR result
for line in result:
    print(' '.join([word_info[1][0] for word_info in line]))
    import os

# Define the output directory
output_dir = '/content/Untitled Folder'

# Check if the output directory exists, if not create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define the path for the output text file
output_text_file = os.path.join(output_dir, 'ocr_output.txt')

# Extract text from OCR result
ocr_text = ""
for line in result:
    ocr_text += ' '.join([word_info[1][0] for word_info in line]) + '\n'

# Write the extracted text into a text file
with open(output_text_file, 'w') as f:
    f.write(ocr_text)

print("OCR output has been written to:", output_text_file)

"""**MODEL TRAINING FOR IDENTIFYING MEDICINE NAME**"""

import pandas as pd
import spacy
from spacy.training import Example
import random

# Load spaCy model for medicine names
nlp_medicine = spacy.blank("en")

# Define the NER pipeline component for medicine names
ner_medicine = nlp_medicine.add_pipe("ner")
ner_medicine.add_label("MEDICINE_NAME")

# Read data from CSV file for medicine names
df_medicine = pd.read_csv("/content/generic.csv.csv")

# Convert data into spaCy training format for medicine names
train_examples_medicine = []
for _, row in df_medicine.iterrows():
    # Use brand name as the medicine name
    text = row["generic name"]
    # Add label for the entire text
    annotations = {"entities": [(0, len(text), "MEDICINE_NAME")]}
    example = Example.from_dict(nlp_medicine.make_doc(text), annotations)
    train_examples_medicine.append(example)

# Training loop for medicine names
other_pipes_medicine = [pipe for pipe in nlp_medicine.pipe_names if pipe != "ner"]
with nlp_medicine.disable_pipes(*other_pipes_medicine):
    optimizer_medicine = nlp_medicine.begin_training()
    for iteration in range(50):
        losses_medicine = {}
        random.shuffle(train_examples_medicine)
        for example in train_examples_medicine:
            nlp_medicine.update([example], drop=0.5, losses=losses_medicine)
        print("Medicine Names - Iteration", iteration, "Losses", losses_medicine)

# Save the trained model for medicine names
nlp_medicine.to_disk("ner_model_medicine")

"""**EXTRACTING MEDICINE NAME AND PATIENT NAME**"""

import os
import re

def extract_medicine_and_patient_names(text):
    # Initialize an empty list to store medicine names
    medicine_names = []

    # Search for medicine names using regex
    for match in re.finditer(r'R\s+([A-Za-z0-9]+)\s*-\s*\d+(\w+)', text):
        medicine_names.append(match.group(1))

    # Extract patient name using regex
    patient_name_match = re.search(r'Patient name:\s*([A-Za-z ]+) ', text)
    patient_name = patient_name_match.group(1) if patient_name_match else ""

    return medicine_names, patient_name
text = "Medical prescription by Klippa Medical Center Lubeckweg 2, 9723HE Groningen, The Netherlands. Patient name: Mario Carlos van der Vaart Patient age: 38 Date: 20-01-2025 R Paracetamol - 50mg R Ibuprofen - 150ml Signed by: Or. Bill Andrew Balmer"

# Extract medicine names and patient name
medicine_names, patient_name = extract_medicine_and_patient_names(text)

# Remove units from medicine names
medicine_names = [name.rstrip("0123456789") for name in medicine_names]

# Print the extracted names
print("Medicine Names:", medicine_names)
print("Patient Name:", patient_name)

# Specify the directories where you want to save the files
medicine_dir = "/var/medicine"
patient_dir = "/var/patient"

# Ensure directories exist, create if not
os.makedirs(medicine_dir, exist_ok=True)
os.makedirs(patient_dir, exist_ok=True)

# Write the extracted medicine names to a text file
medicine_output_filename = "medicine_names.txt"
medicine_output_path = os.path.join(medicine_dir, medicine_output_filename)
with open(medicine_output_path, "w") as file:
    file.write("\n".join(medicine_names))

print(f"Medicine names have been written to '{medicine_output_path}'.")

# Write the extracted patient name to a text file
patient_output_filename = "patient_name.txt"
patient_output_path = os.path.join(patient_dir, patient_output_filename)
with open(patient_output_path, "w") as file:
    file.write(patient_name)

print(f"Patient name has been written to '{patient_output_path}'.")

"""CLASSIFY AS **GENERIC** OR **BRAND** AND
PROVIDE **DESCRIPTION**
"""

import csv
import requests

def find_brand_name(generic_name, csv_file="/content/dataset.csv"):
    try:
        with open(csv_file, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            for row in reader:
                if generic_name.lower() == row[1].lower():  # Case-insensitive matching
                    return f"The generic name for the brand {row[0]} is {generic_name}."
            return "Brand name not found."

    except FileNotFoundError:
        return f"Error: CSV file '{csv_file}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def extract_medicine_names_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            medicine_names = [line.strip() for line in file.readlines()]
        return medicine_names
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def get_medicine_description(medicine_name):
    try:
        # Query Wikipedia API for medicine description
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{medicine_name}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract the description
        description = data.get("extract", "Description not available.")

        return description

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    file_path = input("Enter the path to the text file containing medicine names: ")

    try:
        medicine_names = extract_medicine_names_from_file(file_path)

        for medicine_name in medicine_names:
            brand_name = find_brand_name(medicine_name.strip())
            if brand_name != "Brand name not found.":
                print(brand_name)
            description = get_medicine_description(medicine_name.strip())
            print(f"Description for {medicine_name}: {description}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

!pip uninstall paddleocr
!pip install paddleocr

"""**COMPARING PRESCRIPTION**"""

import os
import re
from paddleocr import PaddleOCR

# Initialize OCR model
try:
    ocr_model = PaddleOCR(lang='en')
except Exception as e:
    print("Error in initializing OCR model:", e)


def extract_text_and_names(image_path):
    # Perform OCR on the image
    result = ocr_model.ocr(image_path)

    # Extracted text from OCR result
    ocr_text = ""
    for line in result:
        ocr_text += ' '.join([word_info[1][0] for word_info in line]) + '\n'

    print("OCR Text:")
    print(ocr_text)

    # Extract medicine names and patient name
    medicine_names = []
    patient_name = ""

    # Search for medicine names using regex
    for match in re.finditer(r'R\s+([A-Za-z0-9\s]+)\s*-\s*\d+(\w+)', ocr_text):
        medicine_names.append(match.group(1))

    # Extract patient name using regex
    patient_name_match = re.search(r'Patient name:\s*([A-Za-z ]+) ', ocr_text)
    if patient_name_match:
        patient_name = patient_name_match.group(1)

    # Remove extra spaces and units from medicine names
    medicine_names = [name.strip().rstrip("0123456789") for name in medicine_names]

    return medicine_names, patient_name


def process_images(image_paths):
    for index, image_path in enumerate(image_paths):
        # Extract text and names from the image
        medicine_names, patient_name = extract_text_and_names(image_path)

        # Specify the directories where you want to save the files
        output_dir = f"/var/output_image_{index+1}"
        os.makedirs(output_dir, exist_ok=True)

        # Write the extracted medicine names to a text file
        medicine_output_filename = "medicine_names.txt"
        medicine_output_path = os.path.join(output_dir, medicine_output_filename)
        with open(medicine_output_path, "w") as file:
            file.write("\n".join(medicine_names))

        print(f"Medicine names from image {index+1} have been written to '{medicine_output_path}'.")

        # Write the extracted patient name to a text file
        patient_output_filename = "patient_name.txt"
        patient_output_path = os.path.join(output_dir, patient_output_filename)
        with open(patient_output_path, "w") as file:
            file.write(patient_name)

        print(f"Patient name from image {index+1} has been written to '{patient_output_path}'.")

# Example image paths
image_paths = ['/content/img1.jpg', '/content/img3.jpg']

# Process the images
process_images(image_paths)

"""**EXTRACTING MEDICINE NAME AND PATIENT NAME**"""

import os
import re

def extract_medicine_and_patient_names(text):
    # Initialize an empty list to store medicine names
    medicine_names = []

    # Search for medicine names using regex
    for match in re.finditer(r'(\b[A-Za-z0-9]+\b)\s*-\s*\d+(\w+)', text):
        medicine_names.append(match.group(1))

    # Extract patient name using regex
    patient_name_match = re.search(r'Patient name:\s*([A-Za-z ]+) ', text)
    patient_name = patient_name_match.group(1) if patient_name_match else ""

    return medicine_names, patient_name


def process_texts(text1, text2):
    # Extract medicine names and patient names from the first text
    medicine_names_1, patient_name_1 = extract_medicine_and_patient_names(text1)
    # Extract medicine names and patient names from the second text
    medicine_names_2, patient_name_2 = extract_medicine_and_patient_names(text2)

    # Remove units from medicine names
    medicine_names_1 = [name.rstrip("0123456789") for name in medicine_names_1]
    medicine_names_2 = [name.rstrip("0123456789") for name in medicine_names_2]

    # Specify the directories where you want to save the files
    medicine_dir = "/var/medicine"
    patient_dir = "/var/patient"

    # Ensure directories exist, create if not
    os.makedirs(medicine_dir, exist_ok=True)
    os.makedirs(patient_dir, exist_ok=True)

    # Write the extracted medicine names from text 1 to a text file
    medicine_output_filename_1 = "medicine_names_1.txt"
    medicine_output_path_1 = os.path.join(medicine_dir, medicine_output_filename_1)
    with open(medicine_output_path_1, "w") as file:
        file.write("\n".join(medicine_names_1))

    print(f"Medicine names from text 1 have been written to '{medicine_output_path_1}'.")

    # Write the extracted patient name from text 1 to a text file
    patient_output_filename_1 = "patient_name_1.txt"
    patient_output_path_1 = os.path.join(patient_dir, patient_output_filename_1)
    with open(patient_output_path_1, "w") as file:
        file.write(patient_name_1)

    print(f"Patient name from text 1 has been written to '{patient_output_path_1}'.")

    # Write the extracted medicine names from text 2 to a text file
    medicine_output_filename_2 = "medicine_names_2.txt"
    medicine_output_path_2 = os.path.join(medicine_dir, medicine_output_filename_2)
    with open(medicine_output_path_2, "w") as file:
        file.write("\n".join(medicine_names_2))

    print(f"Medicine names from text 2 have been written to '{medicine_output_path_2}'.")

    # Write the extracted patient name from text 2 to a text file
    patient_output_filename_2 = "patient_name_2.txt"
    patient_output_path_2 = os.path.join(patient_dir, patient_output_filename_2)
    with open(patient_output_path_2, "w") as file:
        file.write(patient_name_2)

    print(f"Patient name from text 2 has been written to '{patient_output_path_2}'.")

# Example texts
text1 = "Medical prescription by Klippa Medical Center Lubeckweg 2, 9723HE Groningen, The Netherlands. Patient name: Mario Carlos van der Vaart Patient age: 38 Date: 20-01-2025 R Paracetamol - 50mg R Ibuprofen - 150ml Signed by: Or. Bill Andrew Balmer"
text2 = "Medical Prescription by KG Medical Centre NGGO Colony Coimbatore. Patient name: Mario Carlos van der Vaart Patient age:38 Date: 30-01-2025 R AlKaparol - 50mg R thorazine - l50mg Signed by Dr.VinKarsel"


# Process the texts
process_texts(text1, text2)

"""**IDENTIFICATION OF DUPLICATE MEDICATION**"""

import csv

data1 = "/content/dataset.csv"
with open(data1, "r", encoding="latin-1") as file:
    reader = csv.reader(file)
    next(reader)
    text1 = input("Enter generic or brand name 1: ")
    text2 = input("Enter generic or brand name 2: ")
    found = False  # Initialize a flag to track if the match is found
    for row in reader:
        if (text1.lower() == row[0].lower() and text2.lower() == row[1].lower()) or \
           (text2.lower() == row[0].lower() and text1.lower() == row[1].lower()):
            found = True
            break  # Exit the loop once the match is found
    if found:
        print(f"Proceed: One is the generic name and the other is the brand name")
    else:
        print("Don't proceed: Entered names are not matching as generic and brand names")

"""**ACCURACY FOR MEDICINE NAMES**"""

import csv
import requests
import pandas as pd

# Function to find the brand name for a given generic name
def find_brand_name(generic_name, csv_file="/content/dataset.csv"):
    try:
        with open(csv_file, 'r', encoding='latin-1') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            for row in reader:
                if generic_name.lower() == row[1].lower():  # Case-insensitive matching
                    return f"The generic name for the brand {row[0]} is {generic_name}."
            return "Brand name not found."

    except FileNotFoundError:
        return f"Error: CSV file '{csv_file}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to extract medicine names from a text file
def extract_medicine_names_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            medicine_names = [line.strip() for line in file.readlines()]
        return medicine_names
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Function to get the description for a given medicine name
def get_medicine_description(medicine_name):
    try:
        # Query Wikipedia API for medicine description
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{medicine_name}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Extract the description
        description = data.get("extract", "Description not available.")

        return description

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Main function
if __name__ == "__main__":
    file_path = input("Enter the path to the text file containing medicine names: ")

    try:
        medicine_names = extract_medicine_names_from_file(file_path)

        accuracy_brand_name = 0
        accuracy_description = 0
        total_medicines = len(medicine_names)

        for medicine_name in medicine_names:
            brand_name = find_brand_name(medicine_name.strip())
            if brand_name != "Brand name not found.":
                accuracy_brand_name += 1

            description = get_medicine_description(medicine_name.strip())
            if description != "Description not available.":
                accuracy_description += 1

        accuracy_brand_name_percent = (accuracy_brand_name / total_medicines) * 100
        accuracy_description_percent = (accuracy_description / total_medicines) * 100

        print(f"Accuracy for brand names: {accuracy_brand_name_percent:.2f}%")
        print(f"Accuracy for descriptions: {accuracy_description_percent:.2f}%")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

"""**ACCURACY METRICS FOR SPACY-NER MODEL**"""

import pandas as pd
import spacy
import random
from spacy.training import Example
import matplotlib.pyplot as plt

# Initialize a blank spaCy model
nlp_medicine = spacy.blank("en")

# Add the NER pipeline component
ner_medicine = nlp_medicine.add_pipe("ner")

# Add the label to the NER component
ner_medicine.add_label("MEDICINE_NAME")

# Load the training dataset
df_train = pd.read_csv("/content/generic.csv.csv")  # Replace "/path/to/training_dataset.csv" with the path to your training dataset CSV file

# Prepare training examples in spaCy format
train_examples = []
for _, row in df_train.iterrows():
    text = row["generic name"]  # Assuming "generic name" is the text data column
    entities = [(0, len(text), row["drug class"])]  # Assuming "drug class" is the entity label column
    example = Example.from_dict(nlp_medicine.make_doc(text), {"entities": entities})
    train_examples.append(example)

# Training loop for the model
other_pipes_medicine = [pipe for pipe in nlp_medicine.pipe_names if pipe != "ner"]
with nlp_medicine.disable_pipes(*other_pipes_medicine):
    optimizer = nlp_medicine.begin_training()
    losses_history = []  # to store loss values for visualization
    for iteration in range(50):
        random.shuffle(train_examples)
        losses = {}
        for example in train_examples:
            nlp_medicine.update([example], drop=0.5, losses=losses)
        losses_history.append(losses['ner'])
        print("Iteration", iteration, "Losses", losses)

# Load the test dataset with annotated examples
df_test = pd.read_csv("/content/generic.csv.csv")  # Replace "/path/to/test_dataset.csv" with the path to your test dataset CSV file

# Prepare test examples in spaCy format
test_examples = []
for _, row in df_test.iterrows():
    text = row["generic name"]  # Assuming "generic name" is the text data column
    entities = [(0, len(text), row["drug class"])]  # Assuming "drug class" is the entity label column
    example = Example.from_dict(nlp_medicine.make_doc(text), {"entities": entities})
    test_examples.append(example)

# Evaluate the model on the test dataset
scores = nlp_medicine.evaluate(test_examples)

# Print accuracy metrics
print("Accuracy Metrics:")
print("Precision:", scores["ents_p"])
print("Recall:", scores["ents_r"])
print("F1-score:", scores["ents_f"])

# Visualize loss history
plt.plot(range(len(losses_history)), losses_history)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

# Create a DataFrame for accuracy metrics
metrics_df = pd.DataFrame({
    'Metric': ['Precision', 'Recall', 'F1-score'],
    'Score': [scores["ents_p"], scores["ents_r"], scores["ents_f"]]
})

# Display accuracy metrics
print("\nAccuracy Metrics:")
print(metrics_df)

"""**ACCURACY FOR SPACY EN_CORE_WEB_SM**"""

import pandas as pd
import spacy
import random
import matplotlib.pyplot as plt
from spacy.training.example import Example

# Load the pre-trained spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the training dataset
df_train = pd.read_csv("/content/generic.csv.csv")  # Replace with your path

# Training data in spaCy format
train_data = []
for _, row in df_train.iterrows():
    text = row["generic name"]
    entities = [(0, len(text), row["drug class"])]
    train_data.append((text, {"entities": entities}))

# Define and train the NER model
ner = nlp.get_pipe("ner")

# Adding custom label
ner.add_label("MEDICINE_NAME")

# Training loop
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    losses_history = []
    for epoch in range(50):
        random.shuffle(train_data)
        examples = []
        for text, annotations in train_data:
            examples.append(Example.from_dict(nlp.make_doc(text), annotations))
        losses = {}
        nlp.update(examples, drop=0.5, losses=losses)
        losses_history.append(losses['ner'])

# Load the test dataset
df_test = pd.read_csv("/content/generic.csv.csv")  # Replace with your path

# Test data in spaCy format
test_examples = []
for _, row in df_test.iterrows():
    text = row["generic name"]
    entities = [(0, len(text), row["drug class"])]
    test_examples.append(Example.from_dict(nlp.make_doc(text), {"entities": entities}))

# Evaluate the model
scores = nlp.evaluate(test_examples)

# Print accuracy metrics
print("Accuracy Metrics:")
print("Precision:", scores["ents_p"])
print("Recall:", scores["ents_r"])
print("F1-score:", scores["ents_f"])

# Visualize loss history
plt.plot(range(len(losses_history)), losses_history)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

# Create a DataFrame for accuracy metrics
metrics_df = pd.DataFrame({
    'Metric': ['Precision', 'Recall', 'F1-score'],
    'Score': [scores["ents_p"], scores["ents_r"], scores["ents_f"]]
})

# Display accuracy metrics
print("\nAccuracy Metrics:")
print(metrics_df)
