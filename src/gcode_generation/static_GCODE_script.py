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


# definition of the geometrical parameters. All dimentions are expressed in mm
# Number_Slides = 1                  # number of slides to coat at once
Center_area = Point(x=100, y=125)  # Coordinates of the center of the sample
Tool_offset = Position(x=0, y=50, z=0)  # offset of airbrush from the print head
# Orientation_Slide = 0              # direction of the slide's major dimention. 0 for X, 1 for Y
# Dimention_Slide = (75.5,25.5)       # dimention of one slide, major dimention first
# Positioning_uncertainty = 2         # imprecision on the slides positioning

# definition of the spraying parameter geometry
Spray_diameter = 23  # diameter of the spray mm
Hatch = 12  # distance between two spraying lines
Spray_height = 100  # distance between the sample and the spray head
Offest_Purging = 25  # distance from the coating area to begin spaying
# Number_layers = 40                 # Number of layers (ie scans)
Temperature_stage = 50  # hotplate temperature in degree
Feedrate = 4800  # feedrate, displacement speed during spraying
Time_delay = 10  # Delay between two layers to let the water evaporate

# Declaration of variables
Spray_height = Spray_height + Tool_offset.z

gcode = GCODE_writer("static_spray.gcode")

# Begining of the file
gcode.Set_Z_Max_F()
gcode.Set_Acc()
# File_handler.write(f"M140 S{Temperature}\n")
gcode.Home()
gcode.print_G1_line(
    0, 0, Z=Spray_height, E=0, F=Feedrate
)  # move the bed to the designed height and set the feedrate

gcode.print_G1_line(
    Center_area.x, Center_area.y, Spray_height
)  # move to the purging area
gcode.Show("Waiting for the bed temperature to stabilize")
gcode.Temperature(Temperature_stage)

for i in range(50):  # iterate over the number of layers
    gcode.Show(f"layer {i} ongoing")
    ### Implement suplementary movement
    gcode.Spray()
    gcode.Delay(5)
    gcode.Stop_Spray()  # Stop the spray
    gcode.Show("waiting for the ink to dry")

    gcode.Delay(Time_delay)  # wait after each layer for the ink to dry

gcode.HomeXY()  # Goes back to home position at the end of the spraying
# print (Coating_zone_dimention)                                 # Debug command to print the
gcode.Show("Code finished executing")
print("Code finished executing")
