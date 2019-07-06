#!/usr/bin/env python
from __future__ import print_function

template = "comsolJob.pbs"    # Name of the template submission file
check = "check.pbs"             # Name of checking job script
errorMessage = "Could not obtain license for COMSOL Multiphysics" # Error message to check for

def main():
    import argparse
    import os.path
    import time

    parser = argparse.ArgumentParser(description='submit comsol job to TORQUE system')
    parser.add_argument("filename", type=str, help="Accepts names w/ or w/o the '.mph' ending")
    parser.add_argument("-d", "--delay", default=0, type=int, help="Delay time for job resubmission [min]")
    parser.add_argument("-t", "--tries", default=0, type=int, help="Max # tries for resubmission")
    parser.add_argument("-r", "--removePBS", action="store_true", help="Removes PBS job submission scripts")
    parser.add_argument("-nc", "--noCheck", action="store_true", help="Don't submit checking job to queue")
    parser.add_argument("-c", "--check", action="store_true", help="Should be called only after the initial job has been run")
    args = parser.parse_args()

    # args.filename should accept arguments both w/ and w/o '.mph'
    filename = noExt(args.filename,".mph")

    if (args.tries < 0):
        print("Out of resubmission attempts")
        return
    else:
        triesLeft = args.tries - 1

    # args.check should be called only after the initial job has been run
    if (args.check):
        # Parse for error message
        if errorMessage in open(filename+"_output.txt").read():
            # Resubmit job if needed (with delay period)
            print("License error message found")
            time.sleep(args.delay * 60)
            # remove output file to avoid rereading the same error message twice
            os.remove( filename+"_output.txt" )
            os.remove( filename+"_error.txt" )
            print("Comsol job resubmitted\n")
            submitToQueue(filename, template, check, args, triesLeft)
            return

        # If no error, quit
        print("The comsol job ran without a license issue")
        print("[resubmission attempts left: ", triesLeft, "]")

        # Clean up more stuff
        os.remove( filename+"_error.txt" )
        os.remove( filename+"_check_error.txt" )
        return

    submitToQueue(filename, template, check, args, triesLeft)

    return

# Removes the extension name from a filename if present
def noExt(filename, extensionName):
    if filename[-len(extensionName):].find(extensionName) != -1:
        return filename[:-len(extensionName)]
    return filename

# Creates "outfile". Words from "infile" are replaced according to the dictionary, "replacements"
def copyReplace(inName, outName, replacements):
    with open(inName) as infile, open(outName, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():    #use iteritems() for python 2, items() for python 3
                line = line.replace(src, target)
            outfile.write(line)
    return

def submitToQueue(filename, template, check, args, triesLeft):
    import os.path
    import subprocess

    # First check if required files exist
    if not os.path.isfile(filename + ".mph"):
        print("Error: Cannot find " + filename + ".mph")
        return
    if not os.path.isfile(template):
        print("Error: Cannot find " + template)
        return
    if not os.path.isfile(check):
        print("Error: Cannot find " + check)
        return

    # Make new file template_FILENAME.pbs
    replacements = {'$FILENAME':filename}
    comsolPBS = filename + ".pbs"
    copyReplace(template, comsolPBS, replacements)

    # Submit comsol job
    # The last 4 characters are ".s1\n", I just want the job ID
    comsolJob = subprocess.check_output(["qsub", comsolPBS])[:-4]

    # Make new file check_FILENAME.pbs
    replacements = {'$FILENAME':filename, '$TRIESLEFT':str(triesLeft), '$DELAY':str(args.delay), '$COMSOL_JOB':str(comsolJob)}
    checkPBS = noExt(check,".pbs") + "_" + filename + ".pbs"
    copyReplace(check, checkPBS, replacements)

    # Submit checking job
    if not args.noCheck:
        checkingJob = subprocess.check_output(["qsub", checkPBS])[:-4]
    else
        checkingJob = "(Checking job not submitted)"
    print("Job numbers: ", comsolJob, ", ", checkingJob)

    if args.removePBS:
        print("Cleaning up PBS scripts")
        os.remove( comsolPBS )
        os.remove( checkPBS )
    return

if ( __name__ == '__main__' ):
    main()
