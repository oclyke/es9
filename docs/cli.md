# usage

```bash
bazelisk run //es9:cli -- <args>

run //es9:cli -- hpf 0x03 # set high-pass filter for channel pairs 1-2 and 3-4

bazelisk run //es9:cli -- serve --port "ES-9 MIDI In" # start a server listening on the ES-9 MIDI In port

bazelisk run //:config_es9 # run a one-off configuration script
```

# development

Note: weird things seem to happen when you have multiple instance of stereo linked inputs assigned to the same mixer, or in strange orders.

Maybe worth precluding this possibility at a high level in the UI.

E.g. if inputs 1/2 are linked AND Mixer 1 is set up with these input sources:
- 1: Input 1
- 3: Input 2
- 4: Input 3
- 5: Input 2
- 6: Input 1
- 7: Input 2
- 7: Input 1
- 8: Input 3

Then:
- channel 7 cannot be changed to Input 2
- attempting to set channel 7 to Input 2 actually makes channel 8 into Input 2 and blasts away the previous Input 3 setting
- channel 5 cannot be changed to Input 1


The behaviour is beginning to make more sense now...
Stereo linked inputs have a L/R order, and the channels of a mixer also have L/R affinity.
I.e. 
ch1: L
ch2: R
ch3: L
ch4: R
ch5: L
ch6: R
ch7: L
ch8: R

And for the Input 1/2 linked pair:
Input 1: L
Input 2: R

So, if you try to assign a member of a linked pair to a channel with the "wrong" affinity the ES-9 firmware will automatically set it and its make to the linked pair

E.g.

try to set ch4: (R) to Input 1 (L) => ES-9 sets ch4: Input 2 (R) and ch3: Input 1 (L)

```bash
bazelisk query ...   # list all targets

bazelisk run //:requirements.update # update requirements_lock.txt from requirements.in
```

# testing

```bash
bazelisk run //:requirements_test
```
