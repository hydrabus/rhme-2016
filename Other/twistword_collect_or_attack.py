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
