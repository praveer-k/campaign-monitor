#!/usr/bin/python3
import sys, subprocess

def main():
    if len(sys.argv) == 2:
      path = sys.argv[1]
      runnable = ["downloader.py","classifier.py","cleaning.py","modelling.py","diagnostics.py","report.py"]
      for afile in runnable:
        command = "python3 "+afile+" < "+path+"/input.in"+" > "+path+"/output.log"
        try:  
            retcode = subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)
            print("Successful !!!", retcode)
        except subprocess.SubprocessError as e:
            print("Execution failed:", e)
    else:
        print('Error! arguments less or more than 1')
main()
