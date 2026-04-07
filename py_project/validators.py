"""
Input validation functions for the Student Examination Portal
"""

import re
from constants import MIN_MARKS, MAX_MARKS, ERROR_PREFIX

def validate_id(id_value, id_type="ID"):
    """
    Validate if ID is non-empty and alphanumeric.
    
    Args:
        id_value (str): The ID to validate
        id_type (str): Type of ID for error message
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not id_value or not id_value.strip():
        return False, f"{ERROR_PREFIX}{id_type} cannot be empty"
    
    if len(id_value.strip()) > 50:
        return False, f"{ERROR_PREFIX}{id_type} is too long (max 50 characters)"
    
    return True, ""


def validate_name(name):
    """
    Validate if name is valid (letters, spaces, hyphens).
    
    Args:
        name (str): The name to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, f"{ERROR_PREFIX}Name cannot be empty"
    
    if len(name.strip()) > 100:
        return False, f"{ERROR_PREFIX}Name is too long (max 100 characters)"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, f"{ERROR_PREFIX}Name contains invalid characters"
    
    return True, ""


def validate_marks(marks):
    """
    Validate if marks are within valid range.
    
    Args:
        marks (str): The marks to validate
        
    Returns:
        tuple: (is_valid, error_message, marks_int)
    """
    try:
        marks_int = int(marks)
        if marks_int < MIN_MARKS or marks_int > MAX_MARKS:
            return False, f"{ERROR_PREFIX}Marks must be between {MIN_MARKS} and {MAX_MARKS}", None
        return True, "", marks_int
    except ValueError:
        return False, f"{ERROR_PREFIX}Marks must be a valid number", None


def validate_roll_number(roll_no):
    """
    Validate if roll number is valid.
    
    Args:
        roll_no (str): The roll number to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not roll_no or not roll_no.strip():
        return False, f"{ERROR_PREFIX}Roll number cannot be empty"
    
    if len(roll_no.strip()) > 20:
        return False, f"{ERROR_PREFIX}Roll number is too long (max 20 characters)"
    
    return True, ""


def validate_yes_no(response):
    """
    Validate if response is yes or no.
    
    Args:
        response (str): The response to validate
        
    Returns:
        tuple: (is_valid, is_yes)
    """
    if response.lower() in ('y', 'yes'):
        return True, True
    elif response.lower() in ('n', 'no'):
        return True, False
    return False, None


def validate_percentage(percentage):
    """
    Validate if percentage is valid (0-100).
    
    Args:
        percentage (float): The percentage to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        pct = float(percentage)
        if pct < 0 or pct > 100:
            return False, f"{ERROR_PREFIX}Percentage must be between 0 and 100"
        return True, ""
    except ValueError:
        return False, f"{ERROR_PREFIX}Percentage must be a valid number"


def safe_input(prompt, validation_func=None, validator_args=None):
    """
    Get validated user input with error handling.
    
    Args:
        prompt (str): The prompt to display
        validation_func (callable): Optional validation function
        validator_args (dict): Arguments for validation function
        
    Returns:
        str: The validated user input
    """
    validator_args = validator_args or {}
    
    while True:
        try:
            user_input = input(prompt).strip()
            
            if validation_func:
                result = validation_func(user_input, **validator_args)
                if isinstance(result, tuple):
                    is_valid = result[0]
                    if len(result) > 1:
                        error_msg = result[1]
                    else:
                        error_msg = ""
                else:
                    is_valid = result
                    error_msg = ""
                
                if not is_valid:
                    if error_msg:
                        print(error_msg)
                    continue
            
            return user_input
        
        except KeyboardInterrupt:
            print(f"\n{ERROR_PREFIX}Operation cancelled by user")
            raise
        except Exception as e:
            print(f"{ERROR_PREFIX}An error occurred: {str(e)}")
            continue
