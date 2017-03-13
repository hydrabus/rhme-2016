# rhme-2016 write-up Emergency Transmitter

<a name="emergencytransmitter"></a>
## Emergency Transmitter (Other - 500 pts)

*Emergency transmitter* is an interesting challenge in that it requires multiple skills, the most important one being understanding fault injection and most likely Differential Fault Analysis on AES for the final step (there are likely other ways to solve the challenge, but we were not successful). A cryptographic background therefore helps.

The principle of the challenge is that we input a value to the board, which then blinks an LED. The description on the RHme2 website clearly indicates that we will be dealing with an encryption, that we can check by comparing two outputs (the one from the board against the one we are expecting based on the key we have recovered). First, we need to get this output, and as the LED is the only interaction the board has with us, we will study its blinking pattern.

A look at an Arduino Nano schematics shows that there are four LEDs, one for power, one for RX, one for TX and a last one which is bound to the value on pin D13. We hooked up two Arduinos, a first one to interact with the RHme2 board over a serial connection and send a trigger signal to a second Arduino, which constantly monitored the state of D13. Timings are extremely important in such situations as you want to have an accurate count of events, so we avoided monitoring the LED from a PC or a Raspberry Pi. In the end, we would have on one side a hexadecimal value sent to the board, on the other side a data structure equivalent to a sequence of zeros and ones matching the LED blinking pattern.

Next, this sequence needs to be turned into something useful, which means determining the smallest transmission unit, checking that all other transmission patterns are a multiple of this unit, and getting back to a digital value. It turned out that there were only two kinds of patterns at a high state (ie LED on). Interpreting this as Morse code gives you the output value, a 32-character long hexadecimal string.

Now that we can read our output, the next step is to observe the behaviour of the challenge. First, the input length matters:
- if you provide twice the same input and it is shorter than 16 bytes, you get different outputs
- if you provide twice the same input and it is 16-byte long, you get identical outputs

Next, we experimented with empty inputs: after a reset, if you simply press Enter, you will get an identical output every time. The good point is that everything is deterministic, no random number generation is involved.

A more interesting observation is the following one:
1. collect a first output for whatever input and write it down
2. then get another output by just pressing Enter (empty input) and write it down
3. now use the *first output* as an *input*, you will get the second output again

It means that the same buffer is used for input and output. It hints at a much more useful property: if this actually is the state buffer of the algorithm, where all the intermediate states are written to at some point, we can try to introduce a perturbation in the algorithm execution. We can think of injecting a glitch to change a value or skip part of a copy loop, but is actually much simpler here (similar to a whitebox setup): just send data during the execution of the algorithm to the board, you'll control precisely what value you are replacing the internal state with.

We can also now explain the behaviour with short messages: a part of the previous output was reused as we only overwrote part of it, and our actual input size is 16 bytes.

We have three more steps to take:
- think of an attack path
- determine when to inject our modification
- run the attack

Based on the input and output sizes, we made an educated guess that we were dealing with an AES128. This algorithm has this nice property that if you inject a fault at the proper time and location, you will get a recognizable [*differential pattern*](https://www.cryptologie.net/article/169/differential-fault-analysis/). So with this hypothesis in mind, we tried looking for a delay, after inputting our plaintext, that would generate such a differential pattern, and if possible in a reliable way.

To have a reliable delay for the injection, we set up another Arduino which acted as a serial gateway between a PC and the target. We measured the global execution time of the algorithm, took some margin to cover the two last rounds and sent just one byte to change the first intermediate state byte, progressively incrementing our delay. When we saw the expected differential pattern, we knew we were close to breaking the challenge as DFA was clearly on the table.

We considered another attack, though. The final AES operation is an AddRoundKey, ie an XOR. If we can reset the internal state to all zeros right before it, then the output will be the last round key. We'd have to invert the key schedule to get back to the main key and be done quickly. We didn't manage to get our flag this way, though, so we went back to DFA.

Each useful fault injection for a DFA will give you information for 1/4th of the last round subkey. We already knew how to fault the first byte, but we also had to change the second, third and fourth ones. For this, we determined what the actual value was for the first byte, by bruteforcing it and looking for a *safe error*: we inject a fault, which has no effect on the output, yielding the actual value. We then injected the safe error value for the first byte and a faulty second byte, and repeated the process to collect DFA information for all byte positions.

To recover the last round subkey and invert the key schedule to finally get the AES key, you can have a look at [SideChannelMarvels](https://github.com/SideChannelMarvels).
