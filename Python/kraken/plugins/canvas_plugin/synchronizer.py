from kraken.core.maths import Xfo, Vec3, Quat
from kraken.core.synchronizer import Synchronizer

class Synchronizer(Synchronizer):
    """The Synchronizer is a singleton object used to synchronize data between
    Kraken objects and the DCC objects."""

    def __init__(self):
        super(Synchronizer, self).__init__()


    # ============
    # DCC Methods
    # ============
    def getDCCItem(self, kObject):
        """Gets the DCC Item from the full decorated path.

        Args:
            kObject (object): The Kraken Python object that we must find the corresponding DCC item.

        Returns:
            object: The created DCC object.

        """

        path = kObject.getPath()

        return None


    def syncXfo(self, kObject):
        """Syncs the xfo from the DCC object to the Kraken object.

        Args:
            kObject (object): Object to sync the xfo for.

        Returns:
            bool: True if successful.

        """

        return False


    def syncAttribute(self, kObject):
        """Syncs the attribute value from the DCC objec to the Kraken object.

        Args:
            kObject (object): Object to sync the attribute value for.

        Returns:
            bool: True if successful.

        """

        return False

    def syncCurveData(self, kObject):
        """Syncs the curve data from the DCC object to the Kraken object.

        Args:
            kObject (object): object to sync the curve data for.

        Returns:
            bool: True if successful.

        """

        return False
