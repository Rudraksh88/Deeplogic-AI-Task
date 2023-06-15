from flask import Flask, render_template, request
import numpy as np
from tempfile import NamedTemporaryFile
from script import process_files
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')

        file = request.files['file']

        # # Debug print for uploaded file name
        # print('Uploaded file:', file.filename)

        # Check if the file has a valid extension
        if file.filename == '':
            return render_template('index.html', error='No file selected')

        if file and allowed_file(file.filename):
            # Save the uploaded file temporarily
            filename = f'input.{file.filename.rsplit(".", 1)[1].lower()}'
            temp_file = NamedTemporaryFile(delete=False, suffix=filename)
            file.save(temp_file.name)

            # # Debug print for temp file name
            # print('Temp file:', temp_file.name)

            # Run the script on the uploaded file.
            # This will generate a list of CSV files in the app directory
            # Add those filenames to a list
            output_csv = process_files(temp_file.name)

            # # Debug print for output file names
            # print('Output CSV list:', output_csv)

            # Create a dictionary of CSV files and their key-value pairs
            csv_dict = {}
            for output_file in output_csv:
                kv_pairs = {} # key-value pairs for the current CSV file
                with open(output_file, 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    next(csvreader, None) # skip the headers
                    for row in csvreader:
                        key   = row[0] # key is the first column
                        value = row[1] # value is the second column

                        kv_pairs[key] = value # add the key-value pair to the dictionary

                # Add the dictionary to the CSV dictionary
                csv_dict[output_file] = kv_pairs

            # Return the display template with the CSV dictionary
            return render_template('display.html', csv_dict=csv_dict)

    return render_template('index.html', error='')

def allowed_file(filename):
    # Check if the file has a valid extension (PDF or image)
    allowed_extensions = {'pdf', 'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

if __name__ == '__main__':
    app.run(debug=True)
