import time as t;
import wiringpi;
from wiringpi import GPIO;

#INIT GPIO(ALL)
NUM_0 = 2 #green / 7 pin
NUM_1 = 6 #red / 12 pin
NUM_2 = 11 #violet / 19 pin
NUM_3 = 8 #blue / 15 pin
NUM_4 = 16 #orange / 26 pin

#INIT wiringPI
wiringpi.wiringPiSetup();
wiringpi.setwarning = False;

#Set all in OUT
ARRAY_GPIO = [NUM_0,NUM_1,NUM_2,NUM_3,NUM_4];
for Num in ARRAY_GPIO:
    wiringpi.pinMode(Num, GPIO.OUTPUT);
    print(str(wiringpi.digitalRead(Num)) + "    !");

####################
#  #  #  #  #  #  #
####################
#  #  #  #  #  #  #
####################

for Num in ARRAY_GPIO:
    wiringpi.pinMode(Num, GPIO.INPUT);
    print(str(wiringpi.digitalRead(Num)) + "    ¡");

