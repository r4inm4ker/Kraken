# Kraken_Plugin

import win32com.client
from win32com.client import constants

si = Application
log = si.LogMessage


def XSILoadPlugin(in_reg):
    in_reg.Author = 'Eric Thivierge & Phil Taylor'
    in_reg.Name = 'Kraken_Plugin'
    in_reg.Major = 1
    in_reg.Minor = 0

    in_reg.RegisterCommand('OpenKrakenEditor', 'OpenKrakenEditor')
    #RegistrationInsertionPoint - do not remove this line

    return True

def XSIUnloadPlugin(in_reg):
    log(in_reg.Name + ' has been unloaded.', constants.siVerbose)

    return True


# =========
# Commands
# =========
def OpenKrakenEditor_Init( in_ctxt ):
    cmd = in_ctxt.Source
    cmd.Description = 'Opens the Kraken Editor'
    cmd.SetFlag(constants.siCannotBeUsedInBatch, True)
    cmd.ReturnValue = True

    return True


def OpenKrakenEditor_Execute(  ):



    return True
