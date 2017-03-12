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
