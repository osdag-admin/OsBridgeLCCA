# Global dictionary to store form data
form_data = {}

def save_form_data(window_name, data):
    """
    Save form data to the global dictionary.

    Args:
        window_name (str): The name of the window/dialog.
        data (dict): The data to save.
    """
    form_data[window_name] = data

def get_form_data(window_name):
    """
    Retrieve form data for a specific window.

    Args:
        window_name (str): The name of the window/dialog.

    Returns:
        dict: The saved data for the window, or an empty dictionary if not found.
    """
    return form_data.get(window_name, {})