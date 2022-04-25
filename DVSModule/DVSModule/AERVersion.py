
__author__ = "Saulquin Aurélie"
__copyright__ = ""
__credits__ = ["Saulquin Aurélie", "Boulet Pierre", "Elbez Hammouda"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Saulquin Aurélie"
__email__ = "clement.saulquin.etu@univ-lille.fr"
__status__ = "Available"


class AERVersion:
    """
        AER Version Interface

        Only ReadMode, AELen (len of data in byte) and FileExtension depends to version
        ReadMode depends to struct python library https://docs.python.org/3/library/struct.html 

        Use this interface to add a new AER Version
    """

    @property
    def ReadMode(self):
        raise NotImplementedError

    @property
    def AELen(self):
        raise NotImplementedError

    @property
    def FileExtension(self):
        raise NotImplementedError


class AERV1(AERVersion):
    """ 
        Version 1 of aer format

        ReadMode = >HI : > big endian, H unsigned short, I unsigned long
        AELen = 6
        FileExtension = .dat
    """

    @property
    def ReadMode(self):
        return '>HI' # big endian, unsigned short, unsigned long

    @property
    def AELen(self):
        return 6

    @property
    def FileExtension(self):
        return ".dat"




class AERV2(AERVersion):
    """ 
        Version 2 of aer format

        ReadMode = >II : > big endian, I unsigned long, I unsigned long
        AELen = 8
        FileExtension = .aedat
    """

    @property
    def ReadMode(self):
        return '>II' # big endian, unsigned long, unsigned long

    @property
    def AELen(self):
        return 8

    @property
    def FileExtension(self):
        return ".aedat"
