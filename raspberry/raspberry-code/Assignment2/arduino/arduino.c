#define THRESHOLD	64
#define PREAMBLE_LEN	8
#define FIXED_DATA_LEN  10
#define PKT_LEN		18
#define IFS_LEN		4
int preamble[8] = { '1', '0', '1', '0', '1', '0', '1', '0'};
int inPreamble = 0;
int inData = 0;
int inIFS = 0;


if (outVal > THRESHOLD)
	bit = high;
else
	bit = low;

if ((inPreamble == 0) && bit) 
{
	//Possibly the preamble start
	inPreamble = 1;
	count = 0;
}
else if ((inPreamble == 1) && (count < PREAMBLE_LEN))
{
	if (bit == preamble[count + 1])
		count = count + 1;
}
else if ((inPreamble == 1) && (count == PREAMBLE_LEN))
{
	inPreamble = 0;
	inData = 1;
	Serial.print(bit);
	count = count + 1;
}
else if ((inData == 1) && (count < PKT_LEN))
{
	Serial.print(bit);	
	count = count + 1;
}
else if ((inData == 1) && (count == PKT_LEN))
{
	inData = 0;
	inIFS = 1;
	count = 0;
}
else
{
	inData = 0;
	inPreamble  = 0;
	count = 0;
}
