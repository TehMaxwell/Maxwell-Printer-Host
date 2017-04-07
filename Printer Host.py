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
from PyQt4 import QtCore, QtGui
import time
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#A Class Designed to complete all base communications with the 3D Printer and to store base printer information
class printer():
    #Definitions
    #Serial Communication
    serial_wait_time = 0.1          #The amount of time to wait before attempting to read the printers response

    #Tracking Variables
    x = False       #A Variable to track the X Position of the Printer
    y = False       #A Variable to track the Y Position of the Printer
    z = False       #A Variable to track the Z Position of the Printer
    
    #Constructor, generates a new object of the Printer Class with default values
    def __init__(self, com_port, baud_rate):
        #Creating a Boolean to Track whether the code executed successfully or not
        code_successful = True
        
        #Attempting to establish Serial Communication with the Printer
        try:
            #Establishing Serial Communication with the device
            self.port = serial.Serial(port = com_port, baudrate = baud_rate)
            
            #Flushing the Input Buffer to remove any remaining information that may have been previously recieved
            self.port.flushInput()
            
            #Flushing the Output Buffer to remove any remaining information that may have previously failed to send
            self.port.flushOutput()
        
        #Serial access Error
        except serial.SerialException:
            #Printing an Error Message to the Console
            print "Failed to connect to the Printer, Serial Communications could not be initialised."
            
            #Setting Code successful to False to indicate that a Serial Error Occured
            code_successful = False
        
        #Returning the Code Successful Boolean to indicate whether the function executed correctly or not
        return code_successful
        
    #Method used to send a line of GCode to the Printer
    def send_line(self, gcode):
        #Creating a Boolean to Track whether the code executed successfully or not
        code_successful = True
        
        #Attempting to Send a Gcode Line to the Printer
        try:
            #Flushing the Serial Output Buffer to ensure that no residual data is sent with the Gcode line
            self.port.flushOutput()
            
            #Sending the GCode Line Over the Serial Port to initialise a Printer Action
            self.port.write(gcode)
            
            #Generating a Variable to Temporarily store the Printers Reply
            printer_reply = ""
            
            #Flushing the Serial Input Buffer to ensure that no residual data is read with the Printers Reply
            self.port.flushInput()
            
            #Pausing to allow the Printer to Respond
            time.sleep(self.serial_wait_time)
            
            #While there is information remaining in the Serial Input Buffer
            while self.port.inWaiting() > 0:
                #Reading the next byte of information from the Serial Port
                byte = self.port.read(1)
                
                #Appending the byte to the variable storing the Printers Reply String, this builds the reply string byte by byte
                printer_reply += byte
            
            #Getting the Length of the Printers Reply
            length_printer_reply = len(printer_reply)
            
            #If there was no response from the Printer
            if length_printer_reply == 0:
                #Setting the Code Successful Boolean to False to indicate that the GCode line failed to send
                code_successful = False
            
        #Serial access Error
        except serial.SerialException:
            #Printing an Error Message to the Console
            print "Failed to send GCode line due to Serial Communications error."
            
            #Setting the code successful Boolean to indicate that a Serial Error occured
            code_successful = False
        
        #Returning the Printers Reply and the Code Successful Variable to indicate whether the function executed correctly or not
        return printer_reply, code_successful

#A Class Designed to complete all GCode File Interactions
class gcode_file():
    #Method used to open the GCode File at the given Filepath
    def open_file(self, gcode_filepath, access_type):
        #Creating a Boolean to track whether the function executes correctly or not
        code_successful = True
        
        #Attempting to Open the GCode File
        try:
            #Opening the File with the given file path and access type
            new_file = open(gcode_filepath, access_type)
            
            #Updating the Classes current file with the new file
            self.current_file = new_file
        
        #File Access Error
        except IOError:
            #Printing an Error Message to the Console
            print "Failed to open GCode file."
            
            #Setting the code successful variable to False to indicate that a File access Error Occured
            code_successful = False
        
        #Returning the code successful boolean to indicate whether not the function executed successfully
        return code_successful
            
    #Method used to close the currently opened file
    def close_file(self):
        #Creating a Boolean to track whether the function executes correctly or not
        code_successful = True
        
        #Attempting to Close the GCode File
        try:
            #Closing the current file
            self.current_file.close()
            
        #File access Error
        except IOError:
            #Printing an Error Message to the Console
            print "Failed to close GCode file."
        
            #Setting the code successful boolean to False to indicate that a File access error ocurred
            code_successful = False
        
        #Returning the code successful boolean to inidcate whether or not the function executed successfully
        return code_successful
        
    #Method used to read a given number of lines from the GCode File
    def read_gcode_lines(self, num_lines):
        #Creating a Boolean to track whether the function executes correctly or not
        code_successful = True
        
        #Attempting to Read the given number of lines from the Gcode File
        try:
            #Reading the given number of lines from the Gcode File
            gcode_lines = self.current_file.readlines(num_lines)
        
        #File access Error
        except IOError:
            #Printing an Error Message to the Console
            print "Failed to read lines from the GCode file."
            
            #Setting the code successful boolean to False to indicate that a File access error ocurred
            code_successful = False
        
        #Returning the Lines read from the GCode File and the code successful boolean to indicate whether or not the function executed successfully
        return gcode_lines, code_successful
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MAIN CODE
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------