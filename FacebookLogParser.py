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

# WIN=False
# LIN=False

# print os.path.abspath("monkey_no_hands.txt")

system = platform.system()

now = datetime.datetime.now()

crtdate = "{0}-{1}-{2}".format(now.year,now.month,now.day)

cwd = os.getcwd()

print cwd

# if os == "Linux":
#     LIN = True
# else:
#     WIN = True

# if WIN == True:
#     stnd = os.
# elif LIN == True:
#     stnd = "/root/danny/"

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--reference", 
                    action='store',
                    dest='ref',
                    type=str,
                    required=True,
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
                    print "\n\n-----------------------------------------------------"
                    print("\nFor files in root directory {}\n".format(path))
                    print "-----------------------------------------------------\n"
                    print("\nFile ({})'s value for\n'{}'\nis LESS than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    print "------------------------"
                    logging.info("\n\n-----------------------------------------------------")
                    logging.info("\nFor files in root directory {}\n".format(path))
                    logging.info("-----------------------------------------------------\n")
                    logging.info("\nFile ({})'s value for\n'{}'\nis LESS than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    logging.info("------------------------")
                elif mainlines[k] < complines[k]:
                    print "\n\n-----------------------------------------------------"
                    print("\nFor files in root directory {}\n".format(path))
                    print "-----------------------------------------------------\n"
                    print("\nFile ({})'s value for\n'{}'\nis GREATER than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    print "------------------------"
                    logging.info("\n\n-----------------------------------------------------")
                    logging.info("\nFor files in root directory {}\n".format(path))
                    logging.info("-----------------------------------------------------\n")
                    logging.info("\nFile ({})'s value for\n'{}'\nis GREATER than the reference.\n\nReference Value: {}\nComparison Value: {}".format(compare,k.upper(),mainlines[k],complines[k]))
                    logging.info("------------------------")
                elif mainlines[k] != complines[k]:
                    print "\n\n-----------------------------------------------------"
                    print("\nFor files in root directory {}\n".format(root))
                    print("INVALID PARAMETER: '{}'".format(k))
    elif len(mainlines) > len(complines):
        print("Check Shows Less in {}".format(comp))
        logging.error("Check Shows Less in {}".format(comp))
    elif len(mainlines) < len(complines):
        print("Check Shows Greater in {}".format(comp))
        logging.error("Check Shows Greater in {}".format(comp))
    else:
        print("Check is not Good in {}".format(comp))
        logging.error("Check is not Good in {}".format(comp))

def pathCycle(mainfile,path,var):
    for root, dirs, files in os.walk(path, topdown=True):
        for fileA in files:
            comp = os.path.join(root,fileA)
            with open(mainfile) as main:
                with open(comp) as com:
                    if len(main.readlines()) == len(com.readlines()):
                        print fileA
                        parseCompare(mainfile,fileA,root,var)
                    elif len(main.readlines()) != len(com.readlines()):
                        pass


if __name__ == "__main__":
    # parseCompare()
    pathCycle(mainfile=main,path=fileP,var=srch)
    print("\n\n---For log of output check:---\n{}\{}".format(cwd,log))
    print("---------------------------------------------------------")