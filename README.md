# underlight
Python script running my LED strip at home with a Raspberry Pi

Requires `pigpiod`.
This code is mainly used with `shairport-sync`, at least in my case, by
```
shairport-sync -v -o stdout | auproc.py
```

Send data to port 2112 to change the LED's behavior. `doorlt` lights it up white for 1 minute then turns itself off. `hex_code` for RGB changes the light until further notice. If the latter is on, then `doorlt` has no effect.

Originally there is another thread monitoring audio (which is commented out, but is still in the code). However, the RPi2 starts to stutter if that while loop runs, so I had to comment it out. Bummer, but what can I do.

Change the red, green, and blue pins in `ledctrl.py`. Change the port listening in `auproc.py`.
