from datetime import datetime

def validate_pan_name(pan_name):
    # CHECKING CONDITION-> all uppercase and does not exceed 25 characters
    if len(pan_name) <= 25 and pan_name.isupper():
        return True
    return False

def validate_aadhaar_name(aadhaar_name):
    
    words = aadhaar_name.split()
    for word in words:
        if not word.istitle():  # first character should be uppercase
            return False
    return True

def validate_dob(dob):
    
    date_format = "%d/%m/%Y"
    try:
        dob_date = datetime.strptime(dob, date_format)
        
        # Check if the date is not in the future
        if dob_date > datetime.now():
            return False
        
        return True
    except ValueError:
        return False


def valid(data):
    # Extract values from the dictionary
    card_type = data.get("Type")
    name = data.get("Name")
    dob = data.get("DOB")
    
    if card_type == "PAN":
        # Validate PAN details
        if not validate_pan_name(name):
            return False,"Invalid PAN Name."
        
        if not validate_pan_name(data.get("Father's Name")):
            return False,"Invalid Father's Name."
        
        if not validate_dob(dob):
            return False,"Invalid Date of Birth."
    
    elif card_type == "Aadhaar":
        # Validate Aadhaar details
        if not validate_aadhaar_name(name):
            return False,"Invalid Aadhaar Name."
        
        if not validate_dob(dob):
            return False,"Invalid Date of Birth."
    
    else:
        return "Invalid Card Type."

    return True,"All data is valid!"

if __name__=='main':

    data_aadhaar = {
        "Type": "Aadhaar",
        "Name": "John Doe",      
        "DOB": "11/00/1962"      
    }

#      data_pan = {
#     "Type": "PAN",
#     "Name": "JOHN DOE",         # Example PAN Name
#     "Father's Name": "JAMES DOE", # Example Father's Name
#     "DOB": "12/01/1962"         # Example Date of Birth
# }

    # validation_result_pan = valid(data_pan)
    # print(validation_result_pan) 

    validation_result_aadhaar = valid(data_aadhaar)
    print(validation_result_aadhaar) 
