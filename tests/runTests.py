
import os
import sys
import argparse
import subprocess
import StringIO
import contextlib
import traceback
import logging


from kraken.log import getLogger

failedTests = []
updatedReferences = []


def checkTestOutput(filepath, output, update, printoutput=False):
    referencefile = os.path.splitext(filepath)[0] + '.out'
    referencefileExists = os.path.exists(referencefile)
    match = False
    if referencefileExists:
        referenceTxt = str(open(referencefile).read())
        match = (referenceTxt == output)

    if not referencefileExists or update:
        if not match:
            with open(referencefile, 'w') as f:
                f.write(output)

                if referencefileExists:
                    print "Reference Updated:" + referencefile
                else:
                    print "Reference Created:" + referencefile

            updatedReferences.append(referencefile)

        else:
            print "Reference is Valid:" + referencefile
    else:
        if match:
            print "Test Passed:" + filepath
        else:
            print "Test Failed:" + filepath
            resultfile = os.path.splitext(filepath)[0] + '.result'
            with open(resultfile, 'w') as f:
                f.write(output)

            failedTests.append(filepath)

    # TODO: Print out a diff between the output and the previous result.
    if printoutput:
        print output


def runPytonTest(filepath, update, printoutput):

    def format_exception(e):
        krakenPath = os.environ['KRAKEN_PATH']
        stack = traceback.format_tb(sys.exc_info()[2])
        newStack = []
        for line in stack:
            if 'runTests.py' in line:
                continue
            lineParts = line.split('"')
            if len(lineParts) >= 3:
                modulePath = os.path.normpath(lineParts[1])
                if modulePath.startswith(krakenPath):
                    lineParts[1] = os.path.relpath(modulePath, krakenPath)
                    line = '"'.join(lineParts)
            newStack.append(line)
        exception_list = []
        exception_list.extend(newStack)
        exception_list.extend(traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1]))

        exception_str = "Traceback (most recent call last):\n"
        exception_str += "".join(exception_list)
        # Removing the last \n
        exception_str = exception_str[:-1]

        return exception_str

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
            logger = getLogger('kraken')
            logger.setLevel(logging.DEBUG)

            for handler in logger.handlers:
                handler.setLevel(logging.DEBUG)

            execfile(filepath, {})
            output = s.getvalue()
        except Exception as e:
            print(format_exception(e))
            output = s.getvalue() + '\n'

    # Now remove all the output that comes from Fabric Engine loading...
    lines = output.split('\n')
    strippedlines = []
    for line in lines:
        if not line.startswith('[FABRIC'):
            strippedlines.append(line)

    output = '\n'.join(strippedlines)

    checkTestOutput(filepath, output, update, printoutput=printoutput)


def runKLTest(filepath, update, printoutput=False):
    cmdstring = "kl.exe " + filepath

    # Call the kl tool piping output to the output buffer.
    proc = subprocess.Popen(cmdstring, stdout=subprocess.PIPE)

    output = ""
    while True:
        line = proc.stdout.readline()
        if line != '':
            output += line.rstrip().replace("[FABRIC:MT] Ignored extension directory 'D:\\fabric\\FabricEngine-pablo-Windows-x86_64-20160216-102505\\Tests\\Exts': unable to open directory 'D:\\fabric\\FabricEngine-pablo-Windows-x86_64-20160216-102505\\Tests\\Exts': The system cannot find the path specified. (code 3 [0x3])", "")
        else:
            break

    checkTestOutput(filepath, output, update, printoutput=printoutput)


def runTest(filepath, update, printoutput=False):
    skipile = os.path.splitext(filepath)[0] + '.skip'
    if os.path.exists(skipile):
        print "Test Skipped:" + filepath
        return

    if filepath.endswith(".py"):
        runPytonTest(filepath, update, printoutput)
    elif filepath.endswith(".kl"):
        runKLTest(filepath, update, printoutput)


if __name__ == '__main__':
    # Parse the commandline args.
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=False, help="The python or kl File to use in the test (optional)")
    parser.add_argument('--update', required=False, action='store_const', const=True, default=False, help="Force the update of the reference file(s). (optional)")
    args = parser.parse_args()
    update = args.update

    if args.file is not None:
        filepath = args.file
        if not os.path.exists(filepath):
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.file)

        # wehn running a single test at a time, print the output to help with debugging.
        runTest(filepath, update, printoutput=True)
    else:
        testsDir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        for root, dirs, files in os.walk(testsDir):
            for filename in [name for name in files if name != 'runTests.py']:
                filepath = os.path.join(root, filename)
                runTest(filepath, update)

        if not update:
            if len(failedTests) > 0:
                print "======================================"
                print "FAILED TESTS"

                for filepath in failedTests:
                    print filepath
            else:
                print "======================================"
                print "ALL TESTS PASSED"
        else:
            if len(updatedReferences) > 0:
                print "======================================"
                print "UPDATED TESTS"

                for filepath in updatedReferences:
                    print filepath
