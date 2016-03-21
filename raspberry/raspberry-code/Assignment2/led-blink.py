import RPi.GPIO as GPIO
import time

#list = ['1', '0', '1', '0', '1', '0'];

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
#while (True):
i = 0
list = [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1]

while (i < 4):
	GPIO.output(16, True)
	#time.sleep(.01)
	time.sleep(.008)
	#time.sleep(1)
	GPIO.output(16, False)
	#time.sleep(.01)
	time.sleep(.008)
	#time.sleep(1)
	GPIO.output(16, False)
	#time.sleep(.01)
	time.sleep(.008)
	GPIO.output(16, True)
	#time.sleep(.01)
	time.sleep(.008)
	i=i+1
	
state = 1;
j = 0
while (j < 1024):
	if ( state == 0 ):
		GPIO.output(16, True)
		time.sleep(.008)
		GPIO.output(16, False)
		time.sleep(.008)
		state = 1;
	else:
		GPIO.output(16, False)
		time.sleep(.008)
		GPIO.output(16, True)
		time.sleep(.008)
		state = 0;
		
	j = j + 1;

GPIO.output(16, False)
time.sleep(.008)
GPIO.output(16, False)
time.sleep(.008)
GPIO.output(16, False)
time.sleep(.008)
GPIO.output(16, False)
time.sleep(.008)

GPIO.cleanup()
