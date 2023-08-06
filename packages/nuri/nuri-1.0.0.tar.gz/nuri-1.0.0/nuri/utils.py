###############################################################################
# Copyright (c) 2018, Urban Magnetometry Group.
# Produced at the University of California at Berkeley.
# Written by V. Dumont (vincentdumont11@gmail.com).
# All rights reserved.
# This file is part of NURI.
# For details, see github.com/vincentdumont/nuri.
# For details about use and distribution, please read NURI/LICENSE.
###############################################################################

# System
import os
import sys
import time
from datetime import datetime

# External
import numpy
from gwpy.timeseries import TimeSeries

def data_chunk(data,hours,samp_per_hr=3600):
    """
    Concatenate data chunks for a given time period. Given a specific
    time period, this method will loop through all available days and
    concatenate time series data that fall in the same time period.
    This function is used in `our paper <http://citymag.gitlab.io/nuri/paper#Fig.-3:-Power-Spectral-Density>`_
    when building Power Spectral Densities at low frequencies.

    Parameters
    ----------
    data : :class:`numpy.ndarray`
      Input magnetic field data.
    hours : :class:`list` [ :class:`int` ]
      Start and final hours of the daily period.
    samp_per_hr : :class:`int`
      Number of samples in an hour of data.

    Returns
    -------
    avg : :class:`list`
      List of concatenated time series values.

    Examples
    --------
    In the example below, we concatenate 2 hours of time series data,
    from 9 to 11 AM, over a 4-day period, from 1st to 5th of April 2016.
    The data are sampled at 1-Hertz, so 3,600 data points per hour.
    Therefore, a total of 3600 data points * 2 hours * 4 days = 28,800
    data points returned.

    >>> data = nuri.get_data('2016-4-1','2016-4-5','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
    >>> data = nuri.data_chunk(data.value,[9,11],samp_per_hr=3600)
    >>> print(len(data))
    28800
    """
    avg = []
    for i in range(0,len(data),samp_per_hr*24):
        imin = int(hours[0]*samp_per_hr)
        imax = int(hours[1]*samp_per_hr)
        avg.extend(data[i+imin:i+imax])
    return avg

def day_and_night(data,daytime,samp_per_hr=3600):
    """
    Split data into separate day and night time-series.

    Parameters
    ----------
    data : :class:`numpy.ndarray`
      Input magnetic field data.
    daytime : :class:`list` [ :class:`list` [ :class:`int` ] ]
      List of daytime hour ranges. Multiple ranges can be provided
      in case the night time starts after midnight.
    samp_per_hr : :class:`int`
      Number of samples in an hour of data.

    Returns
    -------
    day :  :class:`list` [ :class:`float` ]
      Concatenated daytime time-series.
    night :  :class:`list` [ :class:`float` ]
      Concatenated nighttime time-series.    

    Examples
    --------
    >>> data = nuri.get_data('2016-4-1','2016-4-3','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
    >>> day, night = nuri.day_and_night(data.value,daytime=[[0,1],[4.5,24]])
    >>> print(len(day),len(night))
    147581 25200
    """
    day, night = [], []
    for i in range(0,len(data),samp_per_hr*24):
        for n,(imin,imax) in enumerate(daytime):
            hmin = int(imin*samp_per_hr)
            hmax = int(imax*samp_per_hr)
            day.extend(data[i+hmin:i+hmax])
            if n==0:
                night.extend(data[i:i+hmin])
            if n+1<len(daytime):
                hnext = int(daytime[n+1][0]*samp_per_hr)
                night.extend(data[i+hmax:i+hnext])
            if n+1==len(daytime):
                night.extend(data[i+hmax:i+24*samp_per_hr])
    return day, night

def downsample(data,downfactor):
    """
    Downsample data time series.
    """
    times = data[:,0] if downfactor==1 else data[::downfactor,0][:-1]
    # Get closest multiple of the downsample factor from the data length
    limit = int(downfactor * round(float(len(data))/downfactor))
    # Ensure data length is multiple of downsampling factor
    data = data[:limit,1] if limit<=len(data) else data[:limit-downfactor,1]
    # Re-sample the data
    data = signal.resample(data,len(data)//downfactor)
    # Create dataset
    data = numpy.vstack((times,data)).T
    return data

def str2timestamp(*times):
    """
    Convert times into datetime timestamps.
    
    Parameters
    ----------
    times : :class:`list` [ :class:`str` ]
      Start and final times of the target period.

    Returns
    -------
    time_list : :class:`list` [ :class:`float` ]
      Dates converted into floating timestamps

    Examples
    --------
    >>> times = nuri.str2timestamp('2016-4-1','2016-4-5')
    >>> print(times)
    (1459468800.0, 1459814400.0)
    """
    time_list = []
    for dt in times:
        # Split date by dashes
        dt = numpy.array(dt.split('-'),dtype=int)
        # Include day 1 if no day provided
        dt = dt if len(dt)>2 else numpy.hstack((dt,1))
        # Convert string to datetime format
        dt = datetime(*dt)
        # Convert start date into timestamp
        dt = time.mktime(dt.timetuple())+dt.microsecond/1e6
        # Convert timestamp back local datetime
        now = datetime.fromtimestamp(dt)
        # Convert timestamp to UTC datetime
        utc_now = datetime.utcfromtimestamp(dt)
        # Calculate local difference with UTC time
        utc2local = (now-utc_now).total_seconds()
        # Remove UTC offset from timestamp
        dt += utc2local
        time_list.append(dt)
    return tuple(time_list) if len(time_list)>1 else time_list[0]

def str2datetime(*dates):
    '''
    Convert input string date to datetime format.
    '''
    date_list = []
    for date in dates:
        dstr = ['%Y','%m','%d','%H','%M','%S','%f']
        dsplit = '-'.join(dstr[:date.count('-')+1])
        date = datetime.strptime(date,dsplit)
        date_list.append(date)
    return tuple(date_list) if len(date_list)>1 else date_list[0]

def is_float(a):
    """
    Return whether input variable is a float.
    """
    try:
        float(a)
        return True
    except ValueError:
        return False

def make_video():
    """
    Make video out of saved figures.
    """
    os.system('ls *.png > list.dat')
    filelist = sorted(numpy.loadtxt('list.dat',dtype=str))
    for i in range(len(filelist)):
        newpath = 'series%04i.png'%(i+1)
        if os.path.exists(newpath)==False:
            os.system('cp %s %s'%(filelist[i],newpath))
    os.system('ffmpeg -framerate 30 -i series%04d.png  -start_number 1 -c:v libx264 -r 30 -pix_fmt yuv420p ../video.mp4')
    os.system('rm list.dat series*')
    
def fix_jumps(data,nsamp=1800,edge=5):
    '''
    Fix jumps in time series data.

    Examples
    --------
    >> import nuri
    >> berkeley = berkeley_raw[:-1].copy()
    >> berkeley = nuri.fix_jumps(berkeley,edge=10)
    >> berkeley = nuri.normalize(berkeley,saved='saved.dat',play=False).get_updated_data()
    '''
    for i in range(0,len(data)-nsamp,nsamp):
        var = numpy.var(data.value[i:i+nsamp])
        if abs(var)>0.1:
            for j in range(i+nsamp,i,-1):
                if numpy.var(data.value[j:i+nsamp])>0.005:
                    j-=edge
                    break
            for k in range(i,i+nsamp):
                if numpy.var(data.value[i:k])>0.005:
                    k+=edge
                    break
            break
    data.value[j:k] = data.value[j]
    data.value[k:] -= (data.value[k]-data.value[j])
    return data

def get_variance(data,period='weekday',bin_size=1200):
  start,length = (0,5) if period=='weekday' else (5,2)
  variances = []
  for n,i in enumerate(range(0,len(data)-3600*24,3600*24)):
    if n in numpy.array([numpy.arange(i,i+length) for i in range(start,35,7)]):
      var = []
      for j in range(i,i+3600*24,bin_size):
        var.append(numpy.var(data[j:j+bin_size]))
      variances.append(var)
  var = numpy.mean(variances,axis=0)
  times = numpy.linspace(0,24,len(var))
  return times,var

def rescale(freqs,data,num=1000,mode='linear'):
  if mode=='linear':
    new_freqs = numpy.linspace(freqs[0],freqs[-1],num)
    new_data = [data[abs(freqs-f).argmin()] for f in new_freqs]
    return numpy.array(new_freqs),numpy.array(new_data)
  if mode=='log':
    new_freqs = numpy.logspace(numpy.log10(freqs[1]),numpy.log10(freqs[-1]),num)
    new_data = [data[abs(freqs-f).argmin()] for f in new_freqs]
    return numpy.concatenate(([freqs[0]],new_freqs)),numpy.concatenate(([data[0]],new_data))

def transform_data(data_full,length,sample_rate=1,omega0=6,dj=0.05):
    import mlpy
    data   = data_full[:length]
    scales = mlpy.wavelet.autoscales(N=len(data.value),dt=1./sample_rate,dj=dj,wf='morlet',p=omega0)
    freqs  = (omega0 + numpy.sqrt(2.0 + omega0 ** 2)) / (4 * numpy.pi * scales[1:])
    spec   = mlpy.wavelet.cwt(data.value,dt=1./sample_rate,scales=scales,wf='morlet',p=omega0)
    spec   = numpy.abs(spec)**2
    return scales,freqs,spec

def normalize(data):
    data -= numpy.median(data)
    data /= max(abs(data))
    return data

