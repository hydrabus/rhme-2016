int monitorPin = 8;
int state = 0;
int prev_state = 0;
unsigned long count = 0;
int flushed = 0;

// the setup routine runs once when you press reset:
void setup() {

  // Open serial communications and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  pinMode(monitorPin, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin, delay to stabilize read value
  delayMicroseconds(50);
  state = digitalRead(monitorPin);

  if (state == prev_state)
  {
    count++;
  }
  else
  {
    // print out the state
    if (count < 500)
    {
      Serial.write(' ');Serial.print(count);
    }
    count = 1;
    flushed = 0;
  }
  if (count >= 500)
  {
      if (!flushed)
      {
        Serial.write("\n");
      }
      flushed = 1;
  }
  prev_state = state;

}
