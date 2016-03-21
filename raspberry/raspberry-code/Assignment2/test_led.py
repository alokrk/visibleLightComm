import RPi.GPIO as GPIO
import time
import sys

#list = ['1', '0', '1', '0', '1', '0'];
#mylist = [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1];
mylist = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]; 
#0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1];


GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

for mybit in mylist:
	if ( mybit == 1 ) :
        	GPIO.output(16, True)
		time.sleep(.04)
		GPIO.output(16, False)
		time.sleep(.04)
	else:
		GPIO.output(16, False)
		time.sleep(.04)
        	GPIO.output(16, True)
		time.sleep(.04)
		
print ''.join(str(mli) for mli in mylist)
GPIO.output(16, False)

