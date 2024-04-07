from pathlib import Path

class GCODE_writer:

    def __init__(self, file_name="Spray_scan.gcode"):    
        file_path = Path(file_name)
        # Create and/or open and overwrite the Gcode file
        self.file_handler = open(file_path,"w+")
        self.file_handler.write("(This Gcode is automatically generated to control the movement of a spray coater)\n\n")

    # Definition of the line wrighting functions
    def print_G1_line (self, X,Y,Z=-1,E=-1,F=4800):                   # write a movement line
        if(Z==-1 & E==-1):
            self.file_handler.write(f'G1 X{X} Y{Y}\n')
        elif(Z==-1):
            self.file_handler.write(f'G1 X{X} Y{Y} E{E}\n')
        elif(E==-1):
            self.file_handler.write(f'G1 X{X} Y{Y} Z{Z}\n')
        else:
            self.file_handler.write(f'G1 X{X} Y{Y} Z{Z} E{E} F{F}\n')    # The feedrate is only explicitely overwritten when all parameters are filled at the beginning of the file
    def Spray_ON (self):
        self.file_handler.write("M106 S255\n")                           # Turn ON the cooling fan (spray)
    def Set_Z_Max_F (self):
        self.file_handler.write("M203 Z800\n")
    def Set_Acc (self):
        self.file_handler.write("M201 X40000 Y40000\nM203 X5000\nM203 Y5000\n")
    def Spray_OFF (self):
        self.file_handler.write("M106 S0\n")                             # Turns OFF the cooling fan (spray)
    def Delay (self, Time):
        self.file_handler.write(f'G4 P{Time*1000}\n')                    # Delay the execution of folowing code for {Time} seconds
    def Home (self):
        self.file_handler.write("G28\n")
    def HomeXY (self):
        self.file_handler.write("G28 X0 Y0\n")
    def Show(self, str):
        self.file_handler.write(f'M117 [{str}]\n')
    def Temperature (self, Temperature, Offset=10):
        self.file_handler.write(f'M140 S{Temperature}\n')                # Set the bed target temperature
        self.file_handler.write(f'M190 S{Temperature - Offset}\n')       # Wait for the temparature to reach within {Offset} of the target temperature