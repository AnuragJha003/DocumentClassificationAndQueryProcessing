import os
import tempfile
import fitz  # PyMuPDF
from flask import Flask, render_template, request, jsonify
import regex as re

app = Flask(__name__)

# Define the folder where uploaded files will be temporarily stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the UPLOAD_FOLDER exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_entities(text):
    # Define regex patterns for date, issuing organization, and name
    date_patterns = [
        r'\b\d{1,4}([./-])\d{1,2}\1\d{1,4}\b',  # MM/DD/YYYY or DD/MM/YYYY or YYYY/MM/DD
        r'\b\d{4}[./-]\d{1,2}[./-]\d{1,4}\b',  # YYYY/MM/DD or YYYY-MM-DD
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}\b',  # Month DD, YYYY
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',  # DD Month YYYY
        r'\b\d{4}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\b',  # YYYY Month DD
    ]

    org_patterns = [
        r'(?i)\b(?:organization|org|issued by|issued|issuer|institute|company|dept|department|firm)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:office|body|group|team|agency|association|corporation|bureau|division)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:university|college|school|hospital|clinic|center)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:firm|enterprise|group|agency|association|corporation|society|union|bureau)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:company|business|division|department|service|institution)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:lab|laboratory|firm|enterprise|agency|association|corporation)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:group|team|association|corporation|society|union|bureau)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:department|office|body|agency|association|corporation|division)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:institute|company|office|group|team|agency|corporation|union|division)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:center|company|department|institution|office|group|team|agency)\s*:\s*(.*?)(?:\n|\r|$)',
    ]

    name_patterns = [
        r'(?i)\b(?:name|patient name|issued to|recipient|resident|customer|client|individual|person)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:full name|given name|first name|last name|middle name|surname)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:personnel|employee|member|participant|subject|account holder)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:title|designation|position)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:contact|contact person|contact name)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:customer|client|account holder|guest)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:applicant|applicant name|participant|attendee)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:owner|owner name|holder|possessor)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:person|person name|individual|subject)\s*:\s*(.*?)(?:\n|\r|$)',
        r'(?i)\b(?:party|party name|member|delegate)\s*:\s*(.*?)(?:\n|\r|$)',
    ]

    # Combine patterns into a single pattern for each entity
    date_pattern = '|'.join(date_patterns)
    org_pattern = '|'.join(org_patterns)
    name_pattern = '|'.join(name_patterns)

    # Search for patterns in the text
    date_match = re.search(date_pattern, text)
    org_match = re.search(org_pattern, text)
    name_match = re.search(name_pattern, text)

    # Initialize variables to None
    date = None
    organization = None
    name = None

    # Extract and return matched entities if not None
    if date_match:
        date = date_match.group(0)

    if org_match:
        organization = org_match.group(1).strip() if org_match.group(1) else None

    if name_match:
        name = name_match.group(1).strip() if name_match.group(1) else None

    return {
        'date': date,
        'organization': organization,
        'name': name
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_query', methods=['POST'])
def process_query():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        try:
            # Save the uploaded file to the UPLOAD_FOLDER
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Load the document using PyMuPDF
            doc = fitz.open(filename)
            doc_text = ""
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                doc_text += page.get_text()

            # Extract date, organization, and name
            extracted_entities = extract_entities(doc_text)

            # Close the document to release the file
            doc.close()

            # Clean up the uploaded file
            os.remove(filename)

            # Check if organization and name are not None before stripping
            if extracted_entities['organization'] is not None:
                extracted_entities['organization'] = extracted_entities['organization'].strip()
            if extracted_entities['name'] is not None:
                extracted_entities['name'] = extracted_entities['name'].strip()

            # Return a JSON response with extracted entities
            return jsonify({'entities': extracted_entities})

        except Exception as e:
            return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

