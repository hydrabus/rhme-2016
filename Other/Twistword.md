# rhme-2016 write-up Twistword

<a name="twistword"></a>
## Twistword (Other - 400 pts)

We spent quite a lot of time dealing with *Twistword*. The principle of this challenge is that we have to provide a so-called token to the board, which is then checked. If we do not provided the expected one, the board gives us the value we should have entered.

The main problem with this challenge is that there is pretty much no clue about what you are supposed to do to break it, and in particular whether you are following the right path for that. We explored many dead ends, and probably for way too long each time!

Based on this simple behaviour, we first tried to better control what looked like a random sequence. Our initial attempts aimed at limiting the entropy sources:
- we grounded all the analog pins
- instead of a human, we had an Arduino setup to input data to the target to avoid timing-related entropy
- we even tried better controlling the temperature at which the board was running [with a hairdryer](http://skemman.is/stream/get/1946/10689/25845/1/ardrand.pdf)

Based on the name of the challenge and the way it is written on the challenge map (with upside down letters), we investigated:
- Edwards ECC curves
- quadratic twist
- blockcipher twist attacks
- Mersenne Twister (MT) and TinyMT PRNGs and their attacks with tools such as [untwister](https://github.com/altf4/untwister)

We did notice through Simple Power Analysis and Timing Analysis that there were NVM erase/writes and some processing that was not done in constant time. Consequently, we also considered:
- timing statistical distribution
- timing attack on the value comparison
- faulting the NVM modifications to skip them

We also studied the statistical quality of the generated numbers, checked whether the next output was a md5 of the previous token.

We were pretty much out of ideas, so we looked for a simpler approach, and we came up with collision attacks. So far, we had mostly collected a few to thousands of values after a single reset. The idea was now to reset then collect ten values, hoping that at some point, we would get twice the same token after a reset. If such a collision occurred, we would then check whether the second value was also colliding, meaning that the sequence was deterministic and that we would be able to replay the next token.

A rough estimate showed that we could get around 10 sequences per minute and that despite the birthday paradox, we were still looking at hours of token captures without even being sure that we were going anywhere. What a relief when we observed our first collision! We miserably failed to properly input the replayed tokens to the board, so we had to wait another couple of hours before getting a second chance...

We couldn't figure out the seeding process itself, it is still unclear whether the entropy was at least partially obtained by some analog measure or exclusively by iterating and storing a value in NVM to would not be erased by a reflash (EEPROM maybe?). A fault attack on the seeding was likely the expected way to solve the challenge. But you know... whatever works!

[Python script](twistword_collect_or_attack.py) used:
```python
import serial
import time
import sys
import glob
import os

serRiscureNano = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def reset(ser):
  ser.rts = False
  ser.dtr = False
  time.sleep(0.1)
  ser.rts = True
  ser.dtr = True

def main():

  # Prepare collision dict
  d = {}
  lf = glob.glob("collect_*")
  for f in lf:
    lines = [l.strip() for l in open(f).readlines()]
    if lines:
      d[lines[0]] = lines[1:]

  serRiscureNano.isOpen()

  collect = len(lf)
  print "Continuing collection at %08X" % collect
  while True:
    with open("collect_%08X.txt" % collect, "w") as fd:
      sys.stdout.write('.')
      sys.stdout.flush()
      reset(serRiscureNano)
      time.sleep(1.77)

      printedToken = True
      response = ""
      collision = False
      threetokens = []
      while len(threetokens) != 3:
        if printedToken:
          # "Please press enter"/"Press enter to retry"
          while serRiscureNano.in_waiting:
            response += serRiscureNano.read(1)
          response = ""
          time.sleep(0.01)
          char = serRiscureNano.write('\r\n')
          # "Token:"
          while serRiscureNano.in_waiting:
            response += serRiscureNano.read(1)
          char = serRiscureNano.write('\r\n')
          printedToken = False
          response = ""
        while serRiscureNano.in_waiting:
          response += serRiscureNano.read(1)
        if "Expected token" in response and "Press enter to retry" in response:
          idxToken = response.find("Expected token") + 16
          token = response[idxToken:idxToken+32]
          if token in d.keys():
            print ""
            print "Collision found for token", token
            print ""
            print "Next tokens are:"
            print "\n".join([t for t in d[token]])
            print ""
            collision = True
          else:
            fd.write(token + "\n")
            threetokens.append(token)
            if len(threetokens) == 3:
              d[threetokens[0]] = threetokens[1:]
              collect += 1
            printedToken = True
            response = ""

        if collision:
          break

    if collision:
      # This file should be empty, remove it
      os.unlink("collect_%08X.txt" % collect)

      for tok in d[token]:
        time.sleep(0.1)
        print "Replaying",
        serRiscureNano.write('\r')
        time.sleep(0.3)
        serRiscureNano.read_all()
        time.sleep(0.1)
        serRiscureNano.write(tok + '\r')
        time.sleep(0.1)
        flagresp = serRiscureNano.read_all()
        if "FLAG:" in flagresp:
          print flagresp
          break

      if "FLAG:" in flagresp:
        break


if __name__ == '__main__':
  main()
```
