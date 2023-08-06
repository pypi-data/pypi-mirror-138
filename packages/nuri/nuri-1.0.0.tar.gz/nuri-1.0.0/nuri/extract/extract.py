###############################################################################
# Copyright (c) 2018, Urban Magnetometry Group.
# Produced at the University of California at Berkeley.
# Written by V. Dumont (vincentdumont11@gmail.com).
# All rights reserved.
# This file is part of NURI.
# For details, see http://citymag.gitlab.io/nuri
# For details about use and distribution, please read NURI/LICENSE.
###############################################################################

# System
import glob
import math
import os
import re
import struct
import sys
import time
import zipfile
from datetime import datetime,timedelta,date
from itertools import combinations

# External
import astropy
import h5py
import numpy
from astropy.time import Time
from dateutil import tz
from gwpy.timeseries import TimeSeries
from scipy import signal

# Local
from ..utils import str2datetime,str2timestamp

def get_data(tmin=None,tmax=None,path=None,sensor=None,station=None,rate=None,scalar=True):
    """
    Extract time-series data from a range of dates. This function should also work to extract
    data from individual file. However, we recommend to use the corresponding function in such
    case. That is, :py:meth:`data_extractor` for Biomed data or :py:meth:`get_vmr_data`
    for TwinLeaf data.
    
    Parameters
    ----------
    tmin : :class:`str`
      Start timestamp of the target period.
    tmax : :class:`str`
      Final timestamp of the target period.
    path : :class:`str`
      Path to data repository or file. If repository, this method will execute the
      :py:meth:`data_lookup` function to identify the directory structure and look
      for suitable data files.
    sensor : :class:`str`
      Sensor manufacturer (``biomed`` or ``twinleaf``). If ``None``, Biomed sensor is assumed.
    station : :class:`int`
      Index of the station, 1 to 4.
    rate : :class:`int`
      Resampling rate at which data should be downsampled. If ``None``, the data are
      not downsampled. This parameter is used during the reading the of Biomed sensor
      axis data (see :meth:`read_axis` method) and the reading of the Twinleaf VMR
      sensor (see :meth:`get_vmr_data` method).
    scalar : :class:`bool`
      Type of output value. Default is the scalar magnitude among all directions.

    Returns
    -------
    data : :class:`gwpy.timeseries.timeseries.TimeSeries`
      Full extracted magnetic field time series.

    Examples
    --------
    >>> berkeley = nuri.get_data('2016-4-1','2016-4-2','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
    >>> print(berkeley)
    TimeSeries([49.28078686, 49.3740789 , 49.39699749, ...,
                49.23254931, 49.23953604, 49.23309161]
               unit: dimensionless,
               t0: 1459468800.0 s,
               dt: 1.0001736412571627 s,
               name: None,
               channel: None)
    """
    # Create dataset
    ext = path.split('.')[-1]
    if ext=='bin':
        dataset = [path]
        offset = 0
    else:
        # Convert input dates to readable format
        tmin = str2datetime(tmin)
        tmax = str2datetime(tmax)
        # Determine timing offset based on original file construction
        offset = 0 if sensor=='twinleaf' else data_offset(tmin,tmax,station)
        dataset = data_lookup(path.replace('\ ',' '),tmin,tmax,station,offset)
    # Retrieve the magnetic field data
    assert len(dataset)>0, 'No data file found. Abort.'
    if sensor=='twinleaf':
        data = get_vmr_data(dataset,rate)
    elif '-xx' in dataset[0]:
        data = data_extractor(dataset,offset,rate,sensor,scalar=scalar)
    else:
        data = data_extractor(dataset,offset,rate,scalar=scalar)
    return data

def data_lookup(path,tmin,tmax,station=None,offset=0):
    """
    Lookup available data files within target time period. If direct path
    to binary file provided, this will simply return a list with the given path as a
    single element. Alternatively, and if a specific time period is provided by the
    user, this function will look for either zip files from the Google drive directory
    structure (i.e. year/month/day/hour/station) or the customised architecture
    (i.e. station/).
    
    Parameters
    ----------
    path : :class:`str`
      Path to data file or repository
    tmin : :class:`datetime.datetime`
      Starting time in format YYYY-MM-DD-HH-MM
    tmax : :class:`datetime.datetime`
      Ending time in format YYYY-MM-DD-HH-MM
    station : :class:`int`
      Station number

    Returns
    -------
    dataset : :class:`list`
      List of paths to identified data files

    Examples
    --------
    >>> tmin = nuri.utils.str2datetime('2018-5-7')
    >>> tmax = nuri.utils.str2datetime('2018-6-4')
    >>> dataset = nuri.data_lookup(path='./MagneticFieldData',tmin=tmin,tmax=tmax,station=4)
    >>> print(len(dataset))
    672
    >>> print(dataset[0])
    MagneticFieldData/2018/5/7/0/NURI-station-04/2018-5-7_0-xx.zip
    """
    if station==None or tmin==None or tmax==None:
        print('Station, tmin and tmax must be defined. Abort.')
        quit()
    # Initialise dataset arrays
    zip_list,biomed_list,data_list = [],[],[]
    # Loop through all requested hours
    for date in numpy.arange(tmin+timedelta(seconds=offset),tmax+timedelta(seconds=offset),timedelta(hours=1)):
        # Convert date into readable datetime format
        date = date.astype(datetime)
        # Determine path to compressed timing binary file path from Google structure
        zip_path = '%s/%s/%s/%s/%s/NURI-station-%02i/'%(path,date.year,date.month,date.day,date.hour,station)+date.strftime("%Y-%-m-%-d_%-H-xx.zip")
        zip_list = check_continuity(zip_path,zip_list)
        # Determine customized path to timing binary file
        biomed_path = '%s/NURI-station-%02i/'%(path,station)+date.strftime("%Y-%-m-%-d_%-H-xx_time.bin")
        biomed_list = check_continuity(biomed_path,biomed_list)
        # Determine customized path to timing binary file
        data_path = '%s/NURI-station-%02i/'%(path,station)+date.strftime("%Y-%m-%d-%H_*.bin")
        data_list = check_continuity(data_path,data_list)
    # Select dataset
    dataset = zip_list if len(zip_list)>0 else biomed_list if len(biomed_list)>0 else data_list
    return dataset

def check_continuity(path,dataset):
    """
    Check if subsequent data file is found. This function is executed within the :meth:`data_lookup`
    method and is used to ensure that while looping over consecutive hours, data files are indeed
    found and added to the list. If no files are found, an error message is prompted.

    Parameters
    ----------
    path : :class:`str`
      Assumed path to next data file, the algorithm will check if file exists
    dataset : :class:`list`
      Most recent list of data file actually found so far and up to current searched date

    Returns
    -------
    dataset : :class:`list`
      Incremented list of data files found.
    """
    assert len(dataset)==0 or (len(dataset)>0 and len(glob.glob(path))>0), \
        "No file found for date %s"%re.split('\/|_',path)[-2]
    dataset += glob.glob(path)
    return dataset

def data_offset(tmin,tmax,station,add=False):
    """
    Determine UTC to local Local offset to be applied.
    
    Parameters
    ----------
    tmin : :class:`datetime.datetime`
      Starting time
    tmax : :class:`datetime.datetime`
      Ending time
    station : :class:`int`
      Station number
    output : :class:`bool`
      Offset value requested

    Returns
    -------
    offset : :class:`float`
      Offset time to match time in targeted filename

    Examples
    --------
    >>> tmin = nuri.str2datetime('2018-5-20')
    >>> tmax = nuri.str2datetime('2018-5-30')
    >>> offset = nuri.data_offset(tmin,tmax,station=4)
    >>> print(offset)
    14400.0
    """
    # Identifying the time zone
    utc_zone = tz.gettz('UTC')
    # Format input timestamp into UTC time
    utc_epoch = tmin.replace(tzinfo=utc_zone)
    # Get time in local California time
    local_epoch = utc_epoch.astimezone(tz.gettz('America/Los_Angeles'))
    # Calculate offset between UTC and PST timestamps
    utc2pst = datetime.utcoffset(local_epoch).total_seconds()
    # Consider UTC to PST offset if requested time is before fix date
    utc2pst = utc2pst if tmin<datetime(2017,12,7) else 0
    # Look-up table to identify station's location over time
    locations = numpy.array([[1,datetime(2015,11,1),datetime(2017,12,3),tz.gettz('America/Los_Angeles')],
                             [1,datetime(2017,12,3),datetime.max       ,tz.gettz('America/New_York')   ],
                             [2,datetime(2015,11,1),datetime(2018,6,7) ,tz.gettz('America/Los_Angeles')],
                             [2,datetime(2018,6,7) ,datetime.max       ,tz.gettz('America/New_York'   )],
                             [3,datetime(2015,11,1),datetime(2017,10,6),tz.gettz('America/Los_Angeles')],
                             [3,datetime(2017,10,6),datetime.max       ,tz.gettz('America/New_York')   ],
                             [4,datetime(2015,11,1),datetime(2017,12,3),tz.gettz('America/Los_Angeles')],
                             [4,datetime(2017,12,3),datetime.max       ,tz.gettz('America/New_York')   ]])
    # Identify the location for requested data
    for n,start,end,loc in locations:
        if n==station and start<tmin<end:
            local_zone = loc
    # Identifying the time zone
    utc_zone = tz.gettz('UTC')
    # Format input timestamp into UTC time
    utc_epoch = tmin.replace(tzinfo=utc_zone)
    # Get time in local California time
    local_epoch = utc_epoch.astimezone(local_zone)
    # Calculate offset between Local and UTC timestamps
    utc2local = datetime.utcoffset(local_epoch).total_seconds()
    # Define offset to local time for new timing files
    offset = 0 if tmax<datetime(2016,6,10) else -utc2local
    return utc2pst-offset if add else offset

def data_extractor(dataset,offset=0,rate=None,sensor=None,scalar=True):
    """
    Retrieve data time series
    
    Parameters
    ----------
    rate : int
      Targeted sampling rate
    scalar : bool
      Type of output value, default is the scalar magnitude among all directions.
    
    Returns
    -------
    ts : gwpy.timeseries.TimeSeries
      Time series data, either scalar magnitude or for individual direction.
    """
    data_list = []
    if sensor=='biomed':
        t0 = numpy.array(re.split('\/|-xx',dataset[0]))[-2].replace('_','-')
        t1 = numpy.array(re.split('\/|-xx',dataset[-1]))[-2].replace('_','-')
        for filename in dataset:
            if filename.endswith('.zip'):
              zip_rep = zipfile.ZipFile(filename, 'r')
              zip_rep.extractall()
              zip_rep.close()
            # Extract data from X direction file
            xfile = filename.split('-xx')[0]+'-xx_rawX_uT_3960Hz.bin'
            x = read_axis(xfile.split('/')[-1],rate)
            # Extract data from Y direction file
            yfile = filename.split('-xx')[0]+'-xx_rawY_uT_3960Hz.bin'
            y = read_axis(yfile.split('/')[-1],rate)
            # Extract data from Z direction file
            zfile = filename.split('-xx')[0]+'-xx_rawZ_uT_3960Hz.bin'
            z = read_axis(zfile.split('/')[-1],rate)
            if filename.endswith('.zip'):
              os.system('rm *.bin')
            # Define 2D array
            imax = min(len(x),len(y),len(z))
            ts_data = numpy.vstack((x[:imax],y[:imax],z[:imax])).T
            data_list.append(ts_data)
    else:
        t0 = numpy.array(re.split('\/|_',dataset[0]))[-2]
        t1 = numpy.array(re.split('\/|_',dataset[-1]))[-2]
        for filename in dataset:
            # Read binary file and sore data in array
            with open(filename,'rb') as f:
                ts_data = f.read()
            f.close()
            # Define the total number records (24 bytes per record)
            size = int(len(ts_data)/24)
            # Unpack each record as the following succession:
            ts_data = struct.unpack('ddd'*size,ts_data)
            # Reshape array into 2D format
            ts_data = numpy.array(ts_data,dtype=float).reshape((size,3))
            data_list.append(ts_data)
    # Concatenate all time series in list
    data = numpy.concatenate(data_list)
    # Create timing array with equally separated timing sample
    t0,t1 = str2timestamp(t0,t1)
    times = numpy.linspace(t0-offset,t1-offset+3600,len(data),endpoint=False)
    rate  = 1./((t1+3600-t0)/len(data))
    # Create output data array
    if scalar:
        data = numpy.sqrt(numpy.sum(data**2,axis=1))
        # data = numpy.sqrt(numpy.sum(abs(data[:,1:])**2,axis=1))
        data = TimeSeries(data,sample_rate=rate,epoch=t0-offset)
    else:
        x = TimeSeries(data[:,0],sample_rate=rate,epoch=t0-offset)
        y = TimeSeries(data[:,1],sample_rate=rate,epoch=t0-offset)
        z = TimeSeries(data[:,2],sample_rate=rate,epoch=t0-offset)
        data = (x,y,z)
    return data

def biomed_converter(dataset,station,rate=3960,dest=None):
    """
    Convert binary data into new binary files. This function was optimized to prepare the
    dataset for an entire month of data. Several downsample version of the data will be
    produced: 3960Hz, 1980Hz, 990Hz, 198Hz, 1Hz, and 1S/min.

    Examples
    --------
    >>> nuri convert --path ~/Cloud/Google/MagneticFieldData/ \\ 
    >>>              --dest ~/Cloud/Dropbox/citymag/data/ --rate 1 \\
    >>>              --period 2016-5-15-18 2016-5-21 --station 4
    """
    # Define data path and move to repository
    data_path = os.getenv('HOME')+'/nuri_data' if dest==None else dest
    # Initialise arrays and loop over found datasets
    i=0
    for filename in dataset:
        # Go to station target folder
        os.system('mkdir -p %s/'%data_path)
        os.chdir('%s/'%data_path)
        # Check if target file is original Google Drive zip folder
        if '.zip' in filename and os.stat(filename).st_size>4e+7:
            print('> Extracting files from %s'%filename)
            tprocess = time.time()
            # Read zip file
            zip_rep = zipfile.ZipFile(filename, 'r')
            # Identify timing file in the compressed folder
            filename = filename.split('/')[-1].split('-xx')[-2]+'-xx_time.bin'
            filename = filename if filename in zip_rep.namelist() else filename.replace('.bin','_v2.bin')
            # Check if data already present in repository otherwise extract
            if os.path.exists(filename)==False:
                zip_rep.extractall()
            # Close the zip file reading
            zip_rep.close()
            print('  > Process time: %ss'%(time.time()-tprocess))
        if '.bin' in filename:
            print('  > Creating data with %s sampling rate'%rate)
            tprocess = time.time()
            # Extract data from X direction file
            xfile = filename.split('-xx')[0]+'-xx_rawX_uT_3960Hz.bin'
            x = read_axis(xfile,rate)
            # Extract data from Y direction file
            yfile = filename.split('-xx')[0]+'-xx_rawY_uT_3960Hz.bin'
            y = read_axis(yfile,rate)
            # Extract data from Z direction file
            zfile = filename.split('-xx')[0]+'-xx_rawZ_uT_3960Hz.bin'
            z = read_axis(zfile,rate)
            os.system('rm *xx*.bin')
            # If one array has lower length than others, discard first samples
            imax = min(len(x),len(y),len(z))
            # Create filename for converted file
            filename = numpy.array(re.split('-|_',filename)[:4],dtype=int)
            filename = '{0:>04}-{1:>02}-{2:>02}-{3:>02}'.format(*filename)+'_%ipts.bin'%imax
            # Save magnetic field data into new binary file
            magdata = (numpy.vstack([x[-imax:],y[-imax:],z[-imax:]]).T).ravel()
            # Move to destination path
            station_path = '/NURI-station-%02i/'%station
            os.system('mkdir -p %s/%iHz/%s/'%(data_path,rate,station_path))
            os.chdir('%s/%iHz/%s/'%(data_path,rate,station_path))
            # Create new binary file
            binfile = open(filename,'wb')
            binfile.write(struct.pack('d'*len(magdata), *magdata))
            binfile.close()
            print('  > Process time: %ss'%(time.time()-tprocess))
        
def biomed_timing(filename,rate,offset):
    """
    Read timing binary file and construct full timestamp array.

    Parameters
    ----------
    filename : str
      Path to the timing binary file
    offset : datetime
      Offset time to match time in targeted filename 
    
    Returns
    -------
    tgps : numpy.array
      Reconstructed full timing array
    """
    # Read binary file and sore data in array
    with open(filename,'rb') as f:
        data = f.read()
    f.close()
    # Check timing version
    if 'time_v2' in filename:
        # Define the total number records (63 bytes per record)
        size = len(data)/63
        # Unpack each record as the following succession:
        data = struct.unpack('<'+'qI?Qddcdcdd'*size,data)
        # Reshape array into 2D format
        data = numpy.array(data,dtype=object).reshape((size,11))
        # Fix chunk index column
        idxs = [i*138 for i in range(len(data))]
        # Create incremented sample index array
        x = numpy.array(idxs+data[:,1],dtype=float)
        # Defined timestamp array
        y = numpy.array(data[:,4]+offset)
        # Fit timestamp array
        popt,pcov = numpy.polyfit(x,y,1,cov=True)
        # Create full sample index array
        xfit = numpy.arange(x[-1])
        # Construct full timestamp array
        tgps = numpy.polyval(popt,xfit)
    else:
        # Define the total number records (28 bytes per record)
        size = len(data)/28
        # Unpack each record as the following succession:
        data = struct.unpack('<'+'qiQd'*size,data)
        # Reshape array so that each row corresponds to one record
        data = numpy.reshape(data,(size,4))
        # Convert timestamp into 
        data[:,2] = [(int(i) & 0x7fffffffffffffff)/1e7 for i in data[:,2]]
        # Correct timestamp from offset between system clock and UTC time
        data[:,2]-=(datetime(1970,1,1)-datetime(1,1,1)).total_seconds()
        # Create incremented sample index array
        x = data[:,0]+data[:,1]
        # Defined timestamp array
        y = data[:,2]+offset
        # Fit timestamp array
        popt,pcov = numpy.polyfit(x,y,1,cov=True)
        # Create full sample index array
        xfit = numpy.arange(x[-1])
        # Construct full timestamp array
        tgps = numpy.polyval(popt,xfit)
    # Define downsampling factor
    downfactor = 1 if rate==None else int(3960. / rate)
    # Check if sampling rate divisible by targeted sampling rate
    if rate!=None and 3960 % rate != 0:
        print('Targeted rate of %i is not a multiple of original sampling rate of %i. Abort.'%(rate,3960))
        quit()
    # Downsample time and data arrays
    tgps = tgps if downfactor==1 else tgps[::downfactor][:-1]
    return numpy.array(tgps)

def read_axis(filename,rate):
    """
    Read the binary file of magnetic field axis.

    Parameters
    ----------
    filename : str
      Path to data file

    Returns
    -------
    data : numpy.array
      Magnetic field data.
    """
    # Read binary file and sore data in array
    with open(filename,'rb') as f:
        data = f.read()
    f.close()
    # Define the total number records (63 bytes per record)
    size = len(data)//8
    # Unpack each record
    data = numpy.array(struct.unpack('d'*size,data))
    # Get median and standard deviation of time series
    med = numpy.median(data)
    std = numpy.std(data)
    # Look for outlier (10 times std) and fix value to median.
    idxs = numpy.where(abs(data-med)>10*std)[0]
    data[idxs] = med
    # Define downsampling factor
    downfactor = 1 if rate==None else int(3960. / rate)
    if downfactor>1:
        # Get closest multiple of the downsample factor from the data length
        limit = int(downfactor * round(float(len(data))/downfactor))
        # Ensure data length is multiple of downsampling factor
        data = data[:limit] if limit<=len(data) else data[:limit-downfactor]
        # Re-sample the data
        data = signal.resample(data,len(data)//downfactor)
    return data

def get_coord(filename):
    """
    Extracted longitude and latitude from version 2 timing data files.

    Parameters
    ----------
    filename : str
      Name of the timing binary file.

    Returns
    -------
    lat, lon : float
      Latitute and Longitude of the magnetic sensor.
    """
    with open(filename,'rb') as f:
        data = f.read()
    f.close()
    s = len(data)/63
    data = struct.unpack('<'+'qipQddcdcdd'*s,data)
    data = numpy.reshape(data,(s,11))
    lat  = float(str(float(data[0,5])/100).split('.')[0])
    lat  = lat + (float(data[0,5])-lat*100)/60
    lat  = -lat if data[0,8]=='S' else lat
    lon  = float(str(float(data[0,7])/100).split('.')[0])
    lon  = lon + (float(data[0,7])-lon*100)/60
    lon  = -lon if data[0,6]=='W' else lon
    return lat,lon

def bulk_decimate(input_dir,output_dir,station,tmin,tmax,rate=1):
    """
    Decimate data in bulk. This method loops over files available within
    the target period and save resampled version of the data in the output
    data directory.

    Parameters
    ----------
    input_dir : :class:`str`
      Path to input data directory.
    output_dir : :class:`str`
      Path to output directory where resampled data are saved.
    station : :class:`int`
      Index of station from which data are processed.
    tmin : :class:`str`
      Start timestamp of the target period.
    tmax : :class:`str`
      Final timestamp of the target period.
    rate : :class:`int`
      Target sampling rate

    Examples
    --------
    >>> nuri.bulk_decimate(input_dir='/content/drive/MyDrive/CityMagData/3960Hz/',output_dir='1Hz/',station=2,tmin='2016-3-14-10',tmax='2016-3-14-11',rate=10)
    > Extracting files from /content/drive/MyDrive/CityMagData/3960Hz//2016/3/14/10/NURI-station-02/2016-3-14_10-xx.zip
      > Process time: 2.2113912105560303s
      > Creating data with 10 sampling rate
      > Process time: 21.934987783432007s
    """
    main_path = os.getcwd()
    tmin,tmax = str2timestamp(tmin,tmax)
    tmin = datetime.utcfromtimestamp(tmin)
    tmax = datetime.utcfromtimestamp(tmax)
    offset = data_offset(tmin,tmax,station=station)
    dataset = data_lookup(input_dir,tmin,tmax,station=station,offset=offset)
    for file_path in dataset:
        biomed_converter([file_path],station=station,rate=rate,dest=output_dir)
        os.chdir(main_path)

def get_vmr_data(path,rate=None,offset=0.,ufactor=1000,tmin=None,tmax=None,chunk_size=60):
    """
    Extract data from individual VMR data log file

    Parameters
    ----------
    sample_rate : int
      Actual sampling rate of the recorded data
    rate : int
      Targeted sampling rate after downsampling
    ufactor : float
      Magnetic field factor to convert into microTesla
    
    Returns
    -------
    data : gwpy.timeseries.TimeSeries
      Time series data of the scalar magnitude
    """
    # Read binary file and store floating values in numpy array
    with open(path,'rb') as f:
      data = f.read()
    f.close()
    size = int(len(data)/32)
    data = struct.unpack('dddd'*size,data)
    data = numpy.reshape(data,(size,4))
    data[:,0] += offset*3600.
    # Identify samples to discard
    if tmin!=None:
      idxs = numpy.where(data[:,0]<tmin)[0]
      data = numpy.delete(data,idxs,axis=0)
    if tmax!=None:
      idxs = numpy.where(data[:,0]>tmax)[0]
      data = numpy.delete(data,idxs,axis=0)
    # Derive data sampling rate from average dt between samples
    sample_rate = round(1./numpy.average([data[i+1,0]-data[i,0] for i in range(len(data)-1)]))
    target_rate = sample_rate if rate==None else rate
    downfactor = int(sample_rate / target_rate)
    if sample_rate % target_rate != 0:
        print('Targeted rate of %i is not a multiple of original sampling rate of %i. Abort.'%(target_rate,sample_rate))
        quit()
    # Calculate scalar value of magnetic field for each sample
    scalar = numpy.sqrt(numpy.sum(abs(data[:,1:]/ufactor)**2,axis=1))
    # Check if targeted sampling rate different than original rate
    if sample_rate != target_rate:
        # Get closest multiple of the downsample factor from the data length
        limit = int(downfactor * round(float(len(scalar))/downfactor))
        # Ensure data length is multiple of downsampling factor
        scalar = scalar[:limit] if limit<=len(scalar) else scalar[:limit-downfactor]
        # Re-sample the data
        scalar = signal.resample(scalar,len(scalar)/downfactor)
    # Print out first and last timestamp values
    date0 = datetime.fromtimestamp(data[0,0]).strftime('%Y-%m-%d %H:%M:%S.%f')
    date1 = datetime.fromtimestamp(data[-1,0]).strftime('%Y-%m-%d %H:%M:%S.%f')
    print('Data selected from %s to %s'%(date0,date1))
    # Store data into GwPy time series format
    data = TimeSeries(scalar,sample_rate=target_rate,epoch=data[0,0])
    return data
    
def get_gnome(station,t0,t1,local=False,rep=None):
    """
    Glob all files withing user-defined period and extract data.

    Parameters
    ----------
    station : str
      Name of the station to be analysed
    t0 : str
      Starting time in format YYYY-MM-DD-HH-MM
    t1 : str
      Ending time in format YYYY-MM-DD-HH-MM
    local : bool
      Whether we extract local (GPS) or universal (UTC) time.
    rep : str
      Path in which the data are stored.

    Returns
    -------
    data : numpy.array
      2D magnetic field data array.
    """
    print('Searching GNOME data files...')
    # Convert start and end dates into datetime objects
    t0 = datetime(*numpy.array(t0.split('-'),dtype=int))
    t1 = datetime(*numpy.array(t1.split('-'),dtype=int))
    dataset = []
    for date in numpy.arange(start,end,timedelta(minutes=1)):
        date = date.astype(datetime)
        fullpath = rep+'/'+station+'_'+date.strftime("%Y%m%d_%H%M*.h5")
        dataset += glob.glob(fullpath)
    if sample:
        dataset = glob.glob(rep+"/*.h5")
    gps_offset = (datetime(1980,1,6)-datetime(1970,1,1)).total_seconds()
    tdata,xdata = [],[]
    for fname in sorted(dataset):
        hfile = h5py.File(fname, "r")
        dset = hfile['MagneticFields']
        datestr = dset.attrs["Date"]
        t0str = dset.attrs["t0"]
        # Format date from extracted metadata
        instr = "%d-%d-%02dT" % tuple(map(int, datestr.split('/'))) + t0str
        # Calculate offset between UTC and GPS initial epoch time
        gps_offset = (datetime(1980,1,6)-datetime(1970,1,1)).total_seconds()
        # Calculate GPS epoch
        gps_epoch = astropy.time.Time(instr, format='isot', scale='utc').gps + gps_offset
        utc,gps     = datetime.utcfromtimestamp(gps_epoch),datetime.fromtimestamp(gps_epoch)
        delay       = round(abs((utc-gps).total_seconds())/3600.)
        start_time  = gps if local else utc
        start_time  = time.mktime(start_time.timetuple())
        sample_rate = dset.attrs["SamplingRate(Hz)"]
        end_time    = start_time + len(dset[:]) / sample_rate
        tarray      = numpy.linspace(start_time,end_time,len(dset[:]))
        t0 = time.mktime(t0.timetuple())+t0.microsecond/1e6
        t1 = time.mktime(t1.timetuple())+t1.microsecond/1e6
        idx = numpy.where(numpy.logical_and(t0-1<tarray,tarray<t1+1))[0]
        xdata       = numpy.hstack((xdata,dset[:][idx]))
        tdata       = numpy.hstack((tdata,tarray[idx]))
        hfile.close()
    data = numpy.vstack((tdata,10*xdata)).T
    return data

