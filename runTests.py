

# Import system modules
import sys, string, os
import argparse
import subprocess
import StringIO
import contextlib


def checkTestOutput(filepath, output, update):
    referencefile = os.path.splitext(filepath)[0]+'.out'
    if not os.path.exists(referencefile) or update:
        with open(referencefile, 'w') as f:
            f.write(output)
            print "Reference Created:" + referencefile
    else:
        referenceTxt = str(open( referencefile ).read())
        if referenceTxt == output:
            print "Test Passed:" + filepath
            return True
        else:
            print "Test Failed:" + filepath
            resultfile = os.path.splitext(filepath)[0]+'.result'
            with open(resultfile, 'w') as f:
                f.write(output)


def runPytonTest(filepath, update):

    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    with stdoutIO() as s:
        try:
            execfile( filepath, {} )
            output = s.getvalue()
        except Exception as e:
            # Some tests raise exceptions
            output = s.getvalue()
            output += str(e)

    # Now remove all the output that comes from Fabric Engine loading...
    lines = output.split('\n')
    strippedlines = []
    for line in lines:
        if not line.startswith('[FABRIC'):
            strippedlines.append(line)
    output = '\n'.join(strippedlines)

    checkTestOutput(filepath, output, update)


def runKLTest(filepath, update):
    cmdstring = "kl.exe " + filepath

    # Call the kl tool piping output to the output buffer. 
    proc = subprocess.Popen(cmdstring,stdout=subprocess.PIPE)
    output = ""
    while True:
      line = proc.stdout.readline()
      if line != '':
        output += line.rstrip()
      else:
        break
    checkTestOutput(filepath, output, update)


def runTest(filepath, update):
    skipile = os.path.splitext(filepath)[0]+'.skip'
    if os.path.exists(skipile):
        print "Test Skipped:" + filepath
        return
    if filepath.endswith(".py"):
        runPytonTest( filepath, update )
    elif filepath.endswith(".kl"):
        runKLTest( filepath, update )


# Parse the commandline args.
parser = argparse.ArgumentParser()
parser.add_argument('--file', required=False, help = "The python or kl File to use in the test (optional)")
parser.add_argument('--update', required=False, action='store_const', const=True, default=False, help = "Force the update of the reference file(s). (optional)")
args = parser.parse_args()
update = args.update

if args.file is not None:
    if os.path.exists(args.file):
        runTest(args.file, update)
    else:
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.file)
        runTest(filepath, update)
else:
    testsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests')
    for root, dirs, files in os.walk(testsDir):
        for filename in files:
            filepath = os.path.join(root, filename)
            runTest(filepath, update)