"""Exception call by DVS Module"""

__author__ = "Saulquin Aurélie"
__copyright__ = ""
__credits__ = ["Saulquin Aurélie", "Boulet Pierre", "Elbez Hammouda"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Saulquin Aurélie"
__email__ = "clement.saulquin.etu@univ-lille.fr"
__status__ = "Available"


class NoMoreDataError(Exception):
    """
        Exception raise when dvs reader try to read data when reading head is at the end of file
    """

    def __init__(self, message="End of File reached, impossible to read more data"):
        self.message = message
        super(NoMoreDataError, self).__init__(self.message)


class UnvalaiblePositionError(Exception):
    """
        Exception raise when user ask to dvs read to positionning reading head before the begenning of datas or after the end of file
    """

    def __init__(self, pos, message="Position cannot be reached"):
        self.pos = pos
        self.message = message
        super(UnvalaiblePositionError, self).__init__("{} desired position {}".format(self.message, self.pos))