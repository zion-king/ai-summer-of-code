import json,os, numpy
import re
from datetime import datetime as dts
from src.config import appconfig
import yaml

def load_yaml_file(file_path):
    """
    Reads a YAML file and returns its contents as a Python dictionary.
    
    Args:
        file_path (str): The path to the YAML file.
        
    Returns:
        dict: The contents of the YAML file as a Python dictionary.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data



def get_day_date_month_year_time():
    """
    Get the current date and time with the day of the week as separate variables.

    Returns:
    tuple: A tuple containing current_date, day_of_week, day, month, year, hour, minute, and second.
    """
    current_datetime = dts.now()

    current_date = current_datetime.strftime('%m-%d-%Y')
    day_of_week = current_datetime.strftime('%A')
    day = current_datetime.day
    month = current_datetime.month
    year = current_datetime.year
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    return current_date, day_of_week, day, month, year, hour, minute, second


def check_final_answer_exist(string_to_check):
    """
    Check if 'final' and 'answer' exist in any form in the given string using regex.

    Parameters:
    string_to_check (str): The input string to check.

    Returns:
    bool: True if both 'final' and 'answer' exist, False otherwise.
    """
    # Define the regex pattern for 'final' and 'answer' in any form
    pattern = re.compile(r'\bfinal[_\s]*answer\b|\banswer[_\s]*final\b', re.IGNORECASE)

    # Check if the pattern is found in the string
    return bool(pattern.search(string_to_check))

def get_last_item(directory_path):
    """
    Get the last item (file or directory) in a specified directory.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        str: Full file name with extension of the last item.
    """
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        items = os.listdir(directory_path)
        if items:
            last_item = items[-1]
            full_path = os.path.join(directory_path, last_item)
            return full_path
        else:
            return "Directory is empty."
    else:
        return "Invalid directory path."


def empty_arrays_if_length_4(arr1: list, arr2: list, arr3: list) -> None:
    """
    Empties the provided arrays if the length of the first array is 2.

    Args:
        arr1 (list): The first array to check and potentially clear.
        arr2 (list): The second array to potentially clear.
        arr3 (list): The third array to potentially clear.
    """
    # Check if the first array has a length of 2
    if len(arr1) == 2:
        # If so, empty all three arrays
        arr1.clear()
        arr2.clear()
        arr3.clear()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    

def capitalize_first_letters(sentence):
    # Split the input sentence into individual words
    words = sentence.split()

    # Capitalize the first letter of each word and join them back into a sentence
    capitalized_sentence = ' '.join(word.capitalize() for word in words)

    # Return the resulting sentence with capitalized first letters
    return capitalized_sentence

def performance_tracker(ops):
    if appconfig.Env=="development":
        print(ops)
    else:
        pass
