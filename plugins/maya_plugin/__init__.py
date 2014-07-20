

def dccTest():
    try:
        from maya import cmds

        return True

    except:
        return False