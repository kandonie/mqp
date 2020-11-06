To run, python3 main.py

Currently, things happen based on the GUI. When there is
a change in the GUI, the GUI notifies the state machine (which 
observers the GUI). The state machine's notify currently calls 
appropriate functions on the drive and motor. These call functions
in WiFi to send json info the the ESP. The ESP then makes appropriate
corresponding actions. In the near future, the stae machine's notify 
will only update variables. The the runStateMachin will call 
appropriate functions based on those variabels.