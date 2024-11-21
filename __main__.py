"""rivtlib

rivtlib is generally run in an IDE. When run from the command line within the
file folder:

    python -m rivtlib rivtnn-filename.py

where *rivtnn-* is a rquired prefix for report organization and *nn* is an
integer. See **rivt User Manual** at https://rivt.info for details.

The code base uses a last letter naming convention for indicating variable
types where: 

A = array 
B = boolean 
C = class instance 
D = dictionary 
F = float 
I = integer 
L = list 
P = path 
S = string

"""
__version__ = "a.b.c"
__author__ = "rhholand"

import sys
import getopt

if sys.version_info < (3, 8):
    sys.exit("rivtlib requires Python version 3.8 or later")


def main(argv):
    """process command line arguments"""

    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is ', inputfile)
    print('Output file is ', outputfile)


def cmdlinehelp():
    """command line help"""

    print()
    print("Run the following command in folder with a rivt file:           ")
    print()
    print("     python -m rivtlib rivddff-filename.py                  ")
    print()
    print("The command is run in the rivt file folder.                ")
    print("File name must match 'rivddff-filename.py                  ")
    print("Where ff are dd are two digit integers.                    ")
    print("Text output is written to stdout.                          ")
    print("Other outputs depend on file contents.                     ")
    print("See User Manual at https://rivt-doc.net for details        ")
    sys.exit()


if __name__ == "__main__":
    try:
        argfileS = sys.argv[1]
        import rivtlib.rivtapi
    except:
        cmdlinehelp()
