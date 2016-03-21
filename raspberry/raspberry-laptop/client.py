#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import fcntl
import struct
import sys

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', "eth0")
    )[20:24])

myip=get_ip_address('eth0')  # '192.168.0.110
print myip

#host = socket.gethostname() # Get local machine name
host = "192.168.224.2"# Get local machine name port = 12345                # Reserve a port for your service.
port=12345
try:
	s = socket.socket()         # Create a socket object
except socket.error as msg:
	s = None
	exit();	
try:
	s.connect((host, port))
except socket.error as msg:
	s.close()
	s = None
	exit()	
while True:
	x = getch();
	s.send(x);
	if ( ord(x) == 4 ):
		break;
	else:
		if ( ord(x) == 13 ):
			print("");
		else:
			sys.stdout.write(x)
			sys.stdout.flush()
	
print s.recv(1024)
s.close()                     # Close the socket when done
