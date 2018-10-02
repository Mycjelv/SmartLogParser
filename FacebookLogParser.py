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

now = datetime.datetime.now()

crtdate = "{0}-{1}-{2}".format(now.year,now.month,now.day)

cwd = os.getcwd()

print cwd

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

log = "ParserLog_{}-{}.log".format(crtdate,srch)

logging.basicConfig(filename=log,format='%(message)s',level=logging.INFO)

def createMasterDict(ref):
    masterDict = {}
    with open(ref) as f_line:
        lines = (line.rstrip() for line in f_line)
        filelines = (line for line in lines if line)
        for line in filelines:
            line = line.strip().lower()
            key, val = line.split(":", 1)
            masterDict[key] = val
    
    return masterDict

def myLog(text):
    logging.info(text)
    print text


def parseCompare(main,compare,path,srch):
    comp = os.path.join(path,compare)
    mainlines = createMasterDict(main)
    complines = createMasterDict(comp)
    key = mainlines.keys()
    if len(mainlines) == len(complines):
        for k in key:
            if k.find(srch) == -1:
                pass
            else:
                if mainlines[k] == complines[k]:
                    pass
                elif mainlines[k] > complines[k]:
                    myLog("\n\n-----------------------------------------------------")
                    myLog("\nFor files in root directory {}\n".format(path))
                    myLog("-----------------------------------------------------\n")
                    myLog("\nFile ({})'s value for\n'{}'\nis LESS than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    myLog("------------------------")
                elif mainlines[k] < complines[k]:
                    myLog("\n\n-----------------------------------------------------")
                    myLog("\nFor files in root directory {}\n".format(path))
                    myLog("-----------------------------------------------------\n")
                    myLog("\nFile ({})'s value for\n'{}'\nis GREATER than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    myLog("------------------------")
                elif mainlines[k] != complines[k]:
                    print "\n\n-----------------------------------------------------"
                    print("\nFor files in root directory {}\n".format(path))
                    print("INVALID PARAMETER: '{}'".format(k))
    elif len(mainlines) > len(complines):
        myLog("Check Shows Less in {}".format(comp))
    elif len(mainlines) < len(complines):
        myLog("Check Shows Greater in {}".format(comp))
    else:
        myLog("Check is not Good in {}".format(comp))

def pathCycle(mainfile,path,var):
    for root, dirs, files in os.walk(path, topdown=True):
        for fileA in files:
            if fileA.find("LOG") != -1:
                comp = os.path.join(root,fileA)
                with open(mainfile) as main:
                    with open(comp) as com:
                        if len(main.readlines()) == len(com.readlines()):
                            myLog("\n\n****Reference File: {}****\n\n".format(mainfile))
                            parseCompare(mainfile,fileA,root,var)
                            print("\n\n---For log of output check:---\n{}\{}".format(cwd,log))
                            print("--------------------------------")
                        elif len(main.readlines()) != len(com.readlines()):
                            print "Parameter '{}' not found in file:\n{}".format(var,fileA)
            else:
                myLog("\n\nFile {} does not match expected file name\n\n".format(fileA))


if __name__ == "__main__":

    # parseCompare()
    pathCycle(mainfile=main,path=fileP,var=srch)
    # print "done"