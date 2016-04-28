"""Kraken Get Version Test

Get's the version of Kraken that is running. This simply tests if a valid
version string is returned.

"""

from kraken.core import getVersion


version = getVersion()
versionSplit = version.split('.')

has_suffix = False
if '-' in versionSplit[2]:
    has_suffix = True

suffix_split = None
if has_suffix is True:
    suffix_split = versionSplit[2].split('-')

# Split out suffix if present.
versionSplit = versionSplit[:2] + [suffix_split[0]]

# Tests if the 3 values are valid integers
print ','.join([type(int(x)).__name__ for x in versionSplit])
print len(versionSplit)