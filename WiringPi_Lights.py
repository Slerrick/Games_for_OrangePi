import wiringpi;
import time as t;
import sys;
from wiringpi import GPIO;

#INIT GPIO(ALL)
NUM_0 = 2 #green / 7 pin
NUM_1 = 6 #red / 12 pin
NUM_2 = 11 #violet / 19 pin
NUM_3 = 8 #blue / 15 pin
NUM_4 = 16 #orange / 26 pin

#INIT wiringPI
wiringpi.wiringPiSetup();
wiringpi.serwarhing = False;

#Set all in OUT
ARRAY_GPIO = [NUM_0,NUM_1,NUM_2,NUM_3,NUM_4];
for Num in ARRAY_GPIO:
    wiringpi.pinMode(Num, GPIO.OUTPUT);
    print(wiringpi.digitalRead(Num));

i = 0
while i < 3:
    
    ARRAY_GPIO = [NUM_0,NUM_4,NUM_1];
    for Num in ARRAY_GPIO:
        wiringpi.digitalWrite(Num, GPIO.HIGH);
        t.sleep(1)

    t.sleep(3)
    
    a = 0

    while a < 5:

        for Num in ARRAY_GPIO:
            wiringpi.digitalWrite(Num, GPIO.LOW);

        t.sleep(0.4)

        for Num in ARRAY_GPIO:
            wiringpi.digitalWrite(Num, GPIO.HIGH);

        t.sleep(0.4)

        a += 1 

    for Num in ARRAY_GPIO:
        wiringpi.digitalWrite(Num, GPIO.LOW);

    t.sleep(3)

    wiringpi.digitalWrite(2, GPIO.HIGH)

    t.sleep(2)

    wiringpi.digitalWrite(16, GPIO.HIGH)
    wiringpi.digitalWrite(2, GPIO.LOW)

    t.sleep(2)

    wiringpi.digitalWrite(16, GPIO.LOW)
    wiringpi.digitalWrite(6, GPIO.HIGH)

    t.sleep(2)

    wiringpi.digitalWrite(6, GPIO.LOW)

    i += 1

#Set all in IN
ARRAY_GPIO = [NUM_0,NUM_1,NUM_2,NUM_3,NUM_4];
for Num in ARRAY_GPIO:
    wiringpi.pinMode(Num, GPIO.INPUT);
    print(wiringpi.digitalRead(Num));
   
sys.exit(0)