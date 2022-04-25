__author__ = "Saulquin Aurélie"
__copyright__ = ""
__credits__ = ["Saulquin Aurélie", "Boulet Pierre", "Elbez Hammouda"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Saulquin Aurélie"
__email__ = "clement.saulquin.etu@univ-lille.fr"
__status__ = "Available"


class CameraFamily:
    """
        CameraFamily interface is use to create a camera class with property use to get data from byte
        Data organization on file depends to camera and not to aer version

        Required property are:
            - Xmask
            - Xshift
            - Ymask
            - Yshift
            - Pmask
            - Pshift
            - Width (pixel)
            - Height (pixel)
    """

    @property
    def Xmask(self):
        raise NotImplementedError

    @property
    def Xshift(self):
        raise NotImplementedError

    @property
    def Ymask(self):
        raise NotImplementedError

    @property
    def Yshift(self):
        raise NotImplementedError

    @property
    def Pmask(self):
        raise NotImplementedError

    @property
    def Pshift(self):
        raise NotImplementedError

    @property
    def Width(self):
        raise NotImplementedError

    @property
    def Height(self):
        raise NotImplementedError




class DVS128(CameraFamily):
    """
        DVS128 camera

        Camera property are:
            - Xmask = 0x00fe
            - Xshift = 1
            - Ymask = 0x7f00
            - Yshift = 8
            - Pmask = x01
            - Pshift = 0
            - Width (pixel) = 128
            - Height (pixel) = 128
    """


    @property
    def Xmask(self):
        return 0x00fe

    @property
    def Xshift(self):
        return 1

    @property
    def Ymask(self):
        return 0x7f00

    @property
    def Yshift(self):
        return 8

    @property
    def Pmask(self):
        return 0x1

    @property
    def Pshift(self):
        return 0 

    @property
    def Width(self):
        return 128

    @property
    def Height(self):
        return 128


class DAVIS240(CameraFamily):
    """
        DAVIS240

        Camera property are:
            - Xmask = 0x003ff000
            - Xshift = 12
            - Ymask = 0x1fc0000
            - Yshift = 22
            - Pmask = 0x800
            - Pshift = 11
            - Width (pixel) = 240
            - Height (pixel) = 180
    """

    @property
    def Xmask(self):
        return 0x003ff000

    @property
    def Xshift(self):
        return 12

    @property
    def Ymask(self):
        return 0x7fc00000

    @property
    def Yshift(self):
        return 22

    @property
    def Pmask(self):
        return 0x800

    @property
    def Pshift(self):
        return 11

    @property
    def Width(self):
        return 240

    @property
    def Height(self):
        return 180

    