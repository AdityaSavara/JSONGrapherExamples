
import sys

#### Add the relative or absolute paths to your python modules here ####
sys.path.append('./python_models')

#### Import your python functions here ####
from Langmuir_isotherm_kadskdes import simulate as simulate_langmuir_isotherm_kadskdes
from Langmuir_isotherm_Keq import simulate as simulate_langmuir_isotherm_Keq
#from another_module import another_function as second_function

###Put your functions into the functions dictionary here###
# Whatever you use as the dictionary key should be used as the simulation_function_label in the json file(s)
# This way, you can have multiple functions callable from a single serveo server.
functions_dictionary = {}
functions_dictionary["simulate_Langmuir_by_kadskdes"] = simulate_langmuir_isotherm_kadskdes
functions_dictionary["simulate_Langmuir_by_Keq"] = simulate_langmuir_isotherm_Keq

