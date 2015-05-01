"""Kraken Softimage Plug-in."""


def dccTest():
    try:
        import sipyutils

        return True

    except:
        return False