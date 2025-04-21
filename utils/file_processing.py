import json
from text_extraction import extract_text_from_pdf, extract_text_from_image
from data_extraction import extract_medical_data

# Main function to process file upload
def process_uploaded_file(file):
    filename = file.name.lower()

    # Extract text from the file (PDF or image)
    if filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif filename.endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file)
    else:
        return "Unsupported file type."

    # Extract structured data using regex
    extracted_data = extract_medical_data(text)
    
    if not extracted_data:
        return "Could not extract key medical data. Please upload a clearer or more detailed file."

    # Save the extracted data into a new file (JSON format for easy handling)
    with open("extracted_data.json", "w") as f:
        json.dump(extracted_data, f, indent=4)

    return extracted_data
