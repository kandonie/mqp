To run:
    python3 main.py <shouldConnectToWiFi>

shouldConnectToWiFi defaults to True. True tries to connect to WiFi. False will never try to connect
but will also load faster. Good for testing without the ESP

Currently, things happen based on the GUI. When there is
a change in the GUI, the GUI notifies the state machine (which 
observers the GUI). The state machine's notify currently calls 
appropriate functions on the drive and motor. These call functions
in WiFi to send json info the the ESP. The ESP then makes appropriate
corresponding actions. In the near future, the state machine's notify 
will only update variables. The the runStateMachine will call 
appropriate functions based on those variables.
