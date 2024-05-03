# 3D-Printer-to-AutoSprayer
## Introduction
This project is aimed at creating an affordable, accessible autosprayer by modifying your 3D printer. The process is non-destructive and you will retain the existing functionality of your 3D printer.

Taking it from [a boring 3D Printer](docs/Ender3V3SE.jpg) to [3D Printer + AutoSprayer](docs/finished_system.mp4):


This project was done using an Ender 3 V3 SE, the .stl files provided should therefore be adapted or replaced to suit your existing printer. But feel free to take inspiration from the designs. ;)

Speaking of inspiration: The idea for this project and some development was based off this original instructables article by user: Remi_Rafael so credit to them. <INSERT ORIGINAL INSTRUCTABLES>

## Quick-links
[System Requirements](#system-requirements)

[How does it work?](#how-does-it-work)

[How to set up](#how-to-set-up)

[Quick code breakdown](#the-code---what-does-it-do)


## System requirements
#### Expensive purchases :( 
* 3D printer
* Airbrush
* Compressor for airbrush
* Inks/Paints for airbrushing

#### Equipment you may already have on hand :)
* 2x Resistors in restistance ratio (<INSERT MY SPECIFIC ONES USED FOR ENDER 3 SYSTEM>)
* Arduino Uno (you can, of course, use whatever arduino you may have to hand, but the uno made it convenient with it's plethora of connections)
* 6xAA battery holder and (preferrably rechargeable) batteries (to power servo and circuit). If using an alternative method of powering the system, make sure it can handle the current draw of whatever servo you use. A simple USB will likely not be enough to power it.
* Servo motor (DS239-MG or equivalent) (<INSERT SPECIFIC ONE USED / SPECS>) 
* Heat-set threaded inserts and screws
* Cables
* Cable wrap for cable management

## How does it work?
#### Step 1 - Mounting the Airbrush
The airbrush is mounted onto the existing print-head using custom 3D printed models. To mount to the Ender 3 VS SE I used for the project, I chose to model a replacement print-head with a mount for the airbrush on the side. The .stl files for this printer are included.

#### Step 2 - Controlling Movement of the Print-Head/Airbrush
G-code is a widely used set of instructions used to control CNC machines and 3D printers. We can take advantage of G-code's existing functionality to do things like move the print head (and therefore the airbrush) to the position we desire. The instructions we take advantage of in this system can be found in the GCODE_writer class.

#### Step 3 - Controlling When/Where/What we Spray
We can take advantage of the parts-cooling fan in the printer in order to send a signal to our system telling us when, where and how much we want our airbrush to spray. This is a specific G-code instruction and sets our fan speeds between a range of 0 and 255, sending a different amount of voltage to the pins of the fan. By 'hijacking' this voltage and reading it using our arduino, we can send a signal to our servo motor telling it to turn a lot or a little, pulling the airbrush trigger back more or less respectively.

The circuit used for this is displayed below - both in schematic-form and in a simulator for the less electrically-inclined like myself.

## How to set up
You've got all the hardware, and you're ready to get spraying. How do you set all this up? (If you're using a CNC gantry or alternative printer to the Ender 3 V3 SE, there may be some additional trial and error with modeling and printing your own mounting hardware).
### Step 1 - Printing the mounting hardware
.stl files for the mounting hardware can be found in the models folder of this repository. First let's print the airbrush mount. There are 3 models to connect the airbrush to the print-head: a replacement print-head cover, an extended trigger to allow your servo to pull back the airbrush trigger, and a 'mate' to this print-head cover to hold the airbrush in place.

The models directory also contains a clip to mount your circuit to the frame of the Ender 3 V3 SE. A separate model is included which screws into the clip to hold an arduino uno and a battery. If you are using alternative hardware to an Arduino Uno, you can remodel this whilst still being able to use the clip provided. (The screw holes provided are M3).

I recommend test fitting all components now.

### Step 2 - Set up your circuit
I have provided a circuit schematic and diagram in the [section here](#step-3---controlling-whenwherewhat-we-spray).
For a picture of my assembled circuit, see below. My machine was only a prototype, so I didn't make any effort to permanently fix components in place. For longer-term use I would definitely recommend putting some effort into making it fit more compactly and robustly together (perhaps converting the circuit design into a PCB to make it more compact also).

It's important to note for the circuit to work that all ground connections must be linked (printer fan [next section], battery(/power supply), Arduino).

### Step 3 - Connect your circuit to your printer
To connect your circuit to the printer, we solder two leads from our circuit to the voltage and ground connections on the fan that is attached to the print-head.

If you are using a CNC 3D gantry or simply don't want to solder a connection to the fan on your printer. You can still use a button-controlled circuit to tell the circuit when to spray manually and achieve great results.

### Run the code
Load the relevant Arduino sketch onto your Arduino depending on if you're automated or button controlled spraying. You can then disconnect it if you wish as your battery/power supply can power the Arduino.

To run the ```spray_an_area.py``` script to generate ```.gcode``` to spray a desired area. You can run ```src/gcode_generation/spray_an_area.py``` with the following flags to specify the area you want to spray

```--start-position x y``` - sets the start position to `x` and `y`

```--spray-area w h``` - sets the dimensions of area to be sprayed to `w` (width) and `h` (height) in mm

```--destination filename``` - sets the destination filename of the .gcode file e.g. 'spray_an_area' -> `spray_an_area.gcode`

```--layers n``` - repeat for `n` layers

```--no-temp``` - do not set a target temperature or wait for temperature stabilisation

(```static_GCODE_script.py``` is also included, it takes no arguments and may be useful for debugging.)


### Step 5 - Testing
Now that your circuit is all connected, let's give it a test before we finish the assembly. Your printer's control software should have some way of manually turning on and off the fans on the print head like this on the Ender 3 V3 SE's menu (control->temperature->fans) pictured below.

When the fans are switched on you should see (and hear) your servo actuating to its 'spray' position. When the fans are switched off, you should see it return to its 'resting' position.

If you are using manually controlled spraying, add a button to your circuit and test that your servo activates when a button is pressed.

### Step 6 - Assembly and dry run
Your servo will be attached to the airbrush mounting hardware and will therefore have wires dangling down from the printer's frame. To tidy up these wires along with the leads connecting to the printer's fan, I highly suggest getting some cable wrap to route them all together and prevent unecessary strain on individual cables.

You can now load your airbrush onto your mounting hardware (without any ink loaded in the paint cup), with the extended trigger. Mount the servo as well and position the servo arm primed to push back the airbrush trigger.

Run the gcode_generation script ```spray_an_area.py``` with your desired spray area position and size. Load this onto your printer's SD card (or used networked printing options) and hit print.

You should see your print head strafe over your specified spray area and your servo should pull back the airbrush trigger at the start and end of each strafe.

You can use this opportunity to hone in your spraying dimensions.

### Step 7 - Mask your printer to protect from stray paint
Wait, wait, wait before you start spraying! Make sure you mask off your print bed, and the area around it to prevent getting paint on it.

If your printer has a magnetic print bed like the Ender 3 V3 SE, I would recommned getting a second one so you can hot-swap between spraying and printing more easily.

### Step 8 - Get creating!
You can create stencils using a laser or vinyl cutter (or masking) and now generate consistently sprayed images.
You could adapt my spraying code to spray patterns or images directly without requiring a stencil.
You can spray functional inks like I've done in my demo below to quickly generate functional prototypes on 3D printed objects.

If you do end up creating anything using this repo I'd love to see so please get in touch and show off what you've done!

## The Code - what does it do?
It can be a little overwhelming for some to dive into a repo and try and decipher what all the code does without a little extra explanation so I thought I'd provide that here:

There are two main components to the code provided. In the ```gcode_generation``` folder you will find code for a simple script to spray an even coat across a specific area as this was my goal for the project. (I used my 3D modeling software to create a mask on top of my print in the pattern for the circuit I wanted to make using sprayed functional inks). However the ```GCODE_writer``` class is provided and can be adapted or modified to spray more complex patterns or images. The ```spray_an_area.py``` python script contains arguments that are listed in the [relevant section](#run-the-code).

In the ```arduino_sketches``` folder you will find two very similar scripts with the purpose of controlling the activation of a servo. ```automatic_spray.py``` is an example script that controls the spraying automatically from aforementioned G-code instructions for turning the fan on-and-off. ```button_spray.py``` is an alternative example where spraying can be manually controlled by button-press in the event that alternative printers do not provide as easy access to fan control as with the Ender 3 VS SE (I assume most will as print-heads must be cooled somehow).

Lastly (for my research purposes) there is an evaluation script (```evaluation.py```) provided. This was used for evaluating the performance of the system with regards to applying an even coat of acrylic paint across an paper by seeing how much light passed through - which is important for my application of spraying functional inks to create circuits. You can very likely ignore this but I thought I would include it nonetheless.