# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 15:01:23 2017

@author: Sam

This is the main software file for the Maxwell Printer Host Application. The Maxwell Printer Host is a piece of software designed to
communicate with 3D Printers that run open source control firmware.
"""

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MODULES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
import serial
import sys
from PyQt4 import QtGui
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DEFINITIONS
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#A Class Designed to complete all base communications with the 3D Printer and to store base printer information
class printer():
    #Definitions
    
    #Tracking Variables
    x = False       #A Variable to track the X Position of the Printer
    y = False       #A Variable to track the Y Position of the Printer
    z = False       #A Variable to track the Z Position of the Printer
    
    #Constructor, generates a new object of the Printer Class with default values
    def __init__(self, com_port, baud_rate):
        #Establishing Serial Communication with the device
        self.port = serial.Serial(port = com_port, baudrate = baud_rate)
        
    #Method used to send a line of GCode to the Printer
    def send_line(self, gcode):
        try:
            #Sending the Line over the Serial Port
            self.port.write(gcode)
            
            #Generating a Variable to Temporarily store the Printers Reply
            printer_reply = ""
            
            #Waiting for the Printers Reply
            while self.port.inWaiting() > 0:
                #Reading the reply from the Printer
                byte = chr(self.port.read(1))
                
                #Adding the new byte to the Printer Reply String
                printer_reply += byte
            
            #If the printer did not give a reply, return an error
            if len(printer_reply) == 0:
                #Setting the Value of Printer Reply to the Empty Reply Error
                printer_reply = "No Reply"
            
            #Returning the Printers Reply
            return printer_reply
        #If a Serial Error Occurs, return an error
        except serial.SerialException:
            #Printing the Serial Error
            return "Serial Error"

#A Class Designed to complete all GCode File Interactions
class gcode_file():
    #Definitions
    
    #Tracking Variables
    
    
    #Constructor, generates a new object of the GCode File Class
    def __init__(self):
        #Passing the Constructor
        pass
    
    #Method used to open the GCode File at the given Filepath
    def open_file(self, gcode_filepath, access_type):
        #Opening the File with the given file path and access type
        new_file = open(gcode_filepath, access_type)
        
        #Updating the Classes current file with the new file
        self.current_file = new_file
        
    #Method used to read a given number of lines from the GCode File
    def read_gcode_lines(self, num_lines):
        #Reading the given number of lines from the Gcode File
        gcode_lines = self.current_file.readlines(num_lines)
        
        #Returning the Lines read from the GCode File
        return gcode_lines

#GUI Classes
#Application Class
class main_host_application(QtGui.QApplication):
    #Constructor, generates a new Maxwell Printer Host Application GUI
    def __init__(self):
        #Inheriting from the QApplication Class
        super(main_host_application, self).__init__()
        
        #Running the Main Event Handler Loop of the Application
        sys.exit(self.exec_())
    
#Main Window Class
class main_host_window(QtGui.QWidget):
    #Definitions
    window_title = "Maxwell Printer Host"

    #Tracking Variables
    
    #Constructor, generates a new Maxwell Printer Host Main Window
    def __init__(self):
        #Inheriting from the QWidget Class
        super(main_host_window, self).__init__()
        
        #Setting the Title of the Main Window
        self.setWindowTitle(self.window_title)
        
        #Setting the Geometry of the Main Window
        self.setGeometry(1000, 600)
        
        #Creating a Grid Layout for the Main Window
        glay = QtGui.QGridLayout()
        
        #
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MAIN CODE
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------