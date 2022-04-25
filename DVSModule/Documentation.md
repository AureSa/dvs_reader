# DVSModule Documentation

## class **DVSModule.dvs.DVSEvents**(file, camera, version, verbose=0)

A group of events from Dynamic Vision Sensor (DVS) file.

<u>Parameters</u>
   ----------

- **file** : String

        path of file who's contain the datas (required)

- **camera** : CameraFamily

        Type of camera which was used to write file (required)

- **version** : AERVErsion

        AER Version file 

- **verbose** : int

    print information (0 by default)
    - 0 : mute
    - 1 : file information
    - 2 : file header
    - 3 and more : datas





<u>Property</u>
   ---------- 

- **duration_s** : duration of video in second
- **duration_us** : duration of video in micro-second
- **start_s** : start time of video in second
- **start_us** : start time of video in micro-second
- **end_s** : end time of video in second
- **end_us** : end time of video in micro-second
- **height** : height of the video
- **width** : width of the video

<u>Methods</u>
   ------- 

- **getAllData()** : 

    read all file and return a numpy array of all data

    *Returns*
    -------
        numpy array of event_type data

        
- **getSingleData()** : 

    read just one data

    *Returns*
    -------
        event_type data


- **searchTime(time)** : 

    place reading head of reader on the first data where time event = time
    all next data will have an event time >= time

    *Arguments*
    ---------
        * time : desired time (required)


## class **DVSModule.dvs.DVSProcess(file, camera, version, read_type = ReadType.BLOC, channel_last = True, pool = (1, 1), verbose = 0)**

Group of event usable  by nengo simulator

Initialize reader class to read the file and parameter of video

<u>Parameters</u>
----------

- **file** : string, required

        path of file who's contain the datas

- **camera** : CameraFamily, required

        Type of camera which was used to write file

- **version** : AERVersion, required

        AER Version file

- **read_type** : ReadType, optional, ReadType.BLOC by default

    data recovery method
    - ReadType.BLOC : all data are readed and stored in memory
    - ReadType.FLOW : data are raeded one by one and are not stored in memory

- **channel_last** : bool, optional, True by default

    - if True, polarity is the least-significant index of data
    - if Flase, polarity is the most-significant index of data


- **pool** : (int, int), optional, (1, 1) by default

        Number of pixel to pool over in the vertical and horizontal direction respectevely

- **verbose** : int

    print information (0 by default)

        - 0 : mute
        - 1 : file information
        - 2 : file header
        - 3 and more : datas



<u>Property</u>
   ---------- 

- **dvsClass**: internal dvs class. Read Only. Use this attribute to get time information

```py
dvsNengo = DVSProcess(...)
start = dvsNengo.dvsClass.start_us
``` 

<u>Methods</u>
   ------- 

- **make_step(shape_in, shape_out, dt, rng, state)** : 

    Make the step function toi display the DVS events as image frame

    This function is call by nengo simulator

    *Returns*
    -------
        Function to create image frame depending time


## enum DVSModule.dvs.ReadType

<u>Attributes</u>
   ----------

- **BLOC** 

    The file is completely read and datas aree stored in memory

- **FLOW**

    The file is reading step by step. Datas are not stored in memroy


## Interface DVSModule.AERVersion.AERVersion

Only **ReadMode**, **AELen** (len of data in byte) and **FileExtension** depends to version
ReadMode depends to struct python library https://docs.python.org/3/library/struct.html 

Use this interface to add a new AER Version

<u>Property</u>
   --------

- **ReadMode** : 

    How to interpret byte readed. Depends to struct python library https://docs.python.org/3/library/struct.html

- **AELen** :
    
    Number of bytes to read

- **FileExtension** :

    File extension

### class DVSModule.AERVersion.AERV1

Version 1 of aer format

<u>Property</u>
   --------

- **ReadMode** : 

    `>HI` : Big endian, unsigned short, unsigned int

- **AELen** :
    
    6 : read 6 bytes

- **FileExtension** :

    .dat


### class DVSModule.AERVersion.AERV2

Version 2 of aer format

<u>Property</u>
   --------

- **ReadMode** : 

    `>II` : Big endian, unsigned int, unsigned int

- **AELen** :
    
    8 : read 8 bytes

- **FileExtension** :

    .aedat


## Interface DVSModule.DVSCamera.CameraFamily

CameraFamily interface is use to create a camera class with property use to get data from byte.
Data organization on file depends to camera and not to aer version

<u>Property</u>
   --------

- **Xmask** : 

    mask to get x coordinate

- **Xshift** :
    
    shift to put x to the correct position

- **Ymask** : 

    mask to get y coordinate

- **Yshift** :
    
    shift to put y to the correct position

- **Pmask** : 

    mask to get polarity

- **Pshift** :
    
    shift to put P to the correct position

- **Width** : 

    Number of pixel  in width

- **Height** :
    
    Number of pixel in Height

### class DVSModule.DVSCamera.DVS128

DVS128 camera

<u>Property</u>
   --------

- **Xmask** : 

    0x00fe

- **Xshift** :
    
    1

- **Ymask** : 

    0x7f00

- **Yshift** :
    
    8

- **Pmask** : 

    x01

- **Pshift** :
    
    0

- **Width** : 

    128

- **Height** :
    
    128


### class DVSModule.DVSCamera.DAVIS240

DAVIS240 camera

<u>Property</u>
   --------

- **Xmask** : 

    0x003ff000

- **Xshift** :
    
    12

- **Ymask** : 

    0x1fc0000

- **Yshift** :
    
    22

- **Pmask** : 

    0x800

- **Pshift** :
    
    11

- **Width** : 

    240

- **Height** :
    
    180


## class DVSModule.DVSException.NoMoreDataError(message="End of File reached, impossible to read more data")

Exception raise when dvs reader try to read data when reading head is at the end of file

<u>Parameters</u>
----------

- **message** : string, optional, default = "End of File reached, impossible to read more data"

        Message to print when error is raise


## class DVSModule.DVSException.UnvalaiblePositionError(pos, message="Position cannot be reached")

Exception raise when user ask to dvs read to positionning reading head before the begenning of datas or after the end of file


<u>Parameters</u>
----------

- **pos** : int, required

    position asked by users

- **message** : string, optional, default = "EPosition cannot be reache"

        Message to print when error is raise