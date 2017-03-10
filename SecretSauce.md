# rhme-2016 write-up Secret Sauce

<a name="secretsauce"></a>
## Secret Sauce (Other - 300 pts)

This challenge ask for a password so the idea was it is probably possible to recover it using a timing attack with the help of HydraBus which have ultra accurate timer (1/168Mhz resolution)

So the challenge was to write a dedicated hard realtime firmware in order to measure time of the answer after sending one character of the password + CR

It was required to characterize the jitter of the rhme2 in order to be sure the character is valid or not valid and after multiple tries the jitter was characterized to be less than 20 microsecond.

So if the time after a character exceed 20 microsecond we save this character as valid and continue with next character and so on until the recovery of the full password.

It is like magic and the password appear character after character ...

### Step1 Timing Attack on the Password
* Firmware on hydrabus => timing attack on password (with check of answer timing delta of 20us if char match)
The password is finally
```
TImInG@ttAkw0rk
```

### Step2 Break the True Random Nonce
Now we have a shell and if we hit enter we have
```
>
True Random Nonce:	18f486101aa689bfc19e414f1c937e7d
Encryption:					f2298ab31efcc2bffd3e96f66bbffd77
Input data to encrypt:
```

each time we hit enter we have a new value for True Random Nonce & Encryption

We have immediately say what "True Random Nonce" on a poor ATMEGA328P it is bullshit as it does not contains such hardware feature so what could be similar ;)

Let's check what we have some IO and some Analog Input pins => Bingo let's stick those Analog Pins to GND to check if that do something 
And Yes the True Random Nonce is now always locked to *66e94bd4ef8a2c3b884cfa59ca342b2e* when A3 is connected to GND (other Analog Pin are not used)

=> Set A3 to GND fix Random Nonce then we hit Enter and True Random Nonce:	66e94bd4ef8a2c3b884cfa59ca342b2e
If we check with google 66e94bd4ef8a2c3b884cfa59ca342b2e is in fact an aes test with
```
KEY=00000000000000000000000000000000
PT=00000000000000000000000000000000
CT=66E94BD4EF8A2C3B884CFA59CA342B2E
```

### Step3 Find the keystream of the 1st block as we see there is an XOR on the Input 
Example:
```
> 00000000000000000000000000000000
True Random Nonce:	66e94bd4ef8a2c3b884cfa59ca342b2e
Encryption:			a0f2a7e3ee00f9ade9737df39eb3f9a4 7e4eb43a09613049e46e9b7eb045543e f8e9fbab824b2f158ff790e2274b7ea4
30303030303030303030303030303030 XOR a0f2a7e3ee00f9ade9737df39eb3f9a4 => 90C297D3DE30C99DD9434DC3AE83C994
Keystream is 90C297D3DE30C99DD9434DC3AE83C994
```

Then go back to step 2 just hit enter to have 1st block and use the Keystream 90C297D3DE30C99DD9434DC3AE83C994 to find the flag
```
>
True Random Nonce:	66e94bd4ef8a2c3b884cfa59ca342b2e
Encryption:			0124e496bd8fe7bb2953807987fdab05
```
FLAG:
0124E496BD8FE7BB2953807987FDAB05 XOR 90C297D3DE30C99DD9434DC3AE83C994 => 91E6734563BF2E26F010CDBA297E6291
