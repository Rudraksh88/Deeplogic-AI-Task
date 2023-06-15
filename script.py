import cv2
import csv
from pdf2image import convert_from_path
import numpy as np
from pytesseract import image_to_string
from pprint import pprint

def extract_key_value_pairs(image):
    # Apply OCR to extract text from the image
    result = image_to_string(image)

    key_value_pairs = {}
    list_of_lines = result.split('\n')
    for line in list_of_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # if value is not empty, add to dictionary
            if value:
                key_value_pairs[key] = value

    # # Debug print for key-value pairs
    # pprint(key_value_pairs)

    return key_value_pairs

def ocr_and_save(image, output_csv):
    # Extract key-value pairs from the image
    key_value_pairs = {}
    key_value_pairs = extract_key_value_pairs(image)

    # Save the key-value pairs and tabular data to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the key-value pairs
        writer.writerow(['Key', 'Value'])
        for key, value in key_value_pairs.items():
            writer.writerow([key, value])

        return output_csv

def process_files(file_name):
    # List of output CSV files
    output_files = []
    if file_name.endswith('.pdf'):
        # Process a PDF document. Convert PDF to PIL images and process each page
        pil_images = convert_from_path(file_name, poppler_path=r'X:\\poppler-23.05.0\\Library\\bin')

        # Convert PIL images to OpenCV images (NumPy arrays)
        opencv_images = [cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in pil_images]

        # # Debug print for number of pages
        # print('PDF Images list length', len(opencv_images))

        for idx, image in enumerate(opencv_images):
            output_files.append(ocr_and_save(image, f'output_{idx}.csv'))

        return output_files

    else:
        # Document is not a PDF
        image = cv2.imread(file_name)
        output_files.append(ocr_and_save(image, 'output.csv'))
        return output_files

if __name__ == '__main__':
    document_path = 'sample1.pdf' # Path to the document
    process_files(document_path)

