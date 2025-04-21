import streamlit as st
import json
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import fitz  # PyMuPDF for extracting text from PDFs
import pytesseract
from PIL import Image
import tempfile

URL = "https://api.aimlapi.com/v1/chat/completions"
KEY = "97d5f10dfba94fb49c10b2a6b615268f"

def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    doc = fitz.open(tmp_file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

# Function to extract text from image (using pytesseract)
def extract_text_from_image(image):
    return pytesseract.image_to_string(image)

# Function to extract age and gender from the report (assuming they are present in the text)
def extract_age_and_gender(report_text):
    age, gender = None, None
    # Basic extraction logic (you can improve this with regex or NLP techniques)
    if "age" in report_text.lower():
        # Extract age from text
        age = [int(s) for s in report_text.split() if s.isdigit()][0]  # Simple extraction; improve with regex
    if "male" in report_text.lower():
        gender = "Male"
    elif "female" in report_text.lower():
        gender = "Female"
    return age, gender

# Function to call the AI API
def call_ai_api(report_data):
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o",  # Specify the model you want to use
        "messages": [
            {"role": "user", "content": f"Analyze the following medical report:\n\nReport: {report_data['report_text']}\n\nAge: {report_data['patient_age']}\nGender: {report_data['patient_gender']}\n\nDo not return the values from the report. Instead, provide:\n1. The **issues** found in the report with reasons.\n2. The **risk level** (low, medium, high) of life-threatening conditions like cardiac or other diseases.\n3. A detailed **diagnosis**.\n4. The **major disease** found in the report, and make sure to return it in **bold and large font**."}
        ]
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200 or response.status_code == 201:
        result = response.json()
        diagnosis = result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')

        if diagnosis:
            return diagnosis
        else:
            return "No detailed analysis provided."
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None

# Function to generate PDF of the diagnosis summary
def generate_pdf(diagnosis_summary):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # Page size

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 50, "Diagnosis Summary")

    c.setFont("Helvetica", 12)
    text = diagnosis_summary.split("\n")
    y_position = height - 80

    for line in text:
        c.drawString(30, y_position, line)
        y_position -= 15

    c.save()
    buffer.seek(0)
    return buffer

# Streamlit app code
def main():
    st.title("Medical Report Analysis")

    # File upload functionality
    uploaded_file = st.file_uploader("Upload a medical report (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Check file type and extract text
        if uploaded_file.type == "application/pdf":
            report_text = extract_text_from_pdf(uploaded_file)
        else:
            img = Image.open(uploaded_file)
            report_text = extract_text_from_image(img)

        st.text_area("Extracted Report Text", report_text, height=200)

        # Extract Age and Gender from the report text
        patient_age, patient_gender = extract_age_and_gender(report_text)
        st.write(f"Extracted Age: {patient_age}")
        st.write(f"Extracted Gender: {patient_gender}")

        # Show loading spinner while calling the API
        with st.spinner('Analyzing the report...'):
            # Call the AI API to get diagnosis and risk
            report_data = {
                "report_text": report_text,
                "patient_age": patient_age,
                "patient_gender": patient_gender
            }
            diagnosis_result = call_ai_api(report_data)

        if diagnosis_result:
            st.success(f"✅ **Diagnosis & Risk Analysis**:\n\n{diagnosis_result}")

            # Example extraction of major disease and risk level
            major_disease = "Iron Deficiency Anemia"  # Example; this will be dynamically extracted
            risk_level = "High"  # Example; this will be extracted dynamically

            # Display Major Disease in Bold and Large Font
            st.markdown(f"### **{major_disease}**", unsafe_allow_html=True)

            # Display Risk Level
            st.markdown(f"#### Risk Level: **{risk_level}**")

            # Display the Risk Bar
            if risk_level.lower() == "high":
                risk_percentage = 80
                risk_color = "red"
            elif risk_level.lower() == "medium":
                risk_percentage = 50
                risk_color = "yellow"
            else:
                risk_percentage = 20
                risk_color = "green"

            st.progress(risk_percentage, text=f"Risk: {risk_level}")
            st.markdown(f"<div style='background-color:{risk_color}; height: 20px; width: 100%;'></div>", unsafe_allow_html=True)

            # Add a button to generate PDF of the diagnosis summary
            if st.button("Generate PDF"):
                # Generate PDF with the diagnosis summary
                pdf_buffer = generate_pdf(diagnosis_result)

                # Create a download link for the PDF
                st.download_button(
                    label="Download Diagnosis PDF",
                    data=pdf_buffer,
                    file_name="diagnosis_summary.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
