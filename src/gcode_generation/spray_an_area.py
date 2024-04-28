import sys
import argparse

from dataclasses import dataclass  # Dataclass is used to define the Point class
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


# definition of the parameters. All dimentions are expressed in mm
START = Point(x=25, y=90)  # Coordinates of the center of the sample
# definition of the spraying parameter geometry
HATCH = 8  # distance between two spraying lines
SPRAY_HEIGHT = 80  # distance between the sample and the spray head
STAGE_TEMP = 50  # hotplate temperature in degree
FEEDRATE = 4800  # feedrate, displacement speed during spraying
LAYERS = 1  # number of layers to spray
LAYER_DELAY = 45  # Delay between two layers to let the water evaporate
SPRAY_DELAY_REFILL = 2  # Delay to refill cup
SPRAY_DELAY = 2  # Delay between two spray lines
SPRAY_AREA = Area(width=125, height=120)


parser = argparse.ArgumentParser(description="Spray an area")
parser.add_argument("--area", type=int, nargs="+", help="size of area to spray")
parser.add_argument("--layers", type=int, help="number of layers to spray")
parser.add_argument("--start", type=int, nargs="+", help="start point of spraying")
parser.add_argument("--output", type=str, help="output file name")
parser.add_argument(
    "--no-temp",
    action="store_true",
    help="do not set a target temperature or wait for temperature stabilization",
)
args = parser.parse_args()
print(args)

# HANDLE ARGUMENTS
if args.output:
    gcode = GCODE_writer(args.output + ".gcode")
else:
    gcode = GCODE_writer("area_spray.gcode")

if args.start:
    START = Point(x=args.start[0], y=args.start[1])

if args.area:
    SPRAY_AREA = Area(width=args.area[0], height=args.area[1])

if args.layers:
    LAYERS = args.layers

# Begining of the file
gcode.Set_Z_Max_F()
gcode.Set_Acc()

gcode.Home()
gcode.print_G1_line(
    0, 0, Z=SPRAY_HEIGHT, E=0, F=FEEDRATE
)  # move the bed to the designed height and set the feedrate

if not args.no_temp:
    gcode.Show("Waiting for the bed temperature to stabilize")
    gcode.Temperature(STAGE_TEMP)

iterations = SPRAY_AREA.height // HATCH

line_start = Point(x=START.x, y=START.y)


for i in range(LAYERS):
    for i in range(iterations):  # iterate over the number of lines needed to cover spray area
        gcode.Show(f"layer {i} ongoing")

        gcode.print_G1_line(line_start.x, line_start.y, SPRAY_HEIGHT)  # move to the starting point of line

        gcode.Delay(SPRAY_DELAY)
        gcode.Spray()

        gcode.print_G1_line(
            line_start.x + SPRAY_AREA.width, line_start.y, SPRAY_HEIGHT
        )  # move to the end of the line
        gcode.Stop_Spray()  # Stop the spray
        gcode.Delay(SPRAY_DELAY)

        line_start = Point(x=line_start.x, y=line_start.y + HATCH)

    gcode.Show("waiting for the ink to dry")
    gcode.Delay(LAYER_DELAY)  # wait after each layer for the ink to dry
gcode.HomeXY()  # Goes back to home position at the end of the spraying

gcode.Show("Code finished executing")
print("Code finished executing")
