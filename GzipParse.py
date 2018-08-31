# Created by: MyCjel Venegas
# Created on: 8/29/2018
# Last Updated: -
# Revision: 1.0
# -----------------------GZip Parse--------------------------
# GzipParser.py is for searching through multiple files in a
#            directory for a specified key item. 


import os
import sys
import gzip
import io
import platform
import string
import argparse
import logging

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--filepath",
                    action='store',
                    dest='folder',
                    type=str,
                    help="Path that you want search")
parser.add_argument("-v", "--variable",
                    action='store',
                    dest='var',
                    type=str,
                    help="Log search item search")

arg = parser.parse_args()

fileP = arg.folder
srch = arg.var

logging.basicConfig(filename="GzipParse.log",format='%(message)s',level=logging.INFO)

def readlines(chkfl,var):
    if chkfl.find(".gz") == -1:
        pass
    else:
        with gzip.open(chkfl, "rb") as fileA:
            print("\n\nLines recovered from:\n{}\n".format(fileA))
            print("------------------------------\n")
            logging.info("\n\nLines recovered from:\n{}\n".format(fileA))
            logging.info("------------------------------\n")
            f = io.BufferedReader(fileA)
            filelines = f.readlines()
            for lines in filelines:
                if lines.find(var) == -1:
                    pass
                elif lines.find(var) != -1:
                    print("\n\n{}".format(lines))
                    print("------------------------------")
                    logging.info("\n\n{}".format(lines))
                    logging.info("------------------------------")
        
                # else:
                #     print "invalid line grab"

def pathCycle(path,var):
    # path = "\\flsm-fs01\TDC1\RDT\RDT_Backup\XD5_4TB\MPT3000ENV01_XD5_ERDT_Backup_Midweek3_05312018"
    # path = "\\" + path
    print path
    logging.info(path)
    for root, dirs, files in os.walk(path, topdown=False):
        for fileA in files:
            # print fileA
            testfile = os.path.join(root,fileA)
            readlines(testfile,var)
    print("logs are saved in current directory under GzipParse.log")

            
if __name__ == "__main__":
    pathCycle(path=fileP,var=srch)