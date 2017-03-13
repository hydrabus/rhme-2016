# rhme-2016 write-up Animals

<a name="animals"></a>
## Animals (Exploit - 200 pts)
You can select 1 of the 3 animals to display an ASCII art (cat, dog, mouse).<br>
First test, we sent dog+aaaaaaaaaa...(many times) until a memory dump.<br>
After analysing these bytes, we can understand that they correpond to a table
with different addresses (+ some parameters) used to display the picture.<br>
We can change the current selection by modifying the 2 bytes just after the 
overflow.<br>
Whatever, we can see & verify the following addresses associations:<br>
cat = 0x015e<br>
dog = 0x0158<br>
mouse = 0x0152<br>
??? =  0x014c (yeah)<br>
Replaced the last address is not enough, we need to set a kind of offset
defined by the next 2 bytes..<br>
After few tries, we got the following payload with python:
``` python
from rhme_serial import *

s = rhme_serial()
print s.xfer("dogaaaaaaaaaaaaaaaaa\x4c\x01\x6b\x03\r\n")
s.close()
```
and got the flag of course !
