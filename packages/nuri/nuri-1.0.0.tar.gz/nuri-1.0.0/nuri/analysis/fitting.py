import numpy, math
from scipy.optimize import curve_fit
from scipy import special

class GaussianFit:
  """
  Fit Gaussian profile(s) to the distribution of magnetic field data.

  Examples
  --------
  >>> data = nuri.get_data('2016-3-14','2016-4-11','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
  >>> x,y,y1,y2 = nuri.gaussian_fit(mode='gauss',data=data.value,bins=45,xlim=[48.8,50.3],order=2)
  1/2 Gaussian : amp=140184.97, mu=49.55, sigma=0.212
  2/2 Gaussian : amp=38811.87, mu=49.85, sigma=0.054
  """
  def __init__(self,data,bins,xlim,order=1,reference=[]):
    """
    Initialize Gaussian fitting class. When 2 Gaussian profiles are
    being fitted, i.e., ``order`` is equal to 2, and a reference
    dataset is provide, a single Gaussian profile will first be
    fitted to the reference data; a double Gaussian profile will then
    be fitted to the entire input dataset with the parameters from the
    reference profile being fixed.

    Parameters
    ----------
    data : :class:`numpy.ndarray`
      Input magnetic field data.
    bins : :class:`int`
      Number of bins in the histogram.
    xlim : :class:`list` [ :class:`float` ]
      Range to generate histograms from the data.
    order : :class:`int`
      Number of Gaussian profiles to fit the data with.
    reference : :class:`list` [ :class:`float` ]
      Reference dataset to fit the first Gaussian profile.
    """
    self.xlim = xlim
    self.order = order
    hist = numpy.histogram(data,bins,range=xlim)
    x = numpy.array([0.5 * (hist[1][i] + hist[1][i+1]) for i in range(len(hist[1])-1)])
    y = hist[0]
    params = [max(y)/2,numpy.mean(data),numpy.std(data)]*order
    self.reference = reference
    if len(reference)>0:
      self.reference = GaussianFit(reference,bins,xlim).get_params()
      params = params[3:]
    self.gauss_fit(x,y,params)

  def gauss_single(self,x,amp,mu,sigma):
    return (amp * numpy.exp(-(x - mu)**2.0 / (2 * sigma**2)))

  def gauss_fct(self,x,*params):
    gauss = 0
    for i in range(self.order):
      if i==0 and self.reference!=[]:
        amp, mu, sigma = self.reference
      else:
        idx = i if self.reference==[] else i-1
        amp, mu, sigma = params[idx*3:idx*3+3]
      gauss += self.gauss_single(x, amp, mu, sigma)
    return gauss

  def gauss_fit(self,x,y,params):
    popt, pcov = curve_fit(self.gauss_fct,x,y,p0=params)
    print('1/%i Gaussian : amp=%.2f, mu=%.2f, sigma=%.3f'%(self.order,popt[0],popt[1],abs(popt[2])))
    if self.order>1 and self.reference==[]:
      print('2/%i Gaussian : amp=%.2f, mu=%.2f, sigma=%.3f'%(self.order,popt[3],popt[4],abs(popt[5])))
    self.popt = self.reference+list(popt)

  def get_params(self):
    return self.popt

  def get_fit(self):
    self.reference = []
    x = numpy.arange(*self.xlim,0.001)
    y = self.gauss_fct(x, *self.popt)
    if self.order==1:
      return x,y
    else:
      y1 = self.gauss_single(x, *self.popt[:3])
      y2 = self.gauss_single(x, *self.popt[3:])
      return x,y,y1,y2

class SkewedGaussianFit:
  """
  Fitting data distribution with skewed Gaussian profiles.
  """
  def __init__(self,data,bins,xlim,order=1,reference=[]):
    self.xlim = xlim
    self.order = order
    hist = numpy.histogram(data,bins,range=xlim)
    x = numpy.array([0.5 * (hist[1][i] + hist[1][i+1]) for i in range(len(hist[1])-1)])
    y = hist[0]
    skewness = -5
    params = [max(y)/3,numpy.mean(data),numpy.std(data),skewness]*order
    # popt = [2e4, 49.5, 0.2, 2e4, 50, 0.2, -5]
    self.reference = reference
    if len(reference)>0:
      self.reference = SkewedGaussianFit(reference,bins,xlim).get_params()
      params = params[4:]
    self.skew_fit(x,y,params)

  def skew_single(self, x, amp, mu, sigma, skewness):
    r"""A skewed Gaussian model, using a skewed normal distribution.
    The model has four Parameters: `amplitude` (:math:`A`), `center`
    (:math:`\mu`), `sigma` (:math:`\sigma`), and `gamma` (:math:`\gamma`).

    .. math::

        f(x; A, \mu, \sigma, \gamma) = \frac{A}{\sigma\sqrt{2\pi}}
        e^{[{-{(x-\mu)^2}/{{2\sigma}^2}}]} \Bigl\{ 1 +
        {\operatorname{erf}}\bigl[
        \frac{{\gamma}(x-\mu)}{\sigma\sqrt{2}}
        \bigr] \Bigr\}

    where :func:`erf` is the error function.
    For more information, see:
    https://en.wikipedia.org/wiki/Skew_normal_distribution
    """
    normpdf = (amp / (sigma * numpy.sqrt(2 * math.pi))) * numpy.exp(-(numpy.power((x - mu), 2) / (2 * numpy.power(sigma, 2))))
    normcdf = (1 + special.erf((skewness * ((x - mu) / sigma)) / (numpy.sqrt(2))))
    return normpdf * normcdf

  def skew_fct(self, x, *params):
    skew = 0
    for i in range(self.order):
      if i==0 and self.reference!=[]:
        amp, mu, sigma, skewness = self.reference
      else:
        idx = i if self.reference==[] else i-1
        amp, mu, sigma, skewness = params[idx*4:idx*4+4]
      skew += self.skew_single(x, amp, mu, sigma, skewness)
    return skew

  def skew_fit(self,x,y,params):
    popt, pcov = curve_fit(self.skew_fct,x,y,p0=params)
    perr = numpy.sqrt(numpy.diag(pcov))
    print('1/%i Gaussian (skewed) : amp=%i±%i, mu=%.3f±%.3f, sigma=%.3f±%.3f, skewness=%.2f±%.2f'%(self.order,popt[0],perr[0],popt[1],perr[1],popt[2],perr[2],popt[3],perr[3]))
    if self.order>1 and self.reference==[]:
      print('2/%i Gaussian (skewed) : amp=%i±%i, mu=%.3f±%.3f, sigma=%.3f±%.3f, skewness=%.2f±%.2f'%(self.order,popt[4],perr[4],popt[5],perr[5],popt[6],perr[6],popt[7],perr[7]))
    self.popt = self.reference+list(popt)

  def get_params(self):
    return self.popt

  def get_fit(self):
    self.reference = []
    x = numpy.arange(*self.xlim,0.001)
    y = self.skew_fct(x, *self.popt)
    if self.order==1:
      return x,y
    else:
      y1 = self.skew_single(x, *self.popt[:4])
      y2 = self.skew_single(x, *self.popt[4:])
      return x,y,y1,y2

class MixedGaussianFit:

  def __init__(self,data,bins,xlim,reference=[]):
    self.xlim = xlim
    hist = numpy.histogram(data,bins,range=xlim)
    x = numpy.array([0.5 * (hist[1][i] + hist[1][i+1]) for i in range(len(hist[1])-1)])
    y = hist[0]
    skewness = -5
    params = [max(y)/3,numpy.mean(data),numpy.std(data)]
    params+= [max(y)/3,numpy.mean(data),numpy.std(data),skewness]
    # popt = [2e4, 49.5, 0.2, 2e4, 50, 0.2, -5]
    self.reference = reference
    if len(reference)>0:
      self.reference = GaussianFit(reference,bins,xlim).get_params()
    self.mix_fit(x,y,params)

  def gauss_fct(self,x,*params):
    amp, mu, sigma = params[:3]
    if self.reference!=[]:
      amp, mu, sigma = self.reference
    return (amp * numpy.exp(-(x - mu)**2.0 / (2 * sigma**2)))

  def skew_fct(self, x, *params):
    amp, mu, sigma, gamma = params[3:]
    normpdf = (amp / (sigma * numpy.sqrt(2 * math.pi))) * numpy.exp(-(numpy.power((x - mu), 2) / (2 * numpy.power(sigma, 2))))
    normcdf = (1 + special.erf((gamma * ((x - mu) / sigma)) / (numpy.sqrt(2))))
    return normpdf * normcdf

  def mix_fct(self, x, *params):
    gauss = self.gauss_fct(x,*params)
    skew = self.skew_fct(x,*params)
    return gauss + skew

  def mix_fit(self,x,y,params):
    popt, pcov = curve_fit(self.mix_fct,x,y,p0=params)
    print('1/2 Gaussian : amp=%.2f, mu=%.2f, sigma=%.3f'%(popt[0],popt[1],abs(popt[2])))
    print('2/2 Gaussian (skewed) : amp=%.2f, mu=%.2f, sigma=%.3f, skewness=%3f'%(popt[3],popt[4],popt[5],popt[6]))
    self.popt = popt

  def get_fit(self):
    x = numpy.arange(*self.xlim,0.001)
    y = self.mix_fct(x, *self.popt)
    y1 = self.gauss_fct(x, *self.popt)
    y2 = self.skew_fct(x, *self.popt)
    return x,y,y1,y2

class IndSkewedGaussian:
  """
  Fitting independently day and night distributions using
  skewed Gaussian profiles.

  Examples
  --------
  >>> data = nuri.get_data('2016-3-14','2016-4-11','/content/drive/MyDrive/CityMagData/1Hz',station=2,sensor='biomed',scalar=True)
  >>> day, night = nuri.day_and_night(data.value,daytime=[[0,1],[4.5,24]])
  >>> x,y,y1,y2 = nuri.gaussian_fit(mode='indskew',data=data.value,bins=45,xlim=[48.8,50.3],order=2,reference=[day,night]).get_fit()
  1/1 Gaussian (skewed) : amp=67980.04, mu=49.36, sigma=0.281, skewness=1.393503
  1/1 Gaussian (skewed) : amp=11488.11, mu=49.92, sigma=0.212, skewness=-4.605114
  """
  def __init__(self,data,bins,xlim,order=1,reference=[]):
    self.xlim = xlim
    self.order = order
    hist = numpy.histogram(data,bins,range=xlim)
    x = numpy.array([0.5 * (hist[1][i] + hist[1][i+1]) for i in range(len(hist[1])-1)])
    y = hist[0]
    self.popt = []
    for ref in reference:
      self.popt.extend(SkewedGaussianFit(ref,bins,xlim).get_params())

  def skew_single(self, x, amp, mu, sigma, skewness):
    normpdf = (amp / (sigma * numpy.sqrt(2 * math.pi))) * numpy.exp(-(numpy.power((x - mu), 2) / (2 * numpy.power(sigma, 2))))
    normcdf = (1 + special.erf((skewness * ((x - mu) / sigma)) / (numpy.sqrt(2))))
    return normpdf * normcdf

  def skew_fct(self, x, *params):
    skew = 0
    for i in range(self.order):
      amp, mu, sigma, skewness = params[i*4:i*4+4]
      skew += self.skew_single(x, amp, mu, sigma, skewness)
    return skew

  def get_fit(self):
    x = numpy.arange(*self.xlim,0.001)
    y = self.skew_fct(x, *self.popt)
    if self.order==1:
      return x,y
    else:
      y1 = self.skew_single(x, *self.popt[:4])
      y2 = self.skew_single(x, *self.popt[4:])
      return x,y,y1,y2
    
def gaussian_fit(mode,data,bins,xlim,order=2,reference=[]):
  """
  
  """
  if mode=='gauss':
    return GaussianFit(data,bins,xlim,order,reference).get_fit()
  if mode=='skew':
    return SkewedGaussianFit(data,bins,xlim,order,reference).get_fit()
  if mode=='indskew':
    return IndSkewedGaussian(data,bins,xlim,order,reference).get_fit()
  if mode=='mixed':
    return MixedGaussianFit(data,bins,xlim,reference).get_fit()
