from time import sleep
import serial
import sys
import socket               # Import socket module
import fcntl
import struct


preamble_len = 8;
preamble = [ '1', '0' ,'1', '0', '1', '0', '1', '0' ];
pkt_ifs =  [ '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1' ]; pkt_ifs_len = 12; inPreamble = 0;
inData = 0;
inIfs = 0;
count = 0;
ifs_count = 0;
max_pkt_len = 2072; 	# 255 chars + 4 byte checksum


#host = socket.gethostname() # Get local machine name
host = "192.168.2.15"# Get local machine name port = 12345                # Reserve a port for your service.
port=44444
try:
        s = socket.socket()         # Create a socket object
except socket.error as msg:
        s = None
        exit();
try:
        s.connect((host, port))
except socket.error as msg:
	print msg
        s.close()
        s = None
        exit()


ser = serial.Serial('/dev/ttyACM0',115200)
#counter=32
data = [];
sleep(1.5)
while True:
	cur_bit = ser.readline(1)
#	sys.stdout.write(cur_bit);
#	sys.stdout.flush();
	if ((inPreamble == 0) and (inData == 0) and (cur_bit == '1')):
		#Possibly the preamble start
		inPreamble = 1;
		count = 1;
		msgckbitlen = max_pkt_len;
		#data.append(cur_bit);
	elif ((inPreamble == 1) and (count < preamble_len)):
		if (cur_bit == preamble[count]):
			#data.append(cur_bit);
			count = count + 1;
		else:
			if ( cur_bit == '0'):
				inPreamble = inData = inIFS = 0;
				count = 0;
				data = [];
			else:
				inPreamble = 1;
				count  = 1;
	elif ((inPreamble == 1) and (count == preamble_len)):
		inPreamble = 0;
		inData = 1;
		count = count + 1;
#		sys.stdout.write('|');
#		sys.stdout.flush();
		data.append(cur_bit);
		if (cur_bit == '1'):
			ifs_count = 1;
	elif ((inData == 1)):
#		sys.stdout.write(cur_bit);
#		sys.stdout.flush();
		data.append(cur_bit);
		count = count + 1;
		if (count == 24):
			#extract len of the packet
			msgidbits = ''.join(data[0:8])
			msgid = int(msgidbits, 2);
			lenbits = ''.join(data[8:16])
			msglen = int(lenbits, 2);
			#print "msgid msglen", msgid, msglen;
			msgcklen = msglen + 1;	# 1 byte for checksum
			msgckbitlen = (msgcklen * 8) + 16 + 8; 	#preamble + msgcklen + msgid byte + len byte 
			#print "msgbitlen", msgckbitlen

		if (count >= msgckbitlen ):
			i = 2;
			lrc = 0
			lrc ^= msgid
			lrc ^= msglen
			#print "msglen ", msglen;
			msg=""
			for i in range(2, msglen + 2):
				bytebits = ''.join(data[i*8: (i+1)*8])
				intbyte = int(bytebits, 2);
				lrc^=intbyte;
				msg= msg + str(chr(intbyte));
#				sys.stdout.write(recovered_char)
#				sys.stdout.flush();
			
			recvlrc = int(''.join(data[(msglen + 2)*8: (msglen + 3)*8]), 2);
			if ( lrc == recvlrc ):
				sys.stdout.write(msg);	
				sys.stdout.flush();
				s.send(str(msgid));
#				#print "msgid lrc recvlrc", str(msgid), lrc, recvlrc;
			else:
				s.send("5000");		# Message ID too large which doesn't fall in this 
				print " TODO :Checksum failed"
				print ''.join(data)
			count = 0;	
			inPreamble = 0
			inData = 0
			data = [];
#		if (cur_bit == '1'):
#			ifs_count = ifs_count + 1;
#		else:
#			ifs_count = 0;

#		if (ifs_count == pkt_ifs_len):
			#inPreamble = 0
			#inData = 0
			#newdata = ''.join(data)
			#print ""
			#sys.stdout.write("data ->  ");
			#sys.stdout.write(newdata);
			#sys.stdout.flush();
			#print ""
			#print "data ->  ", newdata;
			#print data
			#print ""
