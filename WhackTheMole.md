# rhme-2016 write-up Whack The Mole

<a name="whackthemole"></a>
## Whack The Mole (Other - 200 pts)

This challenge was funny as the purpose was to set the right rhme2 digital pin(from D2 to D13) to "1" corresponding to number of flash detected on the LED(so counting number of rising edge on the LED pin/D13) in order to hit the mole.

So the challenge was to find how many flash corresponds to which pin.
After multiple test with a beta firmware I have characterized the limit like what is the maximum number of flash... so I have wrote the following rules.

The rules:
* Pin is checked(valid for a pulse count) if COM returns `You missed it. Try again by pressing <Enter>.` in less than 100ms
 * In that case it was required to send `\r` to try again
* Pin is ignored(invalid) if COM returns `You missed it. Try again by pressing <Enter>.` in more than 6s
 * In that case it was required to send `\r` to try again
* Pin is ON for the right Dx pulse count COM returns `Great job. You whacked it. Only XX more to go.`
* Pin from D2 to D13 (A0 to A7 not used) are used as Input on rhme2 board
* When first mole is hit/found we obtain `Great job. You whacked it. Only 50 more to go.`
 * So it was required to hint 50 moles successively as else it restart
 * After each reset the rhme2 pin corresponding to number of LED flash was set randomly
 * When the mole is found the rhme2 continue automatically and blink the LED to hit/find the 2nd Mole and so on
 
The main challenge was to build a LED rising edge counter which returns as fast as possible number of flash when detecting no change(timeout) which means it was the last flash.
 * So the timeout was carefully characterized(after lot of logic analyzer capture on different steps as the firmware was accelerating/slowing a bit depending on how many mole was found) to 50ms + 1ms rhme2 Jitter.
 * If this timeout is too long it simplify returns "You missed it ..." randomly for example after 10 mole found/hit ...

The HydraBus firmware works in two steps:
* 1st Step Discovery (wtm_discovery)
  * Check each WTM PDx Input corresponding to nb pulse(nb rising edge) in order to discover all the combinations(nb pulse) corresponding to rhme2 Pin(from D2 to D13) until we find the 6 unique combinations (nb pulse corresponds to Dx) as after multiple check it was detected that the maximum number of pulse is 6 and of course we are using the rules described previously
  
* 2nd Step Solve the challenge (wtm_solve)
  * Solve by using each WTM PDx Input/Pin corresponding to nbperiod until 50 steps are solved

![Logic Analyzer Whack The Mole Solved](WhacTheMole_Solve_LA.png)

HydraBus UART debug output:
```
> wtm_run start
wtm_discovery start
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Timeout 1=PD2 nb=0
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 5=PD3 nb=0
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 3=PD3 nb=0
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 2=PD3 nb=1
Missed 4=PD4 nb=1
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 5=PD4 nb=1
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 1=PD4 nb=1
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 3=PD4 nb=2
Timeout 1=PD5 nb=2
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 1=PD6 nb=2
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 6=PD6 nb=2
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 6=PD6 nb=2
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 6=PD6 nb=2
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 4=PD6 nb=3
Missed 5=PD7 nb=3
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 6=PD7 nb=4
Timeout 5=PD8 nb=4
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 4=PD9 nb=4
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 6=PD9 nb=4
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 1=PD9 nb=4
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 5=PD9 nb=5
Timeout 5=PD10 nb=5
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 2=PD11 nb=5
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 3=PD11 nb=5
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 4=PD11 nb=5
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
Missed 5=PD11 nb=5
rx1='Ready?'
rx2='Get set!'
rx3='GO!'
OK 1=PD11 nb=6
wtm_discovery end
wtm_solve start
error=3 rx1=''
OK 3=PD4 solved=1
OK 5=PD9 solved=2
OK 1=PD11 solved=3
OK 5=PD9 solved=4
OK 1=PD11 solved=5
OK 6=PD7 solved=6
OK 3=PD4 solved=7
OK 4=PD6 solved=8
OK 4=PD6 solved=9
OK 2=PD3 solved=10
OK 1=PD11 solved=11
OK 5=PD9 solved=12
OK 3=PD4 solved=13
OK 1=PD11 solved=14
OK 4=PD6 solved=15
OK 1=PD11 solved=16
OK 3=PD4 solved=17
OK 6=PD7 solved=18
OK 1=PD11 solved=19
OK 5=PD9 solved=20
OK 3=PD4 solved=21
OK 6=PD7 solved=22
OK 3=PD4 solved=23
OK 3=PD4 solved=24
OK 3=PD4 solved=25
OK 6=PD7 solved=26
OK 4=PD6 solved=27
OK 6=PD7 solved=28
OK 1=PD11 solved=29
OK 2=PD3 solved=30
OK 3=PD4 solved=31
OK 1=PD11 solved=32
OK 1=PD11 solved=33
OK 4=PD6 solved=34
OK 6=PD7 solved=35
OK 3=PD4 solved=36
OK 6=PD7 solved=37
OK 3=PD4 solved=38
OK 5=PD9 solved=39
OK 6=PD7 solved=40
OK 2=PD3 solved=41
OK 3=PD4 solved=42
OK 6=PD7 solved=43
OK 4=PD6 solved=44
OK 2=PD3 solved=45
OK 5=PD9 solved=46
OK 3=PD4 solved=47
OK 2=PD3 solved=48
OK 6=PD7 solved=49
OK 1=PD11 solved=50
data flag:
We are most gratefull for your service.
Please take our most precious belonging.
FLAG:f17537dc5cafb93dbbe79ba4d2036f52
```
