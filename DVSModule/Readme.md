# DVSModule 

DVSModule allows to read aer data file and get event from this file.

Two different classes can be use for dvs data manipulation.

**DVSEvents** class is a event group from Dynamic Vision Sensor (DVS) file.
This class just enough to read file and get data from file.

**DVSProcess** class is a event group from ear file and usable by nengo simulator.
This class read file, gets data and gives these data to nengo simulator.

There are also two interfaces.

**AERVersion** : use to define property of an aer version. 

aer properties are:
- Read Mode : how reader will read data byte, depends to "struct" python library https://docs.python.org/3/library/struct.html
- AELen : how many bit the reader must read
- FileExtension : Extension of file, use to check if file given by user and aer version are compatible


**CameraFamily** : use to define camera data property. These properties will be use to parse byte data to X,Y,Pol data.

Camera properties are:
- Xmask 
- Xshift
- Ymask
- Yshift
- Pmask
- Pshift
- Width
- Height


## How to use

### DVSevents

```py
    from DVSModule.dvs import *

    aer_version = AERV1()
    camera = DVS128()

    dvs_event = DVSEvents("path/to/file.dat", camera, aer_version, verbose=3)

    # to get all data
    all_data = dvs_event.getAllData()

    # or just read one data step by step
    data = dvs_event.getSingleData()

    # get duration of video
    dur_s = dvs_event.duration_s
    dur_us = dvs_event.duration_us

    # to start data retrieval at a specific time
    dvs_event.searchTime(5000000) # 5.000.000 us = 5s
    e= dvs_event.getSingleData() # e is the first event  which has event time >= 5s

```

### DVSProcess

```py
    from DVSModule.dvs import *

    aer_version = AERV1()
    camera = DVS128()

    dvs_proc = DVSProcess("path/to/file.dat", camera, aer_version, read_type = ReadType.FLOW, and some other option)

    nengo.Node(dvs_proc) # give process to nengo simulator
```

DVSProcess class has two different options to read and give data.

ReadType.BLOC : all data will be read and stored in memory
ReadType.FLOW : data will be read step by step and only useful data will be stored in memory and clear after use.

### AER data file version

Version 1 and 2 are available.

You can add a version with AERVersion interface.

```py
    from DVSModule.AERVersion import AERVersion

    class NewVersion(AERVersion):

        @property
        def ReadMode(self):
            return ...

        @property
        def AELen(self):
            return ...

        @property
        def FileExtension(self):
            return ...
```

### DVS Camera

Actually, the data from DVS128 and DAVIS240 are supported.

To add a new camera, use CameraFamily interface

```py
    from DVSModule.DVSCamera import CameraFamily

    class NewCamera(CameraFamily):

        @property
        def Xmask(self):
            return ...

        @property
        def Xshift(self):
            return ...

        @property
        def Ymask(self):
            return ...

        @property
        def Yshift(self):
            return ...

        @property
        def Pmask(self):
            return ...

        @property
        def Pshift(self):
            return ...

        @property
        def Width(self):
            return ...

        @property
        def Height(self):
            return ...
```

For more information see examples folder

## Installation

- Go on DVSModule folder : **dvsevent/DVSModule/**
- type : **pip install .**