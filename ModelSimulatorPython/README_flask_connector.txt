Users should expect to edit flask_connector_settings.py but not flask_connector.py

To use this directory, perform the following steps:
(1) Put a module that has (or can call) your python function within the subdirectory .\python_models or elsewhere.
(2) edit flask_connector_settings.py  to add the system path to your module if is elswhere. Then import your modules. Add the name of your function, as well put your function into the dictionary that the flask connector will use, make a note of the dictionary key (the 'name' that you put for the function in your dictionary).
(3) Put that same dictionary key into the simulation_function_label field for the JSON file.


To use with JSONGrapher:
(1) run the flask connector with:
python flask_connector.py
(2) start the pinggy ssh to http connection within another window (just press enter when asked for a passsword):
ssh -p 443 -o StrictHostKeyChecking=no -R0:127.0.0.1:5000 a.pinggy.io x:xff x:fullurl a:origin:adityasavara.github.io x:passpreflight
(3) copy the pinggy link and paste it into the JSONGrapher record.
(4)Drag your JSONGrapher JSON file into JSONGrapher to initialize.
(5)Drag your file into JSONGrapher a second time. 


To test locally, which is useful for file creation and debugging, requires the following steps:

(1) run the flask connector with:
python flask_connector.py
(2) start the pinggy ssh to http connection with the below command (just press enter when asked for a password):
ssh -p 443 -o StrictHostKeyChecking=no -R0:127.0.0.1:5000 a.pinggy.io x:xff x:fullurl a:origin:adityasavara.github.io x:passpreflight
(3) open httpsCall_local_tester.html
(4) enter the https link
(5) upload your JSONGrapher JSON file
(6) click the button to run a simulation.
