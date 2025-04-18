import json
#### Add the relative path to the units_helper.parse_units module for convenience ####
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import units_helper

## The simulate function should expect to receive a JSON-like dictionary or JSON-like string.
def simulate(input_data):
    # Ensure the input is valid json by converting it back and forth to a string.
    try:
        input_data = json.dumps(input_data)
        input_data = json.loads(input_data)
    except:
        raise TypeError("Input data is not valid JSON.")

    # Extract simulation parameters
    simulation_parameters = input_data["simulate"]  # Accessing directly

    # Use K_eq provided in the input
    K_eq_obj = units_helper.parse_units(simulation_parameters["K_eq"])

    #Set sigma max
    if "sigma_max" in simulation_parameters:
        sigma_max = simulation_parameters["sigma_max"]  
    else:
        sigma_max = "1(<Monolayer>)"
    sigma_max_value_and_units = units_helper.parse_units(sigma_max)

    # This is the actual "simulation"
    def get_predicted_values(K_eq_value, K_eq_unit, sigma_max=1, sigma_max_unit="<Monolayer>"):
        x_label = f"Pressure (1/({K_eq_unit}))"
        y_label = f"Amount Adsorbed ({sigma_max_unit})"
        Y_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] #For our langmuir simulation we use Y to get X in this case. Coverage to calculate pressure.
        X_values = [sigma_max * y / (K_eq_value * (1 - y)) for y in Y_values]
        
        predicted_values = {
            "X_values": X_values,
            "Y_values": Y_values,
            "x_label": x_label,
            "y_label": y_label
        }
        return predicted_values

    # This calls the helper function get_predicted_values to do the simulation.
    # We don't need input_data here, we are just passing it through with the simulation.
    def run_simulation(input_data, K_eq_obj, sigma_max_value_and_units):
        predicted_values = get_predicted_values(K_eq_obj["value"], K_eq_obj["units"], sigma_max_value_and_units["value"], sigma_max_value_and_units["units"])
        
        simulation_output = {
            **input_data, #this is optional, but it provides back the simulation parameters to JSONGrapher.
            "x": predicted_values["X_values"],
            "y": predicted_values["Y_values"],
            "x_label": predicted_values["x_label"],
            "y_label": predicted_values["y_label"]
        }
        
        simulation_result = {
            "success": True,
            "message": "Simulation completed successfully",
            "data": simulation_output
        }
        return simulation_result

    # Main workflow
    simulation_result = run_simulation(input_data, K_eq_obj, sigma_max_value_and_units)
    #Ensure the output is valid json by converting it back and forth to a string then dictionary.
    output_as_json_string = json.dumps(simulation_result, indent=4) 
    output_as_json_dict = json.loads(output_as_json_string)
    return output_as_json_dict
                      
if __name__ == "__main__":
    # Example with input as a JSON-like dictionary.
    input_json_as_dict = {
        "simulate": {
            "K_eq": "5.0(L/mol)",  # Using K_eq directly instead of k_ads and k_des
            "sigma_max": "1.2(<Monolayer>)",
            "simulation_function_label": "simulate_Langmuir_by_Keq"
        }
    }
    output_dict = simulate(input_json_as_dict)  # Function can handle strings or dictionaries
    print("\nOutput from JSON dictionary input: \n", output_dict)

    # Example with input as a JSON-like string.
    input_json_as_string = '{"simulate": {"K_eq": "5.0(L/mol)", "sigma_max": "1.2(<Monolayer>)", "simulation_function_label": "simulate_Langmuir_by_Keq"}}'
    output_dict = simulate(input_json_as_string)  # Function can handle strings or dictionaries
    print("\nOutput from JSON string input: \n", output_dict)

    # Expected Output:
    # Identical outputs for both inputs:
    # {
    #     "success": true,
    #     "message": "Simulation completed successfully",
    #     "data": {
    #         "simulate": {
    #             "k_ads": "0.5(mol/L)",
    #             "k_des": "0.1(s^-1)",
    #             "sigma_max": "1.2(<Monolayer>)"
    #         },
    #         "x": [
    #             0.026666666666666665,
    #             0.06,
    #             0.10285714285714286,
    #             0.16,
    #             0.24,
    #             0.36,
    #             0.5599999999999999,
    #             0.9600000000000002,
    #             2.1600000000000006
    #         ],
    #         "y": [
    #             0.1,
    #             0.2,
    #             0.3,
    #             0.4,
    #             0.5,
    #             0.6,
    #             0.7,
    #             0.8,
    #             0.9
    #         ],
    #         "x_label": "Pressure (1/((mol/L)/(s^-1)))",
    #         "y_label": "Amount Adsorbed (<Monolayer>)"
    #     }
    # }
