import os
import re 
import sys 
import time 
import boto3
import json 
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# def taskchecker():
#     try:
REGION="us-east-2"
FUNCTIONNAME="HelloWorld"
FUNCTIONPYTHON="python3.7"
TOTALMEMORY=256
FUNCTIONTIMEOUT=120
client = boto3.client('lambda', region_name=REGION)
response = client.list_functions()        

def taskchecker():
    try:
        # Gets list of functions and assigns to LIST_OF_FUNCTION
        # I need to use for loop because I need to get the function name
        LIST_OF_FUNCTION = response["Functions"]
        for i in LIST_OF_FUNCTION:
            if FUNCTIONNAME in i.get("FunctionName"):
                print(bcolors.OKGREEN + "Function is created in %s " % REGION + bcolors.ENDC)
                time.sleep(0.5)
                MEMORISIZE = i.get("MemorySize")
                if TOTALMEMORY == MEMORISIZE:
                    print(bcolors.OKGREEN + "Function memory is correct" + bcolors.ENDC)
                    time.sleep(0.5)
                else:
                    print(bcolors.FAIL + "Function memory is not correct, it should be %s, please update by Function >> Configuration >> >> General Configuration" % TOTALMEMORY + bcolors.ENDC)
                    sys.exit(1)
                    time.sleep(0.5)
                NEWFUNCTIONTIMEOUT = i.get("Timeout")
                if FUNCTIONTIMEOUT == NEWFUNCTIONTIMEOUT:
                    print(bcolors.OKGREEN + "Function timeout is correct" + bcolors.ENDC)
                    time.sleep(0.5)
                else:
                    print(bcolors.FAIL + "Function timeout is not correct, it should be %s, please update by Function >> Configuration >> >> General Configuration" % FUNCTIONTIMEOUT + bcolors.ENDC)
                    sys.exit(1)
                    time.sleep(0.5)
                NEWRUNTIME = i.get("Runtime")
                if FUNCTIONPYTHON == NEWRUNTIME:
                    print(bcolors.OKGREEN + "Function runtime is correct" + bcolors.ENDC)
                    time.sleep(0.5)
                else:
                    print(bcolors.FAIL + "Function runtime is not correct, it should be %s, please update by Function" % FUNCTIONPYTHON + bcolors.ENDC)
                    sys.exit(1)
                    time.sleep(0.5)
        if FUNCTIONNAME not in i.get("FunctionName"):
            print(bcolors.FAIL + "Function is not created in %s " % REGION + bcolors.ENDC)
            sys.exit(1)
            time.sleep(0.5)
    except:
        print(bcolors.FAIL + "Something went wrong or you did the task in wrong region should be in %s, please redo the task" % REGION +  bcolors.ENDC)
        time.sleep(0.5)
        sys.exit(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

taskchecker()