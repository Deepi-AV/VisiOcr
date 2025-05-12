import cv2
import pytesseract
import re
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

unwanted_keywords = ['Government', 'india', 'of', 'INCOME', 'TAX','Permanent','Account','Number']
def extract_name_before_dob(text):
    # Find the DOB first
    dob_match = re.search(r'\d{2}/\d{2}/\d{4}' , text)
    if dob_match:
        # Get text before DOB
        text_before_dob = text[:dob_match.start()].strip()
        
        # Split text by lines and look for the last valid line
        lines = text_before_dob.splitlines()
        for line in reversed(lines):
            line = line.strip()
            # Check if the line starts with a capital letter and has no unwanted keywords
            if line and line[0].isupper() and all(word.lower() not in line.lower() for word in unwanted_keywords):
                # Ensure the line looks like a valid name (only alphabetic and spaces)
                if re.match(r'^[A-Za-z\s]+$', line):
                    return line.strip()
    
    return "Not found"

# Function to extract the name and father's name
def extract_names_from_pan(text):

    permanent_index = text.lower().find("india")
    
    # If the word 'India' is found, clean the text before it
    if permanent_index != -1:
        cleaned_text = text[permanent_index:]  # Get text from 'India' onwards
    else:
        cleaned_text = text

    lines = cleaned_text.splitlines()

    extracted_names = []
    
    # Iterate over each line in the OCR text
    for line in lines:
        line = line.strip()

        # Check if the line contains only capital letters and spaces (valid name-like)
        if line.isupper() and re.match(r'^[A-Z\s]+$', line) and len(line)>4:
            # Exclude lines containing unwanted keywords
            if all(keyword.lower() not in line.lower() for keyword in unwanted_keywords):
                # Add to extracted names
                extracted_names.append(line)

    # the first name is the cardholder's name and the second is the father's name
    name = extracted_names[0] if len(extracted_names) > 0 else "Not found"
    father_name = extracted_names[1] if len(extracted_names) > 1 else "Not found"
    
    return name, father_name


def extract_text(image):

    custom_config=r'--oem 3 --psm 11'
       
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray,config=custom_config,lang='eng')
    extracted_text=extract_details(text)
    return final_text(extracted_text)

def extract_details(text):        
    
    aadhaar_pattern = r'\d{4}\s*\d{4}\s*\d{4}'
    aadhaar_match = re.search(aadhaar_pattern, text)

    pan_pattern = r'[A-Z]{5}\d{4}[A-Z]'
    pan_match = re.search(pan_pattern, text)

    
    if aadhaar_match:
       
        name_match = extract_name_before_dob(text)
        dob_match = re.search(r'\d{2}/\d{2}/\d{4}' , text)
        gender_match = re.search(r'(Male|Female)', text,re.IGNORECASE)

        details = {
            "Type": "Aadhaar",
            "Name": name_match,
            "DOB": dob_match.group() if dob_match else "Not found",
            "Gender": gender_match.group() if gender_match else "Not found"
        }
        return details

    elif pan_match:
       
        name_match,father_name_match =extract_names_from_pan(text)
        dob_match = re.search(r'\d{2}/\d{2}/\d{4}', text)

        details = {
            "Type": "PAN",
            "Name": name_match,
            "Father's Name": father_name_match,
            "DOB": dob_match.group() if dob_match else "Not found"
        }
        return details
    
    return "OCR results are too noisy or neither Aadhaar nor PAN details were detected."

def final_text(extracted_text):
    if isinstance(extracted_text, dict):
        for key, value in extracted_text.items():
            if value == "Not found":
                # Return an error message if any key's value is "Not found"
                return f"The field '{key}' was not found. Please check the image and try again."
        # If all values are valid, proceed
        return extracted_text
    else:
        return extracted_text  # If OCR is too noisy, pass the original message

