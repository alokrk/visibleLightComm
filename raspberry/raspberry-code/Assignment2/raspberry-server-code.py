#!/usr/bin/python           # This is server.py file

import sys
import socket               # Import socket module
import fcntl
import struct
import RPi.GPIO as GPIO
import time
import binascii
import zlib

preamble = [ 0, 1, 1, 0, 1, 0, 1, 0, 1, 0 ];
pkt_end =  [ 1, 1, 1, 1]; #, 1, 1, 1, 1, 1, 1, 1, 1];
msg_id = 0;
max_msg_id = 256;
msg_len = 0;
def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result;

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname)
    )[20:24])

eth_ip=get_ip_address('eth0')  # '192.168.0.110
wlan_ip=get_ip_address('wlan0')  # '192.168.0.110

print eth_ip 
print wlan_ip

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, False)

# socket to listen from arduino
print "Please connect from arduino laptop now"
r = socket.socket()
arduino_port = 44444
r.bind((wlan_ip, arduino_port))        # Bind to the port

r.listen(5)                 # Now wait for client connection.
a, ar_addr = r.accept()     # Establish connection with client.
print 'Got connection from arduino receiver', ar_addr

#socket to listen from raspberry-client
print "Please connect from raspberry client laptop now"
s = socket.socket()         # Create a socket object
rasp_client_port = 12345                # Reserve a port for your service.
s.bind((eth_ip, rasp_client_port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
c, addr = s.accept()     # Establish connection with client.
print 'Got connection from', addr

while True:
	GPIO.output(16, False)
	x = c.recv(10);
	msg_len = len(x);
#if ( ord(x) == 4 ):
#break;
#	a=1
#else:

#if ( ord(x) == 13):
#print("");
#else:
#sys.stdout.write(x)
	msg_id = (msg_id + 1) % max_msg_id;
#	msg = tobits(str(msg_id));
#	print tobits(x)
#	print list(map(int, bin(msg_id)[2:].zfill(8)))
	bit_msg = list(map(int, bin(msg_id)[2:].zfill(8))) + list(map(int, bin(msg_len)[2:].zfill(8))) + tobits(x);
	#bit_msg =  list(map(int, bin(msg_len)[2:].zfill(8))) + tobits(x);
#	print bit_msg
#print len(frombits(bit_msg));

	#print len(bit_msg);
	lrc = 0
	for b in range(0 , len(bit_msg) / 8):
		lrc ^= ord(frombits(bit_msg[b*8:(b+1) * 8])); 
		#message += chr(lrc)        # Add the LRC byte

	#msg_crc = zlib.adler32(frombits(bit_msg)) & 0xffffffff;
#	print msg_crc;
#	msg_crc= binascii.crc32(frombits(bit_msg)) & 0xffffffff;
	bit_msg = bit_msg + list(map(int, bin(lrc)[2:].zfill(8)))
#	print bit_msg
#	a=''.join(bit_msg);
#	print ''.join(bit_msg);
#	print frombits(map(int, bit_msg))

#	print frombits(''.join(bit_msg));
#	msg = msg + tobits(str(msg_len));
#	print map(str, mydata);
#	print tobits(x); 
#	sys.stdout.flush()
	bit_msg = preamble + bit_msg; # + pkt_end;
	print ''.join(str(mli) for mli in bit_msg);
# Hack since first bit was missing in many packets 
	sent_successful = False;
	while (sent_successful == False):
		print "Sending message :", msg_id
		for mybit in bit_msg:
			if ( mybit == 1 ):
				GPIO.output(16, True)
				time.sleep(.05)
#				time.sleep(.008)
#				GPIO.output(16, False)
#				time.sleep(.04)
			else:
				GPIO.output(16, False)
				time.sleep(.05)
#				GPIO.output(16, True)
#				time.sleep(.04)
		GPIO.output(16, False)
		a.settimeout(2)
		try:
			ard_resp = a.recv(10);
		except socket.timeout, e:
			err = e.args[0]
			# this next if/else is a bit redundant, but illustrates how the
			# timeout exception is setup
			if err == 'timed out':
#				time.sleep(1)
				print 'recv timed out, retry later'
				continue
			else:
				print e
				sys.exit(1)

		print ard_resp, str(msg_id);
		if (ard_resp == str(msg_id)):
			sent_successful = True;	


c.send('Thank you for connecting')
c.close()                # Close the connection
