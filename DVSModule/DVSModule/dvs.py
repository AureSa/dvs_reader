import os
import struct   # interpret bytes as packed binary data

import numpy as np
from nengo import Process
from enum import Enum

from DVSModule.DVSExceptions import *
from DVSModule.DVSCamera import *
from DVSModule.AERVersion import *

__author__ = "Saulquin Aurélie"
__copyright__ = ""
__credits__ = ["Saulquin Aurélie", "Boulet Pierre", "Elbez Hammouda"]
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Saulquin Aurélie"
__email__ = "clement.saulquin.etu@univ-lille.fr"
__status__ = "Available"

# define type for event
event_type = np.dtype(
    [ ("t", "u4"), ("x", "u2"), ("y", "u2"), ("p", "u1") ]
)

class ReadType(Enum):
    """ 

    Different type of reading method.

    BLOC : The file is completely read and datas aree stored in memory
    FLOW : The file is reading step by step. Datas are not stored in memroy

    """
    BLOC = 0
    FLOW = 1



class _DVSReader:
    """ Class who's read data in file.

    Attributes
    ----------

    * duration : duration of video stored on the file
    * position : position of reading pointer

    Methods
    -------

    * readAllFile() : read all dvs file and return all datas
    * readData() : read just the data pointed by reading head and return this data
    * place(pos)": place the reading head to read the data n° pos 

    """

    def __init__(self, file, camera, version, verbose = 0):
        """
            Initialize all parameter wich allow to read data

            Parameters
            ----------
            * file : string, required
                path of file who's contain the datas 
            * camera : CameraFamily, required
                Type of camera which was used to write file
            * version : AERVersion, required
                AER Version file 
            * verbose : int, 0 by default
                print information
                - 0 : mute
                - 1 : file information
                - 2 : file header
                - 3 and more : datas
        """

        if not isinstance(camera, CameraFamily):
            raise TypeError("camera must be an instance of CameraFamily interface")

        if not isinstance(version, AERVersion):
            raise TypeError("version must be an instance of AERVersion")


        if file == None:
            raise ValueError

        self._verbose = verbose

        # file informations
        self._filePath = file
        self._fileInfo = None

        self._aerDataFile = None    # file ref

        self._fileLen = None # size of file

        # mask to recover data
        self._xmask = camera.Xmask
        self._xshift = camera.Xshift

        self._ymask = camera.Ymask
        self._yshift = camera.Yshift

        self._pmask = camera.Pmask
        self._pshift = camera.Pshift

        # reading information
        self._readMode = version.ReadMode 

        self._aeLen = version.AELen

        self._lineNum = None # actual line
        self._posPtr = None  # position of reader on file

        self._headerLen = 0

        self._initRead(version.FileExtension)    # get information of datas

        # data information
        self._duration = None # duration of video stored in file*

        self._start = None 
        self._end = None

        self._getDuration()

    @property
    def duration(self):
        """
            duration of the video stored in file
        """
        return self._duration

    @property
    def startTime(self):
        """
            data start time
        """

        return self._start

    @property
    def endTime(self):
        """
            data end time
        """

        return self._end

    @property
    def position(self):
        """
            position of reading head according to data numerotation and not byte numerotation 
        """
        return int( (self._posPtr-self._headerLen)/self._aeLen )


    def _initRead(self, ext):
        # Open file and get informations about data in this file
                
        # file extension check
        if not str(self._filePath).endswith(str(ext)):
            actual_ext = str(self._filePath).split('.')[-1]
            raise ValueError("Wrong file extension. Actual file extension .{0}. Excepted extension {1}".format(actual_ext, ext))


        # open file
        try:
            self._aerDataFile = open(self._filePath, 'rb')
        except FileNotFoundError as e:
            raise FileNotFoundError(e)


        # get file informations
        self._fileInfo = os.stat(self._filePath)
        self._fileLen = self._fileInfo.st_size


        self._lineNum = 0 # line number
        self._posPtr = 0  # pointer, position on bytes

        if self._verbose > 0:
            print("file size : ", self._fileLen)

        if self._verbose >= 2:
            print("Header : ")

        # get header information (v1: no head information)
        lt = self._aerDataFile.readline()
        while lt and lt[0] == '#':
            self._posPtr+=len(lt)
            self._lineNum += 1
            lt = self._aerDataFile.readline()
            if self._verbose >= 2:
                print("- ", str(lt))


        self._headerLen = self._posPtr


        if self._verbose >=1 :
            print("mask information : ")
            print("- xmask :\t", self._xmask)
            print("- xshift:\t", self._xshift)
            print("- ymask:\t", self._ymask)
            print("- yshift:\t", self._yshift)
            print("- pmask:\t", self._pmask)
            print("- pshift:\t", self._pshift)




    def _getDuration(self):
        # duration = time of the last data - time of the first data 
        
        buff = np.empty(1, dtype=event_type)

        self._aerDataFile.seek(self._fileLen-self._aeLen)
        s = self._aerDataFile.read(self._aeLen)
        buff = self._parse(s)

        self._end = int(buff['t'])

        self._aerDataFile.seek(self._posPtr)
        s = self._aerDataFile.read(self._aeLen)
        buff = self._parse(s)

        self._start = int(buff['t'])

        self._duration = self._end - self._start



    def _parse(self, s):
        # convert bytes read into understable data

        buff = np.empty(1, dtype=event_type)

        addr, ts = struct.unpack(self._readMode, s)
        hex(ts)
        hex(addr)

        x_addr = (addr & self._xmask) >> self._xshift
        y_addr = (addr & self._ymask) >> self._yshift
        a_pol = (addr & self._pmask) >> self._pshift

        if self._verbose >= 3:
            print("t -> ", ts)
            print("x -> ", x_addr)
            print("y -> ", y_addr)
            print("p -> ", a_pol)
            print("\n")

        buff['t'] = ts
        buff['x'] = x_addr
        buff['y'] = y_addr
        buff['p'] = a_pol
        
        return buff

    
    def _read(self):
        # read bytes and actualize the reader position 

        self._aerDataFile.seek(self._posPtr)
        s = self._aerDataFile.read(self._aeLen)
        self._posPtr += self._aeLen

        return s


    def readAllFile(self):
        """
            Read all data on file

            Returns
            -------
                numpy array list of all event (dtype=event_type)
        """

        array_size = int((self._fileLen-self._headerLen) / self._aeLen )
        buff = np.empty(1, dtype=event_type)
        events = np.empty(array_size, dtype=event_type)

        cpt = 0

        # read all data
        while (self._posPtr < self._fileLen):    
            s = self._read()
            
            events[cpt] = self._parse(s)

            cpt += 1
        

        if self._verbose > 0:
            try:
                print ("read %i (~ %.2fM) AE events, duration= %.2fs" % (len(events), len(events) / float(10 ** 6), self.duration))
            except:
                print ("failed to print statistics")


        return events


    def readData(self):
        """
            Read just on data en return an event_type

            Returns
            -------
                data read in event_type format
        """
        
        buff = np.empty(1, dtype=event_type)

        if not (self._posPtr < self._fileLen):
            raise NoMoreDataError()

        s = self._read()
        buff = self._parse(s)
        return buff



    def place(self, pos):
        """
            Place reader pointer to read data at the position "pos"

            Note :  the position is not depending to byte position but depending to data numerotation
                    for example, if header len is 0, data n°2 is at the byte n°12

            Parameters
            ----------
                * pos : position of data
        """

        p = pos*self._aeLen

        if p > self._fileLen or p < self._headerLen:
            raise ValueError("no data on this position")
        
        self._posPtr = p
        self._aerDataFile.seek(p)


    




class DVSEvents:
    """
        A group of events from Dynamic Vision Sensor (DVS) file.

        Attributes
        ----------

            * duration_s : duration of video in second
            * duration_us : duration of video in micro-second
            * start_s : start time of video in second
            * start_us : start time of video in micro-second
            * end_s : end time of video in second
            * end_us : end time of video in micro-second
            * height : height of the video
            * width : width of the video

        Methods
        -------

            * getAllData() : read all file and return a numpy array of all data
            * getSingleData() : read just one data
            * searchTime(time) : place reading head of reader on the first data where time event = time
        
    """

    def __init__(self, file, camera =DVS128(), version = AERV1(), verbose = 0):
        """
            Initialize reader class to read the file and parameter of video

            Parameters
            ----------

                * file : string, required
                    path of file who's contain the datas
                * camera : CameraFamily, DVS128 by default
                    Type of camera which was used to write file 
                * version : AERVersion, AERV1 by default
                    AER Version file 
                * verbose : int, 0 by default
                    print information 
                    - 0 : mute
                    - 1 : file information
                    - 2 : file header
                    - 3 and more : datas
        """


        if not isinstance(camera, CameraFamily):
            raise TypeError("camera must be an instance of CameraFamily interface")

        if not isinstance(version, AERVersion):
            raise TypeError("version must be an instance of AERVersion")

        self._height = camera.Height
        self._width = camera.Width


        self._reader = _DVSReader(file, camera, version, verbose)


        

    @property
    def duration_s(self):
        return self._reader.duration * 1e-6
    
    @property
    def duration_us(self):
        return self._reader.duration

    @property
    def start_us(self):
        return self._reader.startTime

    @property
    def start_s(self):
        return self._reader.startTime * 1e-6

    @property
    def end_us(self):
        return self._reader.endTime

    @property
    def end_s(self):
        return self._reader.endTime * 1e-6

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


    def getAllData(self):
        """
            read all file and return a numpy array of all data

            Returns
            -------
                numpy array of event_type data
        """
        return self._reader.readAllFile()

    
    def getSingleData(self):
        """
            read just one data

            Returns
            -------
                event_type data
        """
        return self._reader.readData()

    def searchTime(self, time):
        """
            place reading head of reader on the first data where time event = time
            all next data will have an event time >= time

            Arguments
            ---------
                * time : int, required
                    desired time 
        """


        # on cherche la position de début
        # position de début de récupération de données :
        # si evt_t et > t -> on déplace la tete de lecture en arrière jkusuq'a ce que evt_t < t
        # si evt_t < t -> on déplace la tete de lecture en avant jusqu'a ce que evt_t > t, puis on decremente la position
        # pour augmenter : on lis juste les données, le seek de readData va augmenter la position
        # pour diminuer : on prends posPtr et on fait -2 (le seek de readData va faire +1 -> +1-2 = -1)

        if time <= 0 or time > self.duration_s:
            return 

        #data = self.getData()
        evt_t = float(self.getSingleData()['t'])

        if evt_t < time:
            while evt_t < time:
                
                data = self._dvsReader.readData()

                if data is None:
                    return

                evt_t = float(data['t'])

            

        elif evt_t > time:
            while evt_t > time:
                
                try:
                    self._dvsReader.place(self._dvsReader.position-2)
                except ValueError:
                    return

                data = self._dvsReader.readData()

                if data == None:
                    return

                evt_t = float(data['t'])


        try:
            self._dvsReader.place(self._dvsReader.position-1)
        except ValueError:
            return




class DVSProcess(Process):
    """
        Group of event usable  by nengo simulator

        Attributes
        ----------

            * dvsClass: internal dvs class. Read Only
    """

    def __init__(self, file, camera = DVS128(), version = AERV1(), read_type = ReadType.BLOC, channel_last = True, pool = (1, 1), verbose = 0):
        """
            Initialize reader class to read the file and parameter of video

            Parameters
            ----------

                * file : string, required
                    path of file who's contain the datas

                * camera : CameraFamily, DVS128 by default
                    Type of camera which was used to write file

                * version : AERVersion, AERV1 by default
                    AER Version file

                * read_type : ReadType, optional, ReadType.BLOC by default
                    data recovery method
                    - ReadType.BLOC : all data are readed and stored in memory
                    - ReadType.FLOW : data are raeded one by one and are not stored in memory

                * channel_last : bool, optional, True by default
                    - if True, polarity is the least-significant index of data
                    - if Flase, polarity is the most-significant index of data
                
                * pool : (int, int), optional, (1, 1) by default
                    Number of pixel to pool over in the vertical and horizontal direction respectevely

                * verbose : print information (0 by default)
                    - 0 : mute
                    - 1 : file information
                    - 2 : file header
                    - 3 and more : datas
        """
        
        self._dvsEvents = DVSEvents(file, camera=camera, version=version, verbose=verbose)

        self._readType = read_type

        self.channel_last = channel_last


        self.height = int(np.ceil(self._dvsEvents.height / pool[0]))
        self.width = int(np.ceil(self._dvsEvents.width / pool[1]))

        self.polarity = 2
        self.size = self.height * self.width * self.polarity


        self.t_start = 0

        self.poolX = None
        self.poolY = None

        self.strideX = None
        self.strideY = None
        self.strideP = None

        self._initParser(pool)

        super().__init__(default_size_in=0, default_size_out=self.size)




    @property
    def dvsClass(self):
        """
            Function to get DVS classes to get information
        """
        return self._dvsEvents



    def _initParser(self, pool):
        # init stride value in function of channel_last

        self.poolY, self.poolX = pool

        if self.channel_last:
            self.strideX = self.polarity
            self.strideY = self.polarity * self.width
            self.strideP = 1
        else:
            self.strideX = 1
            self.strideY = self.width
            self.strideP = self.width * self.height




    def make_step(self, shape_in, shape_out, dt, rng, state):
        """
            Make the step function toi display the DVS events as image frame

            This function is call by nengo simulator

            Returns
            -------
                Function to create image frame depending time
        """

        assert shape_in == (0,)
        assert len(shape_out) == 1

        h = self.height
        w = self.width
        pol = self.polarity
        t_start = self.t_start

        # Bloc reading methods
        if self._readType == ReadType.BLOC:
            evt = self._dvsEvents.getAllData()

            if evt is None:
                raise ValueError("No event was has been read")

            event_t, event_id = self._parseEventBloc(evt)

            def blocStep(t):

                t = t_start + t
                t_lower = (t-dt) * 1e6
                t_upper = t * 1e6

                idxs = event_id[(event_t >= t_lower) & (event_t < t_upper)]

                image = np.zeros(h*w*pol)
                np.add.at(image, idxs, 1/dt)

                return image


            func = blocStep

        # flow reading methods
        elif self._readType == ReadType.FLOW:  

            def flowStep(t):

                t = t_start + t
                t_lower = (t-dt) * 1e6
                t_upper = t * 1e6


                ei = []

                self._dvsEvents.searchTime(t_lower)

                evt = self._dvsEvents.getSingleData()

                evt_t, evt_i = self._parseEventFlow(evt)

                while evt_t >= t_lower and evt_t < t_upper:
                    ei.append(evt_i)

                    evt = self._dvsEvents.getSingleData()

                    if evt is None:
                        break

                    evt_t, evt_i = self._parseEventFlow(evt)
                
                image = np.zeros(h*w*pol)
                np.add.at(image, ei, 1/dt)


                return image


            func = flowStep

        
        return func


    def _parseEventFlow(self, event):
        # parse only one event

        event_t = event['t']

        event_id = (
            (event['y'].astype(np.int32) // self.poolY) * self.strideY
            + (event['x'].astype(np.int32) // self.poolX) * self.strideX
            + event['p'].astype(np.int32) * self.strideP
        )
        
        return int(event_t), int(event_id)



    def _parseEventBloc(self, events):
        # parse all events

        events_t = events[:]["t"]

        events_ids = (
            (events[:]["y"].astype(np.int32) // self.poolY) * self.strideY
            + (events[:]["x"].astype(np.int32) // self.poolX) * self.strideX
            + events[:]["p"].astype(np.int32) * self.strideP
        )

        return events_t, events_ids
