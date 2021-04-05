

The GUI allows the user to do several things, including viewing data and sending instructions.

The first important feature to note is the ESTOP button in the top left. This will stop the robot.
To the right of this button, we have enable/disable drive and weapon. These buttons determine if
the corresponding motors can more, regaurdless of any state of autonomy.

Next is the intelligence state. Idle means the robot will do nothing. Selecting Remote Control will
open a new window and allow you to drive the robot with the arrow keys. Further instructions reside in
this window. Closing the window brings you back to the main window. Autonomous means the robot will
exercise some autonomous control. For example, you can set the pwm with the GUI and it will move (assuming
drive is enabled), or it may enter a match. The begin match button tells the robot that it is beginning
a combat match and will begin executing the appropriate states of its state maching. Match over sends the
robot into the match over state, where it will perform appropriate actions for a match being over, such as
driving to the door or turning off. Finally, the reset match button reinitializes the robot.

Moving downward, on the left, one can see various data about the robot, provided by the robot. On the right,
the image used by the CV is shown. These are each updated every 500 ms.

At the bottom of the screen lies manual controls for testing the robot. The first column allows you to set
the pwm value of each motor when the button is clicked. The next column allows you to sed the PID values
for all motors when the button is clicked. The next button, set heading, allows you to choose which angle
the robot should turn to face when the button is clicked. Finally, the set distance button tells the robot
to drive a certain distance when clicked.
