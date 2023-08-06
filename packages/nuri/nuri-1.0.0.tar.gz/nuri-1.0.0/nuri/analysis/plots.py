###############################################################################
# Copyright (c) 2018, Urban Magnetometry Group.
# Produced at the University of California at Berkeley.
# Written by V. Dumont (vincentdumont11@gmail.com).
# All rights reserved.
# This file is part of NURI.
# For details, see github.com/vincentdumont/nuri
# For details about use and distribution, please read NURI/LICENSE.
###############################################################################

# System
import os
import math
import glob
from datetime import datetime,timedelta

# External
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib import colors
from matplotlib.ticker import LogLocator
from gwpy.timeseries import TimeSeries
from scipy import fftpack,signal

# Local
from ..utils import transform_data, day_and_night, get_variance
from .fitting import gaussian_fit

# Clean customized matplotlib settings from GwPy
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
# Use seaborn plotting style
plt.style.use('seaborn')
# Set new default label size
plt.rc('font', size=14, family='sans-serif')
plt.rc('axes', labelsize=14, linewidth=0.2)
plt.rc('legend', fontsize=12, handlelength=10)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)
# Increase chunk size
plt.rcParams['agg.path.chunksize'] = 10000

def make_hour_spec(t0,t1,station=None):
    """
    Download data for specific period. The default period downloaded will
    be the last 24 hours.

    Parameters
    ----------
    station : float
      Station number. Default is all stations.
    start : str
      Starting date of the data to be retrieved, YYYY-MM-DD-HH
    end : Ending date of the data to be retrieved, YYYY-MM-DD-HH

    Examples
    --------
    >>> nuri_download --start 2016-03-20 --end 2016-03-21 --station 4
    """
    # Convert start and end date into datetime object
    d0 = datetime(*numpy.array(t0.split('-'),dtype=int)) if t0!=None else datetime(2015,11,1)
    d1 = datetime(*numpy.array(t1.split('-'),dtype=int)) if t1!=None else datetime.now()+timedelta(days=1)
    # Store data for current month
    os.system('skicka ls -r /MagneticFieldData/ > data')
    data = numpy.loadtxt('data',dtype=str,delimiter='\n')
    # Loop through every hour
    for d in numpy.arange(d0,d1,timedelta(hours=1)):
        # Extract individual parameters from datetime object
        year  = d.astype(object).year
        month = d.astype(object).month
        day   = d.astype(object).day
        hour  = d.astype(object).hour
        # Define remote path to and filename of the compressed archive
        path  = 'MagneticFieldData/%i/%i/%i/%i/'%(year,month,day,hour)
        fzip  = '%i-%i-%i_%i-xx.zip'%(year,month,day,hour)
        # Loop through each station
        for i in range(4):
            # Define full path to archive
            fullpath = path+'NURI-station-%02i/'%(i+1)+fzip
            # Check if station is targeted and remote path exists
            if (station==None or int(station)==i+1) and fullpath in data:
                # Download, uncompress and store data
                os.system('mkdir -p ./NURI-station-%02i/'%(i+1))
                os.system('skicka download /%sNURI-station-%02i/%s ./'%(path,i+1,fzip))
                os.system('unzip '+fzip)
                os.system('mv %i-%i-%i_%i-xx_* NURI-station-%02i'%(year,month,day,hour,i+1))
                t0 = '%i-%i-%i-%i'%(year,month,day,hour)
                dnext = d.astype(object)+timedelta(hours=1)
                t1 = '%i-%i-%i-%i'%(dnext.year,dnext.month,dnext.day,dnext.hour)
                mag_data = get_data(t0,t1,downfactor=3960,station=i+1,rep='./')
                tmin,tmax = str2timestamp(d.astype(object),dnext)
                fname = 'NURI-station-%02i/%i-%02i-%02i_%02i'%(i+1,year,month,day,hour)
                plot_spectrogram(mag_data,tmin,tmax,fscale='mHz',scale='mins',tbs=True,fname=fname)
                os.system('rm %s NURI-station-%02i/%i-%i-%i_%i-xx_*'%(fzip,i+1,year,month,day,hour))
    os.system('rm data')

def plot_spectrogram(data,tmin=None,tmax=None,fmin=None,fmax=None,vmin=None,vmax=None,
                     mmax=None,mmin=None,mode='wavelet',omega0=6,dj=0.05,fct='morlet',
                     stride=None,nfft=None,overlap=None,scale='log',median=False,
                     funit='Hz',tunit='secs',cmap='inferno',zone='Local',fname=None):
    """
    Plot multiplot figure with time series, PSD and spectrogram.

    Parameters
    ----------
    data : TimeSeries
      Magnetic field data
    tmin, tmax : datetime
      First and last timestamps
    fmin, fmax : float
      Minimum and maximum frequencies
    vmin, vmax : float
      Minimum and maximum color values
    mode : str
      Spectrogram mode, wavelet or Fourier. Default is Fourier
    omega0 : int
      Wavelet function parameter
    dj : float
      Scale resolution (smaller values of dj give finer resolution)
    fct : str
      Wavelet function (morlet,paul,dog)
    stride : float
      Length of segment
    nfft : float
      Length of FFT
    overlap : float
      Length of overlapping segment
    cmap : str
      Colormap
    scale : str
      Plotted frequency scale. Default is "log".
    funit : strg
      Frequency unit, Hz or mHz. Default is Hz.
    tunit : str
      Time unit, secs, mins or hrs. Default is mins.
    fname : str
      Output file name.

    Examples
    --------
    >>> data = nuri.get_data('2016-3-14-10','2016-3-14-11','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
    >>> nuri.plot_spectrogram(data)

    .. image:: _images/spectrogram.png
    
    Notes
    -----
    The `matplotlib.pyplot.imshow <https://matplotlib.org/api/pyplot_api.html?highlight=matplotlib%20pyplot%20imshow#matplotlib.pyplot.imshow>`_ module is
    used to plot the wavelet spectrogram. This module is usually used
    to plot raw images and assumes that the position of the cell in the
    input spectrogram array directly represents the position of the pixel
    in the raw image. That is, for an input Python array (in which rows
    are appended below previous ones), the first row in the array is
    assumed to represent the top line of pixel in the image. Therefore,
    in order to plot the spectrogram array using the imshow module, one
    needs to carefully check that the rows (which are representative of
    the frequency bands), are stored in descending order such that the
    lowest frequency is placed at the end (bottom) of the array.
    """
    import mlpy
    if mode=='wavelet' and scale=='linear':
        print('Warning: Wavelet mode chosen. Scale will be changed to log.')
        scale = 'log'
    # Initialise figure
    fig = plt.figure(figsize=(24,14),frameon=False)
    plt.subplots_adjust(left=0.07, right=0.95, bottom=0.1, top=0.95, hspace=0, wspace=0)
    ax1 = fig.add_axes([0.20,0.75,0.683,0.20])
    ax2 = fig.add_axes([0.20,0.10,0.683,0.64], sharex=ax1)
    ax3 = fig.add_axes([0.07,0.10,0.123,0.64])
    ax4 = fig.add_axes([0.89,0.10,0.030,0.64])
    # Prepare timing range
    tmin = data.times[0].value  if tmin==None else tmin
    tmax = data.times[-1].value if tmax==None else tmax
    mask = (data.times.value>=tmin) & (data.times.value<=tmax)
    scale_factor = 3600. if tunit=='hrs' else 60. if tunit=='mins' else 1
    times = (data[mask].times.value-tmin)/scale_factor
    dt = 1./data.sample_rate.value
    # Plot time series
    median = numpy.median(data[mask].value) if median else 0.
    ax1.plot(times,data[mask].value-median,alpha=0.5)
    ax1.set_ylabel('Magnetic Fields [uT]',fontsize=11)
    ax1.tick_params(bottom='off',labelbottom='off')
    if mmin!=None: ax1.set_ylim(ymin=mmin)
    if mmax!=None: ax1.set_ylim(ymax=mmax)
    ax1.set_xlim(0,(tmax-tmin)/scale_factor)
    ax1.grid(b=True, which='major', alpha=0.7, ls='--')
    if mode=='wavelet':
        # Calculate wavelet parameters
        scales = mlpy.wavelet.autoscales(N=len(data[mask].value),dt=dt,dj=dj,wf=fct,p=omega0)
        spec = mlpy.wavelet.cwt(data[mask].value,dt=dt,scales=scales,wf=fct,p=omega0)
        freq = (omega0 + numpy.sqrt(2.0 + omega0 ** 2)) / (4 * numpy.pi * scales[1:])
        freq = freq * 1000. if funit=='mHz' else freq
        spec = numpy.abs(spec)**2
        spec = spec[::-1]
        # Define minimum and maximum frequencies
        fmin_log,fmax_log = min(freq),max(freq)
        fmin_linear,fmax_linear = min(freq),max(freq)
        if fmin!=None:
            log_ratio = (numpy.log10(fmin)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
            fmin_linear = min(freq)+log_ratio*(max(freq)-min(freq))
            fmin_log = fmin
        if fmax!=None:
            log_ratio = (numpy.log10(fmax)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
            fmax_linear = min(freq)+log_ratio*(max(freq)-min(freq))
            fmax_log = fmax
        # Get minimum and maximum amplitude in selected frequency range
        idx = numpy.where(numpy.logical_and(fmin_log<freq[::-1],freq[::-1]<fmax_log))[0]
        vmin = vmin if vmin!=None else numpy.sort(numpy.unique(spec[idx]))[1]
        vmax = spec[idx].max() if vmax==None else vmax
        # Plot spectrogram
        img = ax2.imshow(spec,extent=[times[0],times[-1],freq[-1],freq[0]],aspect='auto',
                        interpolation='nearest',cmap=cmap,norm=matplotlib.colors.LogNorm(vmin,vmax)) 
        ax2.set_xlabel('Time [%s] from %s to %s %s Time (%s - %s)'%(tunit,datetime.utcfromtimestamp(tmin),datetime.utcfromtimestamp(tmax),zone,tmin,tmax),fontsize=15)
        ax2.set_xlim(0,(tmax-tmin)/scale_factor)
        ax2.set_yscale('linear')
        ax2.set_ylim(fmin_linear,fmax_linear)
        ax2.grid(False)
        # Set up axis range for spectrogram
        twin_ax = ax2.twinx()
        twin_ax.set_yscale('log')
        twin_ax.set_xlim(0,(tmax-tmin)/scale_factor)
        twin_ax.set_ylim(fmin_log,fmax_log)
        twin_ax.spines['top'].set_visible(False)
        twin_ax.spines['right'].set_visible(False)
        twin_ax.spines['bottom'].set_visible(False)
        ax2.tick_params(which='both', labelleft=False, left=False)
        twin_ax.tick_params(which='both', labelleft=False,left=False, labelright=False, right=False)
        twin_ax.grid(False)
    if mode=='fourier':
        freq, times, spec = signal.spectrogram(data[mask],fs=data.sample_rate.value,
                                           nperseg=stride,noverlap=overlap,nfft=nfft)
        # Convert time array into minute unit
        times = (numpy.linspace(data[mask].times.value[0],data[mask].times.value[-1],len(times))-tmin)/scale_factor
        # Define minimum and maximum frequencies
        freq = freq * 1000. if funit=='mHz' else freq
        fmin = freq[1]      if fmin==None    else fmin
        fmax = max(freq)    if fmax==None    else fmax
        fmin_log,fmax_log = fmin,fmax
        # Get minimum and maximum amplitude in selected frequency range
        idx = numpy.where(numpy.logical_and(fmin<=freq,freq<=fmax))[0]
        vmin = vmin if vmin!=None else numpy.sort(numpy.unique(spec[idx]))[1]
        vmax = spec[idx].max() if vmax==None else vmax
        # Plot spectrogram
        img = ax2.pcolormesh(times,freq,spec,cmap=cmap,norm=matplotlib.colors.LogNorm(vmin,vmax))
        ax2.set_xlabel('Time [%s] from %s to %s %s Time (%s)'%(tunit,datetime.utcfromtimestamp(tmin),datetime.utcfromtimestamp(tmax),zone,tmin),fontsize=15)
        ax2.set_xlim(0,(tmax-tmin)/scale_factor)
        ax2.set_ylim(fmin,fmax)
        ax2.set_yscale(scale)
        ax2.set_ylabel('Frequency [%s]'%funit,fontsize=15,labelpad=40)
        ax2.tick_params(which='both', labelleft=False, left=False)
        ax2.grid(False)
    # Calculate Power Spectral Density
    N = len(data[mask].value)
    delta_t = 1/data.sample_rate.value
    delta_f = 1. / (N * delta_t)
    f = delta_f * numpy.arange(N / 2)
    f = f * 1000. if funit=='mHz' else f
    PSD = abs(delta_t * fftpack.fft(data[mask].value)[:N // 2]) ** 2
    psd = numpy.vstack((f,PSD)).T
    # Plot Power Spectral Density
    ticks = matplotlib.ticker.FuncFormatter(lambda v,_:("$10^{%.0f}$"%math.log(v,10)))
    ax3.loglog(psd[:,1],psd[:,0],alpha=0.5)
    ax3.invert_xaxis()
    ax3.set_ylim(fmin_log,fmax_log)
    ax3.set_ylabel('Frequency [%s]'%funit,fontsize=15)
    ax3.set_xlabel('PSD',fontsize=15)
    ax3.grid(b=True, which='major', alpha=0.7, ls='--')
    # Add color bar and save figure
    cb = fig.colorbar(img,cax=ax4)
    cb.set_ticks(LogLocator())
    cb.set_clim(vmin,vmax)
    ax4.set_ylabel('Power $|\mathrm{W}_v|^2$ $[\mu T^2/\mathrm{Hz}]$',fontsize=15)
    plt.show() if fname==None else plt.savefig(fname)#,frameon=False)
    plt.close(fig)

def plot_time_series(data,tmin=None,tmax=None,ymin=None,ymax=None,regions=[],
                     fname='time_series',zone='Local',tunit='secs',tbs=False):
    """
    Plot time series.

    Parameters
    ----------
    data : gwpy.timeseries.TimeSeries
      Time series data
    tmin : datetime
      First timestamp
    tmax : datetime
      Last timestamp
    fname : str
      Filename
    zone : str
      Output time zone, either UTC or Local
    tunit : str
      Scale of time axis (hrs, mins, secs)
    tbs : bool
      To Be Saved flag
    regions : list
      List of time regions to colorize
    """
    # Define timestamps if not defined by user
    tmin = data.times[0].value  if tmin==None else tmin
    tmax = data.times[-1].value if tmax==None else tmax
    # Re-determine the mask in case timestamps are defined
    mask = (data.times.value>=tmin) & (data.times.value<=tmax)
    # Estimate scale factor for time axis
    scale_factor = 3600. if tunit=='hrs' else 60. if tunit=='mins' else 1
    # Do the plotting
    fig = plt.figure(figsize=(12,5))
    plt.plot((data.times.value[mask]-tmin)/scale_factor,data.value[mask])
    if len(regions)>0:
        for text,tbeg,span in regions:
            tbeg = (str2timestamp(tbeg)-tmin)/scale_factor
            tend = tbeg+span/scale_factor
            plt.axvspan(tbeg,tend,color='red',ls='dotted',alpha=0.1)
            plt.text(tbeg+(tend-tbeg)/2,max(data.value[mask]),'%s'%text,fontsize=25,color='red',ha='center')
    plt.xlabel('Time [%s] from %s %s (%i)'%(tunit,datetime.utcfromtimestamp(tmin),zone,tmin))
    plt.ylabel('Magnetic Field [$\mathrm{\mu}$T]')
    plt.xlim(0,(tmax-tmin)/scale_factor)
    if ymin!=None: plt.ylim(ymin=ymin)
    if ymax!=None: plt.ylim(ymax=ymax)
    plt.tight_layout()
    plt.savefig('%s.png'%fname,frameon=False,transparent=True) if tbs else plt.show()
    plt.close(fig)

def ts_movie(data,tmin=None,tmax=None,fname='time_series',zone='Local',tunit='secs'):
    """
    Create time series movie

    Parameters
    ----------
    data : gwpy.timeseries.TimeSeries
      Time series data
    tmin : datetime
      First timestamp
    tmax : datetime
      Last timestamp
    fname : str
      Filename
    zone : str
      Output time zone, either UTC or Local
    tunit : str
      Scale of time axis (hrs, mins, secs)
    """
    t0,t1 = data.times.value[0],data.times.value[-1]
    tmin,tmax = (t0,t1) if tmin==tmax==None else str2timestamp(tmin,tmax)
    for time in numpy.arange(tmin,tmax,600):
        t0 = datetime.utcfromtimestamp(time)
        t1 = datetime.utcfromtimestamp(time+600)
        plot_time_series(data,t0,t1,fname='video_%s'%time,zone='Local',tunit='secs')
    os.system('convert -delay 60 -loop 0 -dispose previous video_*.png movie.gif')
    os.system('rm video_*.png')

def plot_wavelet(data,tmin=None,tmax=None,fmin=None,fmax=None,vmin=None,vmax=None,omega0=6,dt=1,dj=0.05,
                 fct='morlet',funit='Hz',cmap='inferno',zone='Local',tunit='secs',fname='wavelet',tbs=False):
    """
    Create wavelet spectrogram

    Parameters
    ----------
    data : gwpy.timeseries.TimeSeries
      Time series data
    tmin : datetime
      First timestamp
    tmax : datetime
      Last timestamp
    omega0 : int
      Wavelet function parameter
    dt : float
      Time step
    dj : float
      Scale resolution (smaller values of dj give finer resolution)
    fct : str
      Wavelet function (morlet,paul,dog)
    tbs : bool
      To Be Saved flag
    """
    import mlpy
    # Define timestamps if not defined by user
    tmin = data.times[0].value  if tmin==None else tmin
    tmax = data.times[-1].value if tmax==None else tmax
    # Re-determine the mask in case timestamps are defined
    mask = (data.times.value>=tmin-1) & (data.times.value<=tmax+1)
    # Calculate wavelet parameters
    scales = mlpy.wavelet.autoscales(N=len(data[mask].value),dt=dt,dj=dj,wf=fct,p=omega0)
    spec = mlpy.wavelet.cwt(data[mask].value,dt=dt,scales=scales,wf=fct,p=omega0)
    freq = (omega0 + numpy.sqrt(2.0 + omega0 ** 2)) / (4 * numpy.pi * scales[1:])
    spec = numpy.abs(spec)**2
    spec = spec[::-1]
    # Convert time array into minute unit
    scale_factor = 3600. if tunit=='hrs' else 60. if tunit=='mins' else 1
    times = (data[mask].times.value-tmin)/scale_factor
    # Define minimum and maximum frequencies
    freq = freq * 1000. if funit=='mHz' else freq
    # Determine
    fmin_log,fmax_log = min(freq),max(freq)
    fmin_linear,fmax_linear = min(freq),max(freq)
    if fmin!=None:
        log_ratio = (numpy.log10(fmin)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
        fmin_linear = min(freq)+log_ratio*(max(freq)-min(freq))
        fmin_log = fmin
    if fmax!=None:
        log_ratio = (numpy.log10(fmax)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
        fmax_linear = min(freq)+log_ratio*(max(freq)-min(freq))
        fmax_log = fmax
    # Get minimum and maximum amplitude in selected frequency range
    idx = numpy.where(numpy.logical_and(fmin_log<freq[::-1],freq[::-1]<fmax_log))[0]
    vmin = spec[idx].min() if vmin==None else vmin
    vmax = spec[idx].max() if vmax==None else vmax
    # Initialise figure
    fig,ax = plt.subplots(figsize=(12,7))
    # Plot spectrogram
    img = ax.imshow(spec,extent=[times[0],times[-1],freq[-1],freq[0]],aspect='auto',
                    interpolation='nearest',cmap=cmap,norm=matplotlib.colors.LogNorm(vmin,vmax))
    ax.set_xlabel('Time [%s] from %s %s (%s)'%(tunit,datetime.utcfromtimestamp(tmin),zone,tmin),fontsize=15)
    ax.set_xlim(0,(tmax-tmin)/scale_factor)
    ax.set_yscale('linear')
    ax.set_ylim(fmin_linear,fmax_linear)
    ax.set_ylabel('Frequency [%s]'%funit,fontsize=15,labelpad=40)
    ax.grid(False)
    # Set up axis range for spectrogram
    twin_ax = ax.twinx()
    twin_ax.set_yscale('log')
    twin_ax.set_xlim(0,(tmax-tmin)/scale_factor)
    twin_ax.set_ylim(fmin_log,fmax_log)
    twin_ax.spines['top'].set_visible(False)
    twin_ax.spines['right'].set_visible(False)
    twin_ax.spines['bottom'].set_visible(False)
    ax.tick_params(which='both', labelleft=False, left=False)
    twin_ax.yaxis.tick_left()
    twin_ax.grid(False)
    # Add color bar and save figure
    cb = fig.colorbar(img,ax=ax,pad=0.01)
    cb.set_ticks(LogLocator())
    cb.set_label('Power $|\mathrm{W}_v|^2$ $[\mu T^2/\mathrm{Hz}]$',fontsize=15)
    cb.set_clim(vmin,vmax)
    plt.tight_layout()
    plt.savefig('%s.png'%fname) if tbs else plt.show()
    plt.close(fig)

def plot_psd(data,tmin=None,tmax=None,fname='psd',tbs=False):
    """
    Plot Power Spectral Density

    Parameters
    ----------
    data : gwpy.timeseries.TimeSeries
      Time series data
    tmin : datetime
      First timestamp
    tmax : datetime
      Last timestamp
    """
    # Define timestamps if not defined by user
    tmin = data.times[0].value  if tmin==None else tmin
    tmax = data.times[-1].value if tmax==None else tmax
    # Re-determine the mask in case timestamps are defined
    mask = (data.times.value>=tmin) & (data.times.value<=tmax)
    # Calculate PSD
    N = len(data[mask].value)
    dt = 1/data.sample_rate.value
    df = 1. / (N * dt)
    f = df * numpy.arange(N / 2)
    PSD = abs(dt * fftpack.fft(data[mask].value)[:N / 2]) ** 2
    psd = numpy.vstack((f,PSD)).T
    # Do the plotting
    fig = plt.figure(figsize=(12,7))
    plt.loglog(psd[:,0],psd[:,1])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Power Spectral Density [Hz$^{-1}$]')
    plt.savefig('%s.png'%fname) if tbs else plt.show()
    plt.close(fig)

def plot_specgram(data,tmin=None,tmax=None,fmin=None,fmax=None,vmin=None,vmax=None,tbs=False,
                  funit='Hz',cmap='viridis',zone='Local',tunit='secs',fname='spectrogram',
                  stride=None,nfft=None,overlap=None):
    """
    Plot Fourier spectrogram.

    Parameters
    ----------
    data : gwpy.timeseries.TimeSeries
      Time series data
    tmin : datetime
      First timestamp
    tmax : datetime
      Last timestamp
    tbs : bool
      To Be Saved flag
    """
    # Define timestamps if not defined by user
    tmin = data.times[0].value  if tmin==None else tmin
    tmax = data.times[-1].value if tmax==None else tmax
    # Re-determine the mask in case timestamps are defined
    mask = (data.times.value>=tmin-1) & (data.times.value<=tmax+1)
    freq, times, spec = signal.spectrogram(data[mask],fs=data.sample_rate.value,
                                           nperseg=stride,noverlap=overlap,nfft=nfft)
    times = (data[mask].times.value[::int(stride-overlap)]-tmin)/scale_factor
    # Convert time array into minute unit
    scale_factor = 3600. if tunit=='hrs' else 60. if tunit=='mins' else 1
    #times = (data[mask].times.value-tmin)/scale_factor
    # Define minimum and maximum frequencies
    freq = freq * 1000. if funit=='mHz' else freq
    fmin = freq[1]      if fmin==None    else fmin
    fmax = max(freq)    if fmax==None    else fmax
    # Get minimum and maximum amplitude in selected frequency range
    idx = numpy.where(numpy.logical_and(fmin<=freq,freq<=fmax))[0]
    vmin = vmin if vmin!=None else numpy.sort(numpy.unique(spec[idx]))[1]
    vmax = spec[idx].max() if vmax==None else vmax
    # Initialise figure
    fig,ax = plt.subplots(figsize=(12,7))
    # Plot spectrogram
    img = ax.pcolormesh(times,freq,spec,cmap='inferno',norm=matplotlib.colors.LogNorm())
    ax.set_xlabel('Time [%s] from %s %s (%s)'%(tunit,datetime.utcfromtimestamp(tmin),zone,tmin),fontsize=15)
    ax.set_xlim(0,(tmax-tmin)/scale_factor)
    ax.set_ylim(fmin,fmax)
    ax.set_yscale('log')
    ax.set_ylabel('Frequency [%s]'%funit,fontsize=15,labelpad=40)
    ax.grid(False)
    # Add color bar and save figure
    cb = fig.colorbar(img,ax=ax,pad=0.01)
    cb.set_ticks(LogLocator())
    cb.set_label('Power $|\mathrm{W}_v|^2$ $[\mu T^2/\mathrm{Hz}]$',fontsize=15)
    cb.set_clim(vmin,vmax)
    plt.tight_layout()
    plt.savefig('%s.png'%fname) if tbs else plt.show()
    plt.close(fig)

def plot_availability(path,period,sensor,station):
    """
    Plot data availability.

    Examples
    --------
    >>> nuri availability --path ~/Cloud/Google/MagneticFieldData/ \\
    >>>                   --period 2016-5-2 2016-6-6 --station 4
    """
    if period==None or station==None:
        print('Period or station not defined. Abort.')
        quit()
    # Convert input dates to readable format
    tmin = nuri.str2datetime(period[0])
    tmax = nuri.str2datetime(period[1])
    # Determine timing offset based on original file construction
    offset = data_offset(tmin,tmax,station) if sensor=='biomed' else 0
    # Loop through all requested hours
    i,data_list = 0,numpy.empty((0,2))
    for date in numpy.arange(tmin+timedelta(seconds=offset),tmax+timedelta(seconds=offset),timedelta(hours=1)):
        # Convert date into readable datetime format
        date = date.astype(datetime)
        # Determine path to compressed timing binary file path from Google structure
        data_path = '%s/%s/%s/%s/%s/NURI-station-%02i/'%(path,date.year,date.month,date.day,date.hour,station)+date.strftime("%Y-%-m-%-d_%-H-xx.zip")
        data_flag = 0 if len(glob.glob(data_path))==0 else 1
        # Determine customized path to timing binary file
        data_path = '%s/NURI-station-%02i/'%(path,station)+date.strftime("%Y-%-m-%-d_%-H-xx_time.bin")
        data_flag = data_flag if len(glob.glob(data_path))==0 else 1
        # Determine customized path to timing binary file
        data_path = '%s/NURI-station-%02i/'%(path,station)+date.strftime("%Y-%m-%d-%H_*.bin")
        data_flag = data_flag if len(glob.glob(data_path))==0 else 1
        data_list = numpy.vstack((data_list,[date,data_flag]))
        if data_flag==0:
            print('Data file not found for %s'%date.strftime("%Y-%m-%d-%H"))
        i+=1
    # Create figure
    fig = plt.figure(figsize=(12,5))
    plt.style.use('seaborn')
    plt.rc('font', size=14, family='sans-serif')
    plt.rc('axes', labelsize=20, linewidth=0.2)
    plt.rc('legend', fontsize=12, handlelength=10)
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    plt.scatter(data_list[:,0],data_list[:,1])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gcf().autofmt_xdate()
    plt.xlim(data_list[0,0],data_list[-1,0])
    fig.tight_layout()
    plt.show()
    plt.close()

def plot_dual_ts(ts1_data,ts1_name,ts1_usgs_data,ts2_data,ts2_name,ts2_usgs_data):
  fig,(ax1,ax2) = plt.subplots(2,1,figsize=(12,6),dpi=200)
  for ax,data,city,usgs in [[ax1,ts1_data,ts1_name,ts1_usgs_data],[ax2,ts2_data,ts2_name,ts2_usgs_data]]:
      times = [datetime.fromtimestamp(tstamp) for tstamp in data.times.value]
      ax.plot(times,data,lw=0.07)
      data_small = numpy.empty((0,2))
      for i in range(0,len(data),3600):
          data_small = numpy.vstack((data_small,[times[i],numpy.average(data[i:i+3600])]))
      ax.plot(data_small[:,0],data_small[:,1],lw=1,color='yellow')
      # ax.plot(numpy.arange(times[0],times[-1],timedelta(minutes=1)),usgs/1000,lw=1,color='orange')
      ax.xaxis.set_major_formatter(mdates.DateFormatter('%A\n%Y-%m-%d'))
      ax.xaxis.set_ticks(numpy.arange(times[0],times[-1],timedelta(days=7)))
      for t0 in numpy.arange(times[0]+timedelta(days=5),times[-1],timedelta(days=7)):
          t0 = t0.astype('M8[ms]').astype('O')
          ax.axvspan(t0,t0+timedelta(days=2),alpha=0.1,color='lime')
      if city=='Brooklyn':
        ax.axvspan(times[0]+timedelta(days=21),times[0]+timedelta(days=22),alpha=0.1,color='purple')
      ax.set_ylabel(r'%s Magnetic Field [$\mathrm{\mu T}$]'%city,labelpad=10,fontsize=12)
      ax.set_xlim(times[0],times[-1])
  fig.tight_layout()
  plt.savefig('timeseries.pdf')
  plt.show()
  plt.close()

def plot_dist(dict,xlim=[45,100]):
  """
  Examples
  --------
  >> dict = {'Berkeley':{'data':berkeley.value,
  >>                'color':'mediumpurple',
  >>                'fit': 'gauss',
  >>                'range':[48.8,50.3],
  >>                'xlim':[48.8,50.3],
  >>                'mode': 'gauss',
  >>                'daytime': [[0,1],[5,24]]
  >>                },
  >>    'Brooklyn':{'data':brooklyn.value,
  >>                'color':'indianred',
  >>                'fit': 'gauss',
  >>                'range':[90,94.5],
  >>                'xlim':[90,94.5],
  >>                'mode': 'gauss',
  >>                'daytime': [[9,20]]
  >>                }
  >>    }
  >> from nuri import plots
  >> plots.plot_dist(dict)
  """
  fig = plt.figure(figsize=(12,6),dpi=200)
  plt.subplots_adjust(left=0.12,right=0.97,bottom=0.1,top=0.95,hspace=0.22)
  ax = plt.subplot(211,xlim=xlim)
  for name in dict.keys():
    ax.hist(dict[name]['data'],bins=1000,label=name,range=xlim)
  ax.set_ylabel('Number of samples')
  ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
  ax.legend(loc='upper center',handlelength=2,handleheight=0.07)
  ax.set_yscale('log', nonposy='clip')
  for i,name in enumerate(dict.keys()):
    data = dict[name]['data']
    xlim = dict[name]['xlim']
    mode = dict[name]['mode']
    bins = 200
    ax = plt.subplot(2,2,3+i,xlim=xlim)
    hist = ax.hist(data,bins,range=dict[name]['range'],color='navy',alpha=0.333)
    day, night = day_and_night(data,dict[name]['daytime'])
    ax.hist(day,bins,range=dict[name]['range'],color='orangered',alpha=0.333)
    ax.hist(night,bins,range=dict[name]['range'],color='turquoise',alpha=0.333)
    x,y,y1,y2 = gaussian_fit(mode,data,bins,dict[name]['range'])
    ax.plot(x, y, lw=2, color='navy',label='Full day')
    ax.plot(x, y2, lw=2, color='orangered',label='Daytime')
    ax.plot(x, y1, lw=2, color='turquoise',label='Nighttime')
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), '.0e')))
    ax.set_xlabel(r'%s Magnetic Field [$\mathrm{\mu}$T]'%name)
    if i==1:
      ax.yaxis.tick_right()
    ax.legend(loc='best',handlelength=1,handleheight=0.07)
  plt.tight_layout()
  plt.savefig('distcomp.pdf')
  plt.show()
  plt.close()

def plot_dist_explore(dict):
  """
  Examples
  --------
  >> dict = {'Berkeley':{'data':berkeley.value,
  >>                  'xlim':[48.8,50.3],
  >>                  'mode': 'skew',
  >>                  'bins': 45
  >>                  },
  >>      'Brooklyn':{'data':brooklyn.value,
  >>                  'xlim':[90,94.5],
  >>                  'mode': 'gauss',
  >>                  'bins': 45
  >>                  }
  >>      }
  >> from nuri import plots
  >> plots.plot_dist_explore(dict)
  """
  fig,ax = plt.subplots(2,5,figsize=(12,6),dpi=300,sharex='row',sharey='row')
  plt.subplots_adjust(left=0.12,right=0.97,bottom=0.1,top=0.95,hspace=0.22)
  for i,name in enumerate(dict.keys()):
    bins = dict[name]['bins']
    data = dict[name]['data']
    xlim = dict[name]['xlim']
    mode = dict[name]['mode']
    daytime_loop = [[[0,1],[5,24]],[[6,23]],[[7,21]],[[8,19]],[[9,17]]]
    for n,daytime in enumerate(daytime_loop):
      hist = ax[i][n].hist(data,bins,range=xlim,color='navy',alpha=0.333,edgecolor='navy')
      day, night = day_and_night(data,daytime)
      ax[i][n].hist(day,bins,range=xlim,color='orangered',alpha=0.333)
      ax[i][n].hist(night,bins,range=xlim,color='turquoise',alpha=0.333)
      x,y,y1,y2 = gaussian_fit(mode,data,bins,xlim)
      ax[i][n].plot(x, y1, lw=2, color='orangered',label='Daytime')
      ax[i][n].plot(x, y, lw=2, color='navy',label='Full day')
      ax[i][n].plot(x, y2, lw=2, color='turquoise',label='Nighttime')
      ax[i][n].get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), '.0e')))
      if i==1 and n==2:
        ax[i][n].set_xlabel(r'Magnetic Field [$\mathrm{\mu}$T]')
      # ax[i][n].legend(loc='best',handlelength=1,handleheight=0.07)
      if n==0:
        ax[i][n].set_ylabel(name)
      if i==0:
        ax[i][n].set_title('5AM - 1AM' if n==0 else '%iAM - %iPM'%(daytime[0][0],daytime[0][1]-12))
      # if (i==0 and n=?h.set_linewidth('2')
  plt.tight_layout()
  plt.savefig('distcomp.pdf')
  plt.show()
  plt.close()

def plot_variance(dict):
  """
  Examples
  --------
  >> dict = [['Berkeley',berkeley],['Brooklyn',brooklyn]]
  >> from nuri import plots
  >> plots.plot_variance(dict)
  """
  fig = plt.figure(figsize=(12,4),dpi=200)
  for i,(name,data) in enumerate(dict):
    ax = plt.subplot(1,2,i+1,xlim=[0,24])
    for period,color in [['weekday','navy'],['weekend','gold']]:
      times,var = get_variance(data,period)
      plt.plot(times,var,color=color,label=period)
      plt.fill_between(times,var,color=color,alpha=0.2)
    if i==0:
      plt.ylabel(r'Daily Variance [$\mathrm{\mu T}^2$]',labelpad=10)
    plt.ylim(ymin=0)
    plt.xlabel(r'%s Time [hour]'%name,labelpad=10)
    plt.legend(loc='upper left',handlelength=1,handleheight=0.07)
  plt.tight_layout()
  plt.savefig('variance.pdf')
  plt.show()
  plt.close()

def wavelet_axes(ax,scales,spec,freq,xlim,fmin=None,fmax=None,vmin=None,vmax=None,cmap='bwr',swap=False,hidey=False):
  # Define minimum and maximum frequencies
  fmin_log,fmax_log = min(freq),max(freq)
  fmin_linear,fmax_linear = min(freq),max(freq)
  if fmin!=None:
    log_ratio = (numpy.log10(fmin)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
    fmin_linear = min(freq)+log_ratio*(max(freq)-min(freq))
    fmin_log = fmin
  if fmax!=None:
    log_ratio = (numpy.log10(fmax)-numpy.log10(min(freq)))/(numpy.log10(max(freq))-numpy.log10(min(freq)))
    fmax_linear = min(freq)+log_ratio*(max(freq)-min(freq))
    fmax_log = fmax
  # Get minimum and maximum amplitude in selected frequency range
  idx = numpy.where(numpy.logical_and(fmin_log<freq[::-1],freq[::-1]<fmax_log))[0]
  vmin = vmin if vmin!=None else numpy.sort(numpy.unique(spec[idx]))[1]
  vmax = spec[idx].max() if vmax==None else vmax
  # Build wavelet for both
  img = ax.imshow(spec,extent=[xlim[0],xlim[-1],freq[-1],freq[0]],
                  aspect='auto',interpolation='nearest',cmap=cmap,norm=colors.LogNorm(vmin,vmax))
  ax.set_xlim(xlim)
  ax.set_yscale('linear')
  ax.set_ylim(fmin_linear,fmax_linear)
  ax.grid(False)
  # Set up axis range for spectrogram
  twin_ax = ax.twinx()
  twin_ax.set_yscale('log')
  twin_ax.set_xlim(xlim)
  twin_ax.set_ylim(fmin_log,fmax_log)
  twin_ax.spines['top'].set_visible(False)
  twin_ax.spines['right'].set_visible(False)
  twin_ax.spines['bottom'].set_visible(False)
  ax.tick_params(which='both', labelleft=False, left=False)
  twin_ax.tick_params(which='both', labelleft=True,left=True, labelright=False, right=False)
  if swap:
    twin_ax.yaxis.tick_right()
  if hidey:
    plt.setp(twin_ax.get_yticklabels(), visible=False)
  twin_ax.grid(False)
  return img

def plot_dual_wave(data1,data1_full,data2,data2_full):
  fig = plt.figure(figsize=(12,6),dpi=300)
  ax1 = fig.add_axes([0.06,0.47,0.44,0.36])
  ax2 = fig.add_axes([0.51,0.47,0.44,0.36])
  ax3 = fig.add_axes([0.06,0.09,0.44,0.36],sharex=ax1,sharey=ax1)
  ax4 = fig.add_axes([0.51,0.09,0.44,0.36],sharex=ax2,sharey=ax2)
  cax = fig.add_axes([0.06,0.85,0.89,0.03])
  ax = [[ax1,ax2],[ax3,ax4]]
  plt.subplots_adjust(hspace=0.01,wspace=0.01)
  for i,dataset in enumerate([[data1,data1_full],[data2,data2_full]]):
    for n,data in enumerate(dataset):
      swap   = False   if n==0 else True
      length = 3600*24 if n==0 else 3960*60*5
      rate   = 1       if n==0 else 3960
      omega0 = 6
      dj     = 0.07    if n==0 else 0.1
      xlim   = [0,24]  if n==0 else [0,5]
      fmin   = 1/3960  if n==0 else 0.1
      vmin   = 1e-7
      vmax   = 1e4
      scales,freqs,spec = transform_data(data,length,sample_rate=rate,dj=dj,omega0=omega0)
      img = wavelet_axes(ax[i][n],scales,spec,freqs,xlim,fmin=fmin,vmin=vmin,vmax=vmax,cmap='Spectral_r',swap=swap)
    ax[i][0].set_ylabel('Frequency [Hz]',fontsize=15,labelpad=35)
    plt.setp(ax[0][i].get_xticklabels(), visible=False)
    if i==0:
      ax[1][i].set_xlabel('Monday Time [hour]',fontsize=15)
    else:
      ax[1][i].set_xlabel('Monday 9:00 to 9:05 AM [minute]',fontsize=15)
  cb = plt.colorbar(img,cax=cax,orientation="horizontal")
  cb.set_ticks(LogLocator())
  cb.mappable.set_clim(vmin,vmax)
  cb.set_label('Power $|\mathrm{W}_v|^2$ $[\mu T^2/\mathrm{Hz}]$',fontsize=15,labelpad=10)
  cax.xaxis.set_label_position('top')
  cax.xaxis.tick_top()
  plt.savefig('wavelet.png')
  plt.show()

def plot_samples(input_data):
  plt.style.use('seaborn')
  fig,ax = plt.subplots(3,5,figsize=(12,6),dpi=300)
  for i,(imin,imax,data) in enumerate(input_data):
    (imin,imax) = imin*200,imax*200
    data_y = data[imin:imax]
    y = data_y.value

    ax[0][i].plot(numpy.arange(imax-imin)/(200*60),y,color='black',lw=0.3)
    ax[0][i].fill_between(numpy.arange(imax-imin)/(200*60),y,color='navy',alpha=0.2)
    ax[0][i].set_xlim(0,8)
    ax[0][i].set_ylim(min(y),max(y))
    ax[0][i].set_xlabel('Time [min]')
    ax[0][i].xaxis.set_ticks([1,3,5,7])
    ax[0][i].xaxis.set_ticks([1,3,5,7])
    mean = (min(y)+max(y))//2
    diff = max(y)-min(y)
    # ax[0][i].yaxis.set_ticks([mean-diff//4,mean,mean+diff//4])
    ax[0][i].xaxis.set_label_position('top')
    ax[0][i].xaxis.tick_top()
    if i==0:
      ax[0][i].set_ylabel(r'Magnetic Field [$\mathrm{\mu T}$]')

    scales,freqs,spec = transform_data(data_y,200*60*8,sample_rate=200,dj=0.1,omega0=6)
    img = wavelet_axes(ax[1][i],scales,spec,freqs,[0,8],fmin=0.005,vmin=1e-6,vmax=1e5,cmap='Spectral_r',hidey=True if i>0 else False)
    plt.setp(ax[1][i].get_xticklabels(), visible=False)
    if i==0:
      ax[1][i].set_ylabel('Frequency [Hz]',labelpad=30)

    f, Pxx_den = signal.welch(data.value[imin:imax], 200, nperseg=500)
    ax[2][i].semilogy(f,Pxx_den,color='black',lw=0.5)
    ax[2][i].fill_between(f,Pxx_den,color='gold',alpha=0.2)
    ax[2][i].xaxis.set_ticks([20,40,60,80])
    ax[2][i].yaxis.set_ticks([1e-6,1e-3,1])
    ax[2][i].set_xlim(0,100)
    ax[2][i].set_ylim(1e-8,100)
    ax[2][i].set_xlabel('Frequency [Hz]')
    if i==0:
      ax[2][i].set_ylabel(r'PSD [$\mathrm{\mu T}^2/\mathrm{Hz}$]')
    else:
      plt.setp(ax[2][i].get_yticklabels(), visible=False)

  plt.tight_layout(w_pad=0.2, h_pad=0.1)
  plt.savefig('samples')
  plt.show()
  plt.close()
