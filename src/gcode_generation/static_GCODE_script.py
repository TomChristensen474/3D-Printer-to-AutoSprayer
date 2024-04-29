from dataclasses import dataclass  # Dataclass is used to define the Point class
from GCODE_writer import GCODE_writer
from math import ceil  # Ceil is used to calculate the number of line per scan
from pathlib import Path


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Position:
    x: int
    y: int
    z: int


# definition of the parameters. All dimentions are expressed in mm
START = Point(x=25, y=90)  # Coordinates of the center of the sample
# definition of the spraying parameter geometry
HATCH = 8  # distance between two spraying lines
SPRAY_HEIGHT = 80  # distance between the sample and the spray head
STAGE_TEMP = 50  # hotplate temperature in degree
FEEDRATE = 4800  # feedrate, displacement speed during spraying
LAYERS = 20  # number of layers to spray
LAYER_DELAY = 10  # Delay between two layers to let the water evaporate
SPRAY_DELAY_REFILL = 2  # Delay to refill cup
SPRAY_DELAY = 2  # Delay between two spray lines


gcode = GCODE_writer("static_spray.gcode")

# Begining of the file
gcode.Set_Z_Max_F()
gcode.Set_Acc()
# File_handler.write(f"M140 S{Temperature}\n")
gcode.Home()
gcode.print_G1_line(
    0, 0, Z=SPRAY_HEIGHT, E=0, F=FEEDRATE
)  # move the bed to the designed height and set the feedrate

gcode.print_G1_line(
    START.x, START.y, SPRAY_HEIGHT
)  # move to the purging area

for i in range(LAYERS):  # iterate over the number of layers
    gcode.Show(f"layer {i} ongoing")
    ### Implement suplementary movement
    gcode.Spray()
    gcode.Delay(5)
    gcode.Stop_Spray()  # Stop the spray

    gcode.Show("waiting for the ink to dry")

    gcode.Delay(LAYER_DELAY)  # wait after each layer for the ink to dry

gcode.HomeXY()  # Goes back to home position at the end of the spraying

gcode.Show("Code finished executing")
print("Code finished executing")
