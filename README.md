# 3D-Printer-to-AutoSprayer
## Introduction
This project is aimed at creating an affordable, accessible autosprayer by modifying your 3D printer. The process is non-destructive and you will retain the existing functionality of your 3D printer.

<INSERT GIF OF DEMO>

This project was done using an Ender 3 V3 SE, the .stl files provided should therefore be adapted or replaced to suit your existing printer. But feel free to take inspiration from the designs. ;)

Speaking of inspiration: The idea for this project and some code developed was based off this original instructables article by user: Remi_Rafael so credit to them. <INSERT ORIGINAL INSTRUCTABLES>

## System requirements
#### Expensive purchases :( 
* 3D printer
* Airbrush
* Compressor for airbrush
* Inks/Paints for airbrushing

#### Equipment you may already have on hand :)
* Resistors (<INSERT MY SPECIFIC ONES USED FOR ENDER 3 SYSTEM>)
* Arduino
* 6xAA battery holder and (preferrably rechargeable) batteries (to power servo and circuit)
* Servo motor (<INSERT SPECIFIC ONE USED / SPECS>)
* Heat-set threaded inserts and screws

# How does it work?
#### Step 1 - Mounting the Airbrush
The airbrush is mounted onto the existing print-head using custom 3D printed models. To mount to the Ender 3 VS SE I used for the project, I chose to model a replacement print-head with a mount for the airbrush on the side. (Once again) The .stl files for this printer are included.

#### Step 2 - Controlling Movement of the Print-Head/Airbrush
G-code is a widely used set of instructions used to control CNC machines and 3D printers. We can take advantage of G-code's existing functionality to do things like move the print head (and therefore the airbrush) to the position we desire. The instructions we take advantage of in this system can be found in the GCODE_writer class.

#### Step 3 - Controlling When/Where/What we Spray
We can take advantage of the parts-cooling fan in the printer in order to send a signal to our system telling us when, where and how much we want our airbrush to spray. This is a specific G-code instruction and sets our fan speeds between a range of 0 and 255, sending a different amount of voltage to the pins of the fan. By 'hijacking' this voltage and reading it using our arduino, we can send a signal to our servo motor telling it to turn a lot or a little, pulling the airbrush trigger back more or less respectively.

The circuit used for this is displayed below - both in schematic-form and in a simulator for the less electrically-inclined like myself.

#### Step 4 - Profit
Sorry - I couldn't help myself


# Code - what does it do?
There are two main components to the code provided. In the *gcode_generation* folder you will find code for a simple script to spray an even coat across a specific area as this was my goal for the project. (I used masking to create the pattern for the circuits I wanted to make using sprayed functional inks). However the *GCODE_write*r class is provided and can be adapted or modified to spray more complex patterns or images.

In the *arduino_sketches* folder you will find two very similar scripts with the purpose of controlling the activation of a servo. *automatic_spray.py* is an example script that controls the spraying automatically from aforementioned G-code instructions for turning the fan on-and-off. *button_spray.py* is an alternative example where spraying can be manually controlled by button-press in the event that alternative printers do not provide as easy access to fan control as with the Ender 3 VS SE (I assume most will as print-heads must be cooled somehow).

Lastly (for my research purposes) there is an evaluation script (*evaluation.py*) provided. This was used for evaluating the performance of the system with regards to applying an even coat of ink across an acrylic sheet by seeing how much light passed through - which is important for my application of spraying functional inks to create circuits. You can very likely ignore this but I thought I would include it nonetheless.

# Demo
I wanted to build an end-to-end functional prototype with as much automation as possible. I built a simple model of an SNES-like controller, 3D printed it, masked it manually before spraying the masked model with a conductive ink. I then built a capacitive touch sensor using all the sprayed buttons. Using arduino keyboard emulation we can kick back and play some games now that work is done!