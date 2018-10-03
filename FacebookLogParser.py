# Created by: MyCjel Venegas
# Created on: 8/28/2018
# Last Updated: -
# Revision: 1.1 (TESTING)
# --------------------Facebook Log Parser------------------------
# FacebookLogParser.py is for searching through multiple files in
# a directory and comparing them to a specified reference file for
#                             key values


import os
import sys
import string
import platform
import argparse
import logging
import datetime
import re

system = platform.system()

# sets the date structure for the "myLog" function
now = datetime.datetime.now()

crtdate = "{0}-{1}-{2}".format(now.year,now.month,now.day)

# finds the Current Working Directory (cwd) for path and log storage
cwd = os.getcwd()

# finds a log file to use as a reference for comparison
n = 1
for root, dirs, files in os.walk(cwd, topdown=False):
    for fileA in files:
        if n == 1:
            if fileA.find("LOG") != -1:
                dfltref = os.path.join(root,fileA)
                n = n + 1
            else:
                pass
        else:
            pass

# setup for argparse variables for 'reference', 'filepath', and 'variable'
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reference", 
                    action='store',
                    dest='ref',
                    type=str,
                    nargs="?",
                    default=dfltref,
                    help="Reference file for parsing")
parser.add_argument("-f", "--filepath",
                    action='store',
                    dest='folder',
                    type=str,
                    nargs="?",
                    default=cwd,
                    help="Path that you want compare.Default is current path")
parser.add_argument("-v", "--variable",
                    action='store',
                    dest='var',
                    type=str,
                    nargs="?",
                    default="",
                    help="Log search item for comparison")

arg = parser.parse_args()

main = arg.ref
fileP = arg.folder 
srch = arg.var

# logging configurations for script
log = "ParserLog_{}-{}.log".format(crtdate,srch)

logging.basicConfig(filename=log,format='%(message)s',level=logging.INFO)

# reads lines and creates a dictionary of log parameters and values while filtering for empty line space
def createMasterDict(ref):
    masterDict = {}
    with open(ref) as f_line:
        # this section is used for filtering out empty lines found in the log files
        lines = (line.rstrip() for line in f_line)
        filelines = (line for line in lines if line)
        # this section is used for compiling the lines into a (parameter):(value) dictionary
        for line in filelines:
            line = line.strip().lower()
            key, val = line.split(":", 1)
            masterDict[key] = val
    return masterDict

# takes input string and adds to log while printing in the terminal
def myLog(text):
    logging.info(text)
    print text

# takes the log files that meet qualification to this point and
# compares their values to find if there are variances
def parseCompare(main,compare,path,srch):
    # takes full path log files and uses createMasterDict() to create dictionary values for them
    comp = os.path.join(path,compare)
    mainlines = createMasterDict(main)
    complines = createMasterDict(comp)
    # filters files to make sure that only log files that are comprable are compared
    key = mainlines.keys()
    if len(mainlines) == len(complines):
        for k in key:
            if k.find(srch) == -1:
                pass
            else:
                if mainlines[k] == complines[k]:
                    pass
                elif mainlines[k].find("namespace-id") != -1:
                    pass
                elif mainlines[k] > complines[k]:
                    myLog("-----------------------------------------------------\n")
                    myLog("\nFile ({})'s value for\n'{}'\nis LESS than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    myLog("------------------------")
                elif mainlines[k] < complines[k]:
                    myLog("-----------------------------------------------------\n")
                    myLog("\nFile ({})'s value for\n'{}'\nis GREATER than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    myLog("------------------------")
                elif mainlines[k] != complines[k]:
                    print("INVALID PARAMETER: '{}'".format(k))
    elif len(mainlines) > len(complines):
        myLog("Check Shows Less in {}".format(comp))
    elif len(mainlines) < len(complines):
        myLog("Check Shows Greater in {}".format(comp))
    else:
        myLog("Check is not Good in {}".format(comp))

# goes through all sub directories of the selected folder*
# to find logs to compare to your reference file**
# with the option of a key parameter*** being compared
def pathCycle(mainfile,path,var):
    myLog("\n\n****Reference File: {}****\n\n".format(mainfile))
    for root, dirs, files in os.walk(path, topdown=True):
        for fileA in files:
            myLog("\n\n-----------------------------------------------------")
            myLog("\nFor files in root directory:\n{}\n".format(root))
            if fileA.find("LOG") != -1:
                comp = os.path.join(root,fileA)
                with open(mainfile) as main:
                    with open(comp) as com:
                        if len(main.readlines()) == len(com.readlines()):
                            parseCompare(mainfile,fileA,root,var)
                        elif len(main.readlines()) != len(com.readlines()):
                            print "Parameter '{}' not found in file:\n{}".format(var,fileA)
                        else:
                            myLog("UNEXPECTED EVENT OCCURRED")
            else:
                myLog("\n\nFile {} does not match expected file name\n\n".format(fileA))


if __name__ == "__main__":
    pathCycle(mainfile=main,path=fileP,var=srch)
    print("\n\n/////////////////////////////////////////////////")
    print("***For log of output check:***\n{}\{}".format(cwd,log))
    print("/////////////////////////////////////////////////")

# *   = no file selected results in your current working directory being default
# **  = no refererence file selected results in random file selected
# *** = no parameter selected results in all parameters being compared