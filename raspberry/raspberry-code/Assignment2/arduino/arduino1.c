/*
  Analog input, analog output, serial output

 Reads an analog input pin, maps the result to a range from 0 to 255
 and uses the result to set the pulsewidth modulation (PWM) of an output pin.
 Also prints the results to the serial monitor.

 The circuit:
 * potentiometer connected to analog pin 0.
   Center pin of the potentiometer goes to the analog pin.
   side pins of the potentiometer go to +5V and ground
 * LED connected from digital pin 9 to ground

 created 29 Dec. 2008
 modified 9 Apr 2012
 by Tom Igoe

 This example code is in the public domain.

 */

// These constants won't change.  They're used to give names
// to the pins used:
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to
int ledPin = 12;

char a[4] = {'1', '0', '1', '0'};
char str1[8] = {'1', '0', '1', '0', '1', '0', '1', '0'};
//char preandDel[9] = {'0x55', '0x55', '0x55', '0x55', '0x55', '0x55', '0x55', '0xD5'}; 
//char IFS[13] = {'0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'};

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
int i = 0;


//#define THRESHOLD       64
int threshold = 400;
int preamble_len = 8;
int fixed_data_len = 160;
int pkt_len = 168;
int ifs_len = 4;
/*
#define PREAMBLE_LEN    8
#define FIXED_DATA_LEN  10
#define PKT_LEN         18
#define IFS_LEN         4
*/
int preamble[8] = { 1, 0, 1, 0, 1, 0, 1, 0};
int inPreamble = 0;
int inData = 0;
int inIFS = 0;
int state = 0;
int count = 0;


/*
void init_preamble_and_delimiter()
{
  int i = 0;

  // Set preamble bits
  for ( i = 0; i < 7; i++)
  {
    preandDel[i] = '0x55';
  }

  // Set Start frame delimiter
  preandDel[7] = '0xD5';
}

void init_inter_frame_space()
{
  int i = 0;

  for ( i = 0; i < 12; i++)
  {
    IFS[i] = '0x00';
  }
}
*/
void setup() {
  // initialize serial communications at 9600 bps:
  // init_preamble_and_delimiter();
  // init_inter_frame_space();
  Serial.begin(115200);
}

void loop() {
  // read the analog in value:
  /*
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 0, 255);
  // change the analog out value:
  analogWrite(analogOutPin, outputValue);

  // print the results to the serial monitor:
  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);
*/
/*
  for ( i = 0; i < 8; i++)
  {
      if(str1[i] == '1')
      {
        digitalWrite(ledPin, HIGH);
      }
      else
      {
        digitalWrite(ledPin, LOW);
      }
      //delay(5);
      sensorValue = analogRead(analogInPin);
     // delay(5);
  */    
     sensorValue = analogRead(analogInPin);
     /*
      Serial.print("\n sensor = ");
      Serial.print(sensorValue);
      */
      //if (sensorValue < 511)
      if (sensorValue < 400)
      {
        //Serial.print("\n sensor = 0");
      }
      else
      {
        //Serial.print("\nc = ");
        //Serial.print(count);
      }
      
      if (sensorValue > threshold)
        state = 1;
      else
        state = 0;
      Serial.print(state);
if ((inPreamble == 0) && (inData == 0) && (state == 1))
{
        //Possibly the preamble start
        inPreamble = 1;
        count = 1;
        //Serial.print("Case 1");
}
else if ((inPreamble == 1) && (count < preamble_len))
{
        count = count + 1;
        if (state == preamble[count - 1])
                ;
        else
        {
                inPreamble = 0;
                count = 0;
        }

        //Serial.print("Case 2 = ");
        //Serial.print(count);
}
else if ((inPreamble == 1) && (count == preamble_len))
{
        inPreamble = 0;
        inData = 1;
        //Serial.print("Case 3=");
        Serial.print(state);
        count = count + 1;
}
else if ((inData == 1) && (count < pkt_len))
{
        //Serial.print("Case 4");
        Serial.print(state);
        count = count + 1;
}
else if ((inData == 1) && (count == pkt_len))
{
        //Serial.print("Case 5");
        inData = 0;
        inIFS = 1;
        count = 0;
}
else
{
        //Serial.print("Case 6");
        inData = 0;
        inPreamble  = 0;
        count = 0;
}

 // }
  /* 
  //if(sensorValue < 511)
  if (sensorValue < 450)
  {
    digitalWrite(ledPin, HIGH);
  // stop the program for <sensorValue> milliseconds:
  }
  //delay(sensorValue);
  // turn the ledPin off:
  else {
    digitalWrite(ledPin, LOW);
  }
  */
  // wait 2 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading
  delay(.5);
  //delay(1000);
}
