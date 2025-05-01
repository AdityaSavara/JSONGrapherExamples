import os
import json
import copy

def update_title_field(data, depth=1, max_depth=10):
    """ Recursively checks for 'title' fields and converts them to dictionary format. """
    if depth > max_depth or not isinstance(data, dict):
        return data
    
    for key, value in data.items():
        if key == "title" and isinstance(value, str):
            data[key] = {"text": value}
        elif isinstance(value, dict):  # Nested dictionary
            data[key] = update_title_field(value, depth + 1, max_depth)
        elif isinstance(value, list):  # Lists can contain nested dictionaries
            data[key] = [update_title_field(item, depth + 1, max_depth) if isinstance(item, dict) else item for item in value]
    
    return data

def remove_extra_information_field(data, depth=1, max_depth=10):
    """Recursively checks for 'extraInformation' fields and removes them."""
    if depth > max_depth or not isinstance(data, dict):
        return data

    # Use a copy of the dictionary keys to safely modify the dictionary during iteration
    for key in list(data.keys()):
        if key == "extraInformation":
            del data[key]  # Remove the field
        elif isinstance(data[key], dict):  # Nested dictionary
            data[key] = remove_extra_information_field(data[key], depth + 1, max_depth)
        elif isinstance(data[key], list):  # Lists can contain nested dictionaries
            data[key] = [
                remove_extra_information_field(item, depth + 1, max_depth) if isinstance(item, dict) else item for item in data[key]
            ]
    
    return data
    

def remove_nested_comments(data, top_level=True):
    """Removes 'comments' fields that are not at the top level of the JSON-dict. Starts with 'top_level = True' when dict is first passed in then becomes false after that. """
    if not isinstance(data, dict):
        return data

    # Process nested structures
    for key in list(data.keys()):
        if isinstance(data[key], dict):  # Nested dictionary
            data[key] = remove_nested_comments(data[key], top_level=False)
        elif isinstance(data[key], list):  # Lists can contain nested dictionaries
            data[key] = [
                remove_nested_comments(item, top_level=False) if isinstance(item, dict) else item for item in data[key]
            ]

    # Only remove 'comments' if not at the top level
    if not top_level:
        data = {k: v for k, v in data.items() if k != "comments"}

    return data

def clean_json_dict(json_dict, fields_to_update=["title_field", "extraInformation", "nested_comments"]):
    data = json_dict
    #unmodified_data = copy.deepcopy(data)
    if "title_field" in fields_to_update:
        data = update_title_field(data)
    if extraInformation in fields_to_update:
        data = remove_extra_information_field(data)
    if "nested_comments" in fields_to_update:
        data = remove_nested_comments(data)
    return data
    
def clean_json_files(base_dir, max_depth=10, fields_to_update=["title_field", "extraInformation", "nested_comments"]):
    """ Walks through directories up to 'max_depth', modifies JSON files, and saves updates. """
    changed_files = []
    
    for root, _, files in os.walk(base_dir):
        depth = root[len(base_dir):].count(os.sep) + 1
        if depth > max_depth:
            continue  # Skip folders beyond depth limit
        
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    unmodified_data = copy.deepcopy(data)
                    if "title_field" in fields_to_update:
                        data = update_title_field(data)
                    if "extraInformation" in fields_to_update:
                        data = remove_extra_information_field(data)
                    if "nested_comments" in fields_to_update:
                        data = remove_nested_comments(data)
                    if data != unmodified_data:  # Only write if changes were made
                        with open(file_path, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        changed_files.append(file_path)
                
                except (json.JSONDecodeError, IOError) as e:
                    print(f"Skipping {file_path}: {e}")

    return changed_files

# Execution
if __name__ == "__main__":
    working_dir = os.getcwd()  # Use current working directory
    #modified_files = clean_json_files(working_dir, fields_to_update=["title_field"])
    modified_files = clean_json_files(working_dir, fields_to_update=["extraInformation", "nested_comments"])
    
    print("\nModified JSON files:")
    for file in modified_files:
        print(file)
