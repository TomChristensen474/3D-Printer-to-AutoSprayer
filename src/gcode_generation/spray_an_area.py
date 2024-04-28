import sys
import argparse

from dataclasses import dataclass    # Dataclass is used to define the Point class
from GCODE_writer import GCODE_writer


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Position:
    x: int
    y: int
    z: int

@dataclass
class Area:
    width: int
    height: int

# definition of the geometrical parameters. All dimentions are expressed in mm
# Number_Slides = 1                  # number of slides to coat at once
START = Point(x=25, y=90)  # Coordinates of the center of the sample
# TOOL_OFFSET = Position(x=10, y=5, z=0)  # offset of airbrush from the print head
# Orientation_Slide = 0              # direction of the slide's major dimention. 0 for X, 1 for Y
# Dimention_Slide = (75.5,25.5)       # dimention of one slide, major dimention first
# Positioning_uncertainty = 2         # imprecision on the slides positioning

# definition of the spraying parameter geometry
SPRAY_DIAMGETER = 23  # diameter of the spray
HATCH = 8  # distance between two spraying lines
SPRAY_HEIGHT = 80  # distance between the sample and the spray head
PURGING_OFFSET = 25  # distance from the coating area to begin spaying
# Number_layers = 40                 # Number of layers (ie scans)
STAGE_TEMP = 50  # hotplate temperature in degree
FEEDRATE = 4800  # feedrate, displacement speed during spraying

LAYER_DELAY = 45  # Delay between two layers to let the water evaporate
SPRAY_DELAY_REFILL = 2  # Delay to refill cup
SPRAY_DELAY = 2  # Delay between two spray lines

SPRAY_AREA = Area(width=125, height=120)
# print(sys.argv)
# TODO parameterise
parser = argparse.ArgumentParser(description='Spray an area')
parser.add_argument('--area', type=int, nargs='+', help='size of area to spray')
parser.add_argument('--layers', type=int, help='number of layers to spray')
parser.add_argument('--start', type=int, nargs='+', help='start point of spraying')
args = parser.parse_args()
print(args)
LAYERS = 1

gcode = GCODE_writer('area_spray.gcode')
# Begining of the file
gcode.Set_Z_Max_F()
gcode.Set_Acc ()

# File_handler.write(f'M140 S{Temperature}\n') # can delete this

gcode.Home()
gcode.print_G1_line (0,0,Z=SPRAY_HEIGHT,E=0,F=FEEDRATE)               # move the bed to the designed height and set the feedrate 

gcode.Show("Waiting for the bed temperature to stabilize")
gcode.Temperature(STAGE_TEMP)

iterations = SPRAY_AREA.height // HATCH

line_start = Point(x=START.x, y=START.y)

for i in range(LAYERS):
    for i in range(iterations):                                             # iterate over the number of lines needed to cover spray area
        gcode.Show(f'layer {i} ongoing')
        
        gcode.print_G1_line(line_start.x, line_start.y, SPRAY_HEIGHT)         # move to the starting point of line
        
        gcode.Delay(SPRAY_DELAY)
        gcode.Spray()
        # gcode.Delay(1) # time for servo to activate
        gcode.print_G1_line(line_start.x + SPRAY_AREA.width, line_start.y, SPRAY_HEIGHT)  # move to the end of the line
        gcode.Stop_Spray()                                                 # Stop the spray
        gcode.Delay(SPRAY_DELAY)

        line_start = Point(x=line_start.x, y=line_start.y + HATCH)

    gcode.Show("waiting for the ink to dry")
    gcode.Delay(LAYER_DELAY)                                           # wait after each layer for the ink to dry
gcode.HomeXY()                                                        # Goes back to home position at the end of the spraying

gcode.Show("Code finished executing")
print ("Code finished executing")   