# Parses the unit value from the input and returns both the value and the units
def parse_units(value):
    # Find the position of the first '(' and the last ')'
    start = value.find('(')
    end = value.rfind(')')
    
    if start != -1 and end != -1 and end > start:  # Ensure both are found and properly ordered
        number_part = value[:start].strip()  # Everything before '('
        units_part = value[start + 1:end].strip()  # Everything inside '()'
        parsed_output = {
            "value": float(number_part),  # Convert number part to float
            "units": units_part  # Extracted units
        }
    else:
        parsed_output = {
            "value": float(value),  # No parentheses, assume the entire string is numeric
            "units": ""
        }
    return parsed_output

if __name__ == "__main__":
    result1 = parse_units("200 (1/(bar * s))")
    result2 = parse_units("3.14 (kg/(m^3))")
    result3 = parse_units("500 (J/mol)")
    result4 = parse_units("42")

    print(result1)
    print(result2)
    print(result3)
    print(result4)