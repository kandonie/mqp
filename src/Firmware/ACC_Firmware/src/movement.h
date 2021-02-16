
void movementSetup();
void testPWM();
void enablePWM(String system);
void disablePWM(String system);
void setRight(int speed);
void setLeft(int speed);
void setWeapon(int speed);
boolean PWMDriveDisabled();
boolean PWMWeaponDisabled();
bool turnToAngle(double currentHeading, double desiredHeading);