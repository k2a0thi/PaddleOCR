\# Medical Prescription Analysis with OCR and NER

This project is designed to extract information from medical
prescription images using Optical Character Recognition (OCR) and Named
Entity Recognition (NER). It aims to extract patient names and medicine
names from prescription images, and perform additional analysis such as
finding generic and brand names of medicines, and providing descriptions
of medicines using external APIs.

\## Table of Contents - \[Features\](#features) -
\[Requirements\](#requirements) - \[Setup
Instructions\](#setup-instructions) - \[Usage\](#usage) - \[Code
Overview\](#code-overview) - \[Troubleshooting\](#troubleshooting) -
\[Contributing\](#contributing)

\## Features - \*\*OCR with PaddleOCR:\*\* Extracts text from medical
prescription images. - \*\*NER with spaCy:\*\* Identifies medicine names
and patient names in the extracted text. - \*\*Data Extraction:\*\*
Extracts medicine and patient names using regular expressions. -
\*\*Data Storage:\*\* Saves extracted data into text files. - \*\*API
Integration:\*\* Fetches medicine descriptions from Wikipedia using its
API. - \*\*Validation:\*\* Checks if given names are generic or brand
names using a CSV dataset. - \*\*Accuracy Reporting:\*\* Reports the
accuracy of extracting brand names and descriptions.

\## Requirements - Python 3.7 or higher - Required Python libraries:  -
\`paddlepaddle\`  - \`paddleocr\`  - \`opencv-python\`  - \`pandas\`  -
\`spacy\`  - \`requests\`  - \`matplotlib\`

\## Setup Instructions

1\. \*\*Clone the Repository:\*\*

\`\`\`bash git clone \[repository-url\] cd \[repository-folder\] \`\`\`

2\. \*\*Install Required Libraries:\*\*

Install PaddlePaddle: \`\`\`bash pip install paddlepaddle pip install
paddlepaddle-gpu \# Only if using a GPU \`\`\`

Install PaddleOCR: \`\`\`bash pip install paddleocr \`\`\`

Install other required libraries: \`\`\`bash pip install opencv-python
pandas spacy requests matplotlib \`\`\`

3\. \*\*Setup spaCy Models:\*\*

Download necessary spaCy models: \`\`\`bash python -m spacy download
en_core_web_sm \`\`\`

4\. \*\*Prepare Data:\*\*

 - Ensure you have the CSV files (\`generic.csv.csv\`, \`dataset.csv\`)
available in the specified paths or update the paths in the code
accordingly.  - Have the images (\`img1.jpg\`, \`img3.jpg\`, etc.)
available in the \`/content\` directory or update paths accordingly.

\## Usage

1\. \*\*OCR and NER Processing:\*\*  - Place your prescription images in
the specified directory.  - Run the OCR extraction: \`\`\`python
img_path = \'/content/img1.jpg\' \# Change to your image path result =
ocr_model.ocr(img_path) \`\`\`  - Run NER extraction: \`\`\`python text
= \"Your extracted text here\" medicine_names, patient_name =
extract_medicine_and_patient_names(text) \`\`\`

2\. \*\*Extract Medicine and Patient Names from Text:\*\*  - Update
\`text1\` and \`text2\` with actual prescription text.  - Run the
\`process_texts\` function to extract and save data.

3\. \*\*Fetching Medicine Descriptions:\*\*  - Provide a text file with
medicine names.  - Run the provided script to fetch descriptions from
Wikipedia.

4\. \*\*Validation of Medicine Names:\*\*  - Input names to check
against the \`dataset.csv\` to verify if they are generic or brand
names.

\## Code Overview

\- \*\*OCR Model Initialization:\*\* Uses PaddleOCR to extract text from
images. - \*\*NER Training and Extraction:\*\* Trains a spaCy model to
recognize medicine names and extracts patient names using regex. -
\*\*Text Processing:\*\* Parses text to find medicine and patient names,
and writes them to text files. - \*\*API Interaction:\*\* Fetches
medicine descriptions using the Wikipedia API. - \*\*Data
Validation:\*\* Compares provided names against a CSV dataset to
identify relationships between generic and brand names. - \*\*Accuracy
Calculation:\*\* Measures the accuracy of name extraction and
description fetching.

\## Troubleshooting

\- Ensure all paths are correct and files exist in the specified
directories. - Make sure that the correct versions of dependencies are
installed. - If PaddleOCR installation fails, check the official
\[PaddleOCR documentation\](https://github.com/PaddlePaddle/PaddleOCR)
for installation help.

\## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or
open an Issue to improve the project.
