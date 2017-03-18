#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); // RX (connect to TX of other device), TX (connect to RX of other device)
unsigned int mymillidelay = 24;

byte in[17];
byte firstbytefault[2];
byte i = 0;

void setup()
{
  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // set the data rate for the SoftwareSerial port
  mySerial.begin(19200);
}

void loop() // run over and over
{
  byte val = 0;

  in[0] = val;
  in[1] = val;
  in[2] = val;
  in[3] = val;
  in[4] = val;
  in[5] = val;
  in[6] = val;
  in[7] = val;
  in[8] = val;
  in[9] = val;
  in[10] = val;
  in[11] = val;
  in[12] = val;
  in[13] = val;
  in[14] = val;
  in[15] = val;
  in[16] = '\n';

  firstbytefault[0] = i;
  firstbytefault[1] = '\n';

  i+= 1;

  Serial.print("Current delay: ");
  Serial.println(mymillidelay);

  // Push the message
  mySerial.write(in, sizeof(in));

  delay(mymillidelay);

  // Faulting just the first byte
  mySerial.write(firstbytefault, sizeof(firstbytefault));

  // Stop after 256 injections
  if (i == 0)
  {
    while(1);
  }

  delay(1500);
}

