



























from __future__ import print_function, division

import sys
import math
import cmath
import os
import numpy as np
import struct
import re
import h5py
import urllib2

from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from scipy.stats import hmean
from scipy.misc import logsumexp

from types import StringType, FloatType


ARCSECTORAD = float('4.8481368110953599358991410235794797595635330237270e-6')
RADTOARCSEC = float('206264.80624709635515647335733077861319665970087963')
SECTORAD    = float('7.2722052166430399038487115353692196393452995355905e-5')
RADTOSEC    = float('13750.987083139757010431557155385240879777313391975')
RADTODEG    = float('57.295779513082320876798154814105170332405472466564')
DEGTORAD    = float('1.7453292519943295769236907684886127134428718885417e-2')
RADTOHRS    = float('3.8197186342054880584532103209403446888270314977710')
HRSTORAD    = float('2.6179938779914943653855361527329190701643078328126e-1')
PI          = float('3.1415926535897932384626433832795028841971693993751')
TWOPI       = float('6.2831853071795864769252867665590057683943387987502')
PIBYTWO     = float('1.5707963267948966192313216916397514420985846996876')
SECPERDAY   = float('86400.0')
SECPERJULYR = float('31557600.0')
KMPERPC     = float('3.0856776e13')
KMPERKPC    = float('3.0856776e16')
Tsun        = float('4.925490947e-6') 
Msun        = float('1.9891e30')      
Mjup        = float('1.8987e27')      
Rsun        = float('6.9551e8')       
Rearth      = float('6.378e6')        
SOL         = float('299792458.0')    
MSUN        = float('1.989e+30')      
G           = float('6.673e-11')      
C           = SOL
KPC         = float('3.0856776e19')   
I38         = float('1e38')           


def rad_to_dms(rad):
  """
  rad_to_dms(rad):
     Convert radians to degrees, minutes, and seconds of arc.
  """
  if (rad < 0.0): sign = -1
  else: sign = 1
  arc = RADTODEG * np.fmod(np.fabs(rad), math.pi)
  d = int(arc)
  arc = (arc - d) * 60.0
  m = int(arc)
  s = (arc - m) * 60.0
  if sign==-1 and d==0:
    return (sign * d, sign * m, sign * s)
  else:
    return (sign * d, m, s)

def dms_to_rad(deg, mins, sec):
  """
  dms_to_rad(deg, min, sec):
     Convert degrees, minutes, and seconds of arc to radians.
  """
  if (deg < 0.0):
    sign = -1
  elif (deg==0.0 and (mins < 0.0 or sec < 0.0)):
    sign = -1
  else:
    sign = 1
  return sign * ARCSECTORAD * \
    (60.0 * (60.0 * np.fabs(deg) + np.fabs(mins)) + np.fabs(sec))

def dms_to_deg(deg, mins, sec):
  """
  dms_to_deg(deg, min, sec):
     Convert degrees, minutes, and seconds of arc to degrees.
  """
  return RADTODEG * dms_to_rad(deg, mins, sec)

def rad_to_hms(rad):
  """
  rad_to_hms(rad):
     Convert radians to hours, minutes, and seconds of arc.
  """
  rad = np.fmod(rad, 2.*math.pi)
  if (rad < 0.0): rad = rad + 2.*math.pi
  arc = RADTOHRS * rad
  h = int(arc)
  arc = (arc - h) * 60.0
  m = int(arc)
  s = (arc - m) * 60.0
  return (h, m, s)

def hms_to_rad(hour, mins, sec):
  """
  hms_to_rad(hour, min, sec):
     Convert hours, minutes, and seconds of arc to radians
  """
  if (hour < 0.0): sign = -1
  else: sign = 1
  return sign * SECTORAD * \
         (60.0 * (60.0 * np.fabs(hour) + np.fabs(mins)) + np.fabs(sec))

def coord_to_string(h_or_d, m, s):
  """
  coord_to_string(h_or_d, m, s):
     Return a formatted string of RA or DEC values as
     'hh:mm:ss.ssss' if RA, or 'dd:mm:ss.ssss' if DEC.
  """
  retstr = ""
  if h_or_d < 0:
    retstr = "-"
  elif abs(h_or_d)==0:
    if (m < 0.0) or (s < 0.0):
      retstr = "-"

  h_or_d, m, s = abs(h_or_d), abs(m), abs(s)
  if (s >= 9.9995):
    return retstr+"%.2d:%.2d:%.4f" % (h_or_d, m, s)
  else:
    return retstr+"%.2d:%.2d:0%.4f" % (h_or_d, m, s)

def rad_to_string(rad, ra_or_dec):
  """
  rad_to_string(rad, ra_or_dec):
     Convert an angle in radians to hours/degrees, minutes seconds and output
     it as a string in the format 'hh:mm:ss.ssss' if RA, or 'dd:mm:ss.ssss' if DEC.
     Whether to use hours or degrees is set by whether ra_or_dec is 'RA' or 'DEC'
  """
  if ra_or_dec.upper() == 'RA':
    v, m, s = rad_to_hms(rad)
  elif ra_or_dec.upper() == 'DEC':
    v, m, s = rad_to_dms(rad)
  else:
    raise("Unrecognised option: Expected 'ra_or_dec' to be 'RA' or 'DEC'")

  return coord_to_string(v, m, s)

def ra_to_rad(ra_string):
  """
  ra_to_rad(ar_string):
     Given a string containing RA information as
     'hh:mm:ss.ssss', return the equivalent decimal
     radians. Also deal with cases where input
     string is just hh:mm, or hh.
  """
  hms = ra_string.split(":")
  if len(hms) == 3:
    return hms_to_rad(int(hms[0]), int(hms[1]), float(hms[2]))
  elif len(hms) == 2:
    return hms_to_rad(int(hms[0]), int(hms[1]), 0.0)
  elif len(hms) == 1:
    return hms_to_rad(float(hms[0]), 0.0, 0.0)
  else:
    print("Problem parsing RA string %s" % ra_string, file=sys.stderr)
    sys.exit(1)

def dec_to_rad(dec_string):
  """
  dec_to_rad(dec_string):
     Given a string containing DEC information as
     'dd:mm:ss.ssss', return the equivalent decimal
     radians. Also deal with cases where input string
     is just dd:mm or dd
  """
  dms = dec_string.split(":")
  if "-" in dms[0] and float(dms[0]) == 0.0:
    m = '-'
  else:
    m = ''

  if len(dms) == 3:
    return dms_to_rad(int(dms[0]), int(m+dms[1]), float(m+dms[2]))
  elif len(dms) == 2:
    return dms_to_rad(int(dms[0]), int(m+dms[1]), 0.0)
  elif len(dms) == 1:
    return dms_to_rad(float(dms[0]), 0.0, 0.0)
  else:
    print("Problem parsing DEC string %s" % dec_string, file=sys.stderr)
    sys.exit(1)

def p_to_f(p, pd, pdd=None):
  """
  p_to_f(p, pd, pdd=None):
    Convert period, period derivative and period second
    derivative to the equivalent frequency counterparts.
    Will also convert from f to p.
  """
  f = 1.0 / p
  fd = -pd / (p * p)
  if (pdd==None):
    return [f, fd]
  else:
    if (pdd==0.0):
      fdd = 0.0
    else:
      fdd = 2.0 * pd * pd / (p**3.0) - pdd / (p * p)

    return [f, fd, fdd]

def pferrs(porf, porferr, pdorfd=None, pdorfderr=None):
  """
  pferrs(porf, porferr, pdorfd=None, pdorfderr=None):
     Calculate the period or frequency errors and
     the pdot or fdot errors from the opposite one.
  """
  if (pdorfd==None):
    return [1.0 / porf, porferr / porf**2.0]
  else:
    forperr = porferr / porf**2.0
    fdorpderr = np.sqrt((4.0 * pdorfd**2.0 * porferr**2.0) / porf**6.0 +
                          pdorfderr**2.0 / porf**4.0)
    [forp, fdorpd] = p_to_f(porf, pdorfd)

    return [forp, forperr, fdorpd, fdorpderr]



float_keys = ["F", "F0", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
              "PEPOCH", "POSEPOCH", "DM", "START", "FINISH", "NTOA",
              "TRES", "TZRMJD", "TZRFRQ", "TZRSITE", "NITS",
              "A1", "XDOT", "E", "ECC", "EDOT", "T0", "PB", "PBDOT", "OM",
              "OMDOT", "EPS1", "EPS2", "EPS1DOT", "EPS2DOT", "TASC", "LAMBDA",
              "BETA", "RA_RAD", "DEC_RAD", "GAMMA", "SINI", "M2", "MTOT",
              "FB0", "FB1", "FB2", "ELAT", "ELONG", "PMRA", "PMDEC", "DIST",
              "PB_2", "PB_3", "T0_2", "T0_3", "A1_2", "A1_3", "OM_2", "OM_3",
              "ECC_2", "ECC_3", "DIST", "PX", "KIN", "KOM", "A0", "B0", "D_AOP",
              
              "H0", "COSIOTA", "PSI", "PHI0", "THETA", "I21", "I31", "C22", "HPLUS", "HCROSS",
              "C21", "PHI22", "PHI21", "SNR", "COSTHETA", "IOTA", "Q22"]
str_keys = ["FILE", "PSR", "PSRJ", "NAME", "RAJ", "DECJ", "RA", "DEC", "EPHEM",
            "CLK", "BINARY", "UNITS"]

class psr_par:
  def __init__(self, parfilenm):
    """
    This class parses a TEMPO(2)-style pulsar parameter file. If possible all parameters
    are converted into SI units and angles are in radians. Epochs will be converted from
    MJD values into GPS times.
    """
    self.FILE = parfilenm
    pf = open(parfilenm)
    for line in pf.readlines():
      
      if not line.strip():
        continue

      
      line = line.replace("D-", "E-")
      line = line.replace("D+", "E+")
      
      line = line.replace("d-", "e-")
      line = line.replace("d+", "e+")
      splitline = line.split()

      
      key = splitline[0].upper()

      if key in str_keys:
        setattr(self, key, splitline[1])
      elif key in float_keys:
        try:
          setattr(self, key, float(splitline[1]))
        except:
          continue

      if len(splitline)==3: 
        if splitline[2] not in ['0', '1']:
          setattr(self, key+'_ERR', float(splitline[2]))
          setattr(self, key+'_FIT', 0) 

      if len(splitline)==4:
        if splitline[2] == '1': 
          setattr(self, key+'_FIT', 1)
        else:
          setattr(self, key+'_FIT', 0)
        setattr(self, key+'_ERR', float(splitline[3]))

    
    if hasattr(self, 'RAJ'):
      setattr(self, 'RA_RAD', ra_to_rad(self.RAJ))

      
      if hasattr(self, 'RAJ_ERR'):
        setattr(self, 'RA_RAD_ERR', hms_to_rad(0, 0, self.RAJ_ERR))

        if hasattr(self, 'RAJ_FIT'):
          setattr(self, 'RA_RAD_FIT', self['RAJ_FIT'])
    if hasattr(self, 'DECJ'):
      setattr(self, 'DEC_RAD', dec_to_rad(self.DECJ))

      
      if hasattr(self, 'DECJ_ERR'):
        setattr(self, 'DEC_RAD_ERR', dms_to_rad(0, 0, self.DECJ_ERR))

        if hasattr(self, 'DECJ_FIT'):
          setattr(self, 'DEC_RAD_FIT', self['DECJ_FIT'])

    
    for pv in ['RA', 'DEC']:
      if hasattr(self, 'PM'+pv):
        pmv = self['PM'+pv]
        setattr(self, 'PM'+pv+'_ORIGINAL', pmv) 
        setattr(self, 'PM'+pv , pmv*np.pi/(180.*3600.e3*365.25*86400.))

        if hasattr(self, 'PM'+pv+'_ERR'):
          pmve = self['PM'+pv+'_ERR']
          setattr(self, 'PM'+pv+'_ERR_ORIGINAL', pmv) 
          setattr(self, 'PM'+pv+'_ERR' , pmve*np.pi/(180.*3600.e3*365.25*86400.))

    
    if hasattr(self, 'P'):
      setattr(self, 'P0', self.P)
    if hasattr(self, 'P0'):
      setattr(self, 'F0', 1.0/self.P0)
    if hasattr(self, 'F0'):
      setattr(self, 'P0', 1.0/self.F0)
    if hasattr(self, 'FB0'):
      setattr(self, 'PB', (1.0/self.FB0)/86400.0)
    if hasattr(self, 'P0_ERR'):
      if hasattr(self, 'P1_ERR'):
        f, ferr, fd, fderr = pferrs(self.P0, self.P0_ERR,
                                       self.P1, self.P1_ERR)
        setattr(self, 'F0_ERR', ferr)
        setattr(self, 'F1', fd)
        setattr(self, 'F1_ERR', fderr)
      else:
        if hasattr(self, 'P1'):
          f, fd, = p_to_f(self.P0, self.P1)
          setattr(self, 'F0_ERR', self.P0_ERR/(self.P0*self.P0))
          setattr(self, 'F1', fd)
    if hasattr(self, 'F0_ERR'):
      if hasattr(self, 'F1_ERR'):
        p, perr, pd, pderr = pferrs(self.F0, self.F0_ERR,
                                    self.F1, self.F1_ERR)
        setattr(self, 'P0_ERR', perr)
        setattr(self, 'P1', pd)
        setattr(self, 'P1_ERR', pderr)
      else:
        if hasattr(self, 'F1'):
          p, pd, = p_to_f(self.F0, self.F1)
          setattr(self, 'P0_ERR', self.F0_ERR/(self.F0*self.F0))
          setattr(self, 'P1', pd)

    
    try:
      import lalpulsar
      for epoch in ['PEPOCH', 'POSEPOCH', 'DMEPOCH', 'T0', 'TASC', 'T0_2', 'T0_3']:
        if hasattr(self, epoch):
          setattr(self, epoch+'_ORIGINAL', self[epoch]) 
          setattr(self, epoch, lalpulsar.TTMJDtoGPS(self[epoch]))

          if hasattr(self, epoch+'_ERR'): 
            setattr(self, epoch+'_ERR_ORIGINAL', self[epoch+'_ERR']) 
            setattr(self, epoch+'_ERR', self[epoch+'_ERR'] * SECPERDAY)
    except:
      print("Could not convert epochs to GPS times. They are all still MJD values.", file=sys.stderr)

    
    convfacs = {'DIST': KPC, 'PX': 1e-3*ARCSECTORAD}
    for item in convfacs:
      if hasattr(self, item): 
        setattr(self, item+'_ORIGINAL', self[item]) 
        setattr(self, item, self[item] * convfacs[item])

        if hasattr(self, item+'_ERR'):
          setattr(self, item+'_ERR_ORIGINAL', self[item+'_ERR']) 
          setattr(self, item+'_ERR', self[item+'_ERR'] * convfacs[item])

    
    
    for om in ['OM', 'OM_2', 'OM_3', 'KIN', 'KOM']:
      if hasattr(self, om): 
        setattr(self, om, self[om] / RADTODEG )

        if hasattr(self, om+'_ERR'):
          setattr(self, om+'_ERR', self[om+'_ERR'] / RADTODEG )

    
    for pb in ['PB', 'PB_2', 'PB_3']:
      if hasattr(self, pb): 
        setattr(self, pb+'_ORIGINAL', self[pb]) 
        setattr(self, pb, self[pb] * SECPERDAY)

        if hasattr(self, pb+'_ERR'):
          setattr(self, pb+'_ERR_ORIGINAL', self[pb+'_ERR']) 
          setattr(self, pb+'_ERR', self[pb+'_ERR'] * SECPERDAY)

    
    if hasattr(self, 'OMDOT'): 
      setattr(self, 'OMDOT_ORIGINAL', self['OMDOT']) 
      setattr(self, 'OMDOT', self['OMDOT'] / (RADTODEG * 365.25 * SECPERDAY))

      if hasattr(self, 'OMDOT_ERR'):
        setattr(self, 'OMDOT_ERR_ORIGINAL', self['OMDOT_ERR']) 
        setattr(self, 'OMDOT_ERR', self['OMDOT_ERR'] / (RADTODEG * 365.25 * SECPERDAY))

    if hasattr(self, 'EPS1') and hasattr(self, 'EPS2'):
      ecc = math.sqrt(self.EPS1 * self.EPS1 + self.EPS2 * self.EPS2)
      omega = math.atan2(self.EPS1, self.EPS2)
      setattr(self, 'E', ecc)
      setattr(self, 'OM', omega) 
      setattr(self, 'T0', self.TASC + self.PB * omega/TWOPI)
    if hasattr(self, 'PB') and hasattr(self, 'A1') and not (hasattr(self, 'E') or hasattr(self, 'ECC')):
      setattr(self, 'E', 0.0)
    if hasattr(self, 'T0') and not hasattr(self, 'TASC') and hasattr(self, 'OM') and hasattr(self, 'PB'):
      setattr(self, 'TASC', self.T0 - self.PB * self.OM/TWOPI)

    
    for binu in ['XDOT', 'PBDOT', 'EDOT', 'EPS1DOT', 'EPS2DOT', 'XPBDOT']:
      if hasattr(self, binu):
        setattr(self, binu+'_ORIGINAL', self[binu]) 
        if np.abs(self[binu]) > 1e-7:
          setattr(self, binu, self[binu] * 1.0e-12)

          
          if self[binu] > 10000.: 
            setattr(self, binu, 0.0)

    
    for mass in ['M2', 'MTOT']:
      if hasattr(self, mass): 
        setattr(self, mass+'_ORIGINAL', self[mass]) 
        setattr(self, mass, self[mass]*MSUN)

        if hasattr(self, mass+'_ERR'):
          setattr(self, mass+'_ERR_ORIGINAL', self[mass+'_ERR']) 
          setattr(self, mass+'_ERR', self[mass+'_ERR'] * MSUN)

    
    if hasattr(self, 'D_AOP'): 
      setattr(self, 'D_AOP_ORIGINAL', self['D_AOP']) 
      setattr(self, 'D_AOP', self['D_AOP'] * RADTODEG * 3600. )

    pf.close()

  def __getitem__(self, key):
    try:
      par = getattr(self, key)
    except:
      par = None

    return par

  def __str__(self):
    out = ""
    for k, v in self.__dict__.items():
      if k[:2]!="__":
        if type(self.__dict__[k]) is StringType:
          out += "%10s = '%s'\n" % (k, v)
        else:
          out += "%10s = %-20.15g\n" % (k, v)

    return out


class psr_prior:
  def __init__(self, priorfilenm):
    self.FILE = priorfilenm
    pf = open(priorfilenm)
    for line in pf.readlines():
      splitline = line.split()

      
      key = splitline[0].upper()

      if key in str_keys:
        
        setattr(self, key, [float(splitline[2]), float(splitline[3])])
      elif key in float_keys:
        setattr(self, key, [float(splitline[2]), float(splitline[3])])

    
    if hasattr(self, 'RA'):
      hl, ml, sl = rad_to_hms(self.RA[0])
      rastrl = coord_to_string(hl, ml, sl)
      hu, mu, su = rad_to_hms(self.RA[1])
      rastru = coord_to_string(hu, mu, su)
      setattr(self, 'RA_STR', [rastrl, rastru])

    if hasattr(self, 'DEC'):
      dl, ml, sl = rad_to_dms(self.DEC[0])
      decstrl = coord_to_string(dl, ml, sl)
      du, mu, su = rad_to_dms(self.DEC[1])
      decstru = coord_to_string(du, mu, su)
      setattr(self, 'DEC_STR', [decstrl, decstru])

    pf.close()

  def __getitem__(self, key):
    try:
      atr = getattr(self, key)
    except:
      atr = None

    return atr

  def __str__(self):
    out = ""
    for k, v in self.__dict__.items():
      if k[:2]!="__":
        out += "%10s = %-20.15g, %-20.15g\n" % (k, float(v[0]), float(v[1]))

    return out





def spin_down_limit(freq, fdot, dist):
  hsd = math.sqrt((5./2.)*(G/C**3)*I38*math.fabs(fdot)/freq)/(dist*KPC)

  return hsd




def h0_to_ellipticity(h0, freq, dist):
  ell = h0*C**4.*dist*KPC/(16.*math.pi**2*G*I38*freq**2)

  return ell



def h0_to_quadrupole(h0, freq, dist):
  q22 = math.sqrt(15./(8.*math.pi))*h0*C**4.*dist*KPC/(16.*math.pi**2*G*freq**2)

  return q22




def phipsiconvert(phipchain, psipchain):
  chainlen=len(phipchain)

  phichain = []
  psichain = []

  theta = math.atan2(1,2);
  ct = math.cos(theta);
  st = math.sin(theta);

  for i in range(0,chainlen):
    phi0 = (1/(2*st))*phipchain[i] - (1/(2*st))*psipchain[i];
    psi = (1/(2*ct))*phipchain[i] + (1/(2*ct))*psipchain[i];

    
    if math.fabs(psi) > math.pi/4.:
      
      phi0 = phi0 + math.pi;

      
      if psi > math.pi/4.:
        psi = -(math.pi/4.) + math.fmod(psi+(math.pi/4.), math.pi/2.);
      else:
        psi = (math.pi/4.) - math.fmod((math.pi/4.)-psi, math.pi/2.);

    
    if phi0 > 2.*math.pi:
      phi0 = math.fmod(phi0, 2.*math.pi);
    else:
      phi0 = 2.*math.pi - math.fmod(2.*math.pi-phi0, 2.*math.pi);

    phichain.append(phi0)
    psichain.append(psi)

  return phichain, psichain





def plot_posterior_hist(poslist, param, ifos,
                        parambounds=[float("-inf"), float("inf")],
                        nbins=50, upperlimit=0, overplot=False,
                        parfile=None, mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt
  from lalapps.pulsarhtmlutils import paramlatexdict

  
  myfigs = []

  
  ulvals = []

  
  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'serif',
      'font.size': 12 }

  matplotlib.rcParams.update(mplparams)

  
  coldict = {'H1': 'r', 'H2': 'c', 'L1': 'g', 'V1': 'b', 'G1': 'm', 'Joint':'k'}

  
  try:
    paraxis = paramlatexdict[param.upper()]
  except:
    paraxis = param

  ymax = []

  
  
  parval = None
  if parfile:
    parval = parfile[param.upper()]

  if ifos == None:
    
    ifos = ['H1']

  
  for idx, ifo in enumerate(ifos):
    
    if overplot and idx == 0:
      myfig = plt.figure(figsize=(4,4),dpi=200)
      plt.hold(True)
    elif not overplot:
      myfig = plt.figure(figsize=(4,4),dpi=200)

    pos = poslist[idx]

    pos_samps = pos[param].samples

    
    n, bins = hist_norm_bounds( pos_samps, int(nbins), parambounds[0], \
                                parambounds[1] )

    
    plt.step(bins, n, color=coldict[ifo])

    if 'h0' not in param:
      plt.xlim(parambounds[0], parambounds[1])

    plt.xlabel(r''+paraxis, fontsize=14, fontweight=100)
    plt.ylabel(r'Probability Density', fontsize=14, fontweight=100)
    myfig.subplots_adjust(left=0.18, bottom=0.15) 

    if not overplot:
      plt.ylim(0, n.max()+0.1*n.max())
      
      
      ax = plt.gca()
      ax.set_axis_bgcolor("")
      myfigs.append(myfig)
    else:
      ymax.append(n.max()+0.1*n.max())

    
    if upperlimit != 0:
      ct = cumtrapz(n, bins)

      
      ct = np.insert(ct, 0, 0)

      
      ctu, ui = np.unique(ct, return_index=True)
      intf = interp1d(ctu, bins[ui], kind='linear')
      ulvals.append(intf(float(upperlimit)))

  
  if parval:
    if not overplot:
      plt.hold(True)
      plt.axvline(parval, color='k', ls='--', linewidth=1.5)
    else:
      plt.axvline(parval, color='k', ls='--', linewidth=1.5)

  if overplot:
    plt.ylim(0, max(ymax))
    
    ax = plt.gca()
    ax.set_axis_bgcolor("")
    plt.hold(False)
    myfigs.append(myfig)

  return myfigs, ulvals




def upper_limit(pos, upperlimit=0.95, parambounds=[float("-inf"), float("inf")], nbins=50):
  ulval = 0

  
  n, bins = hist_norm_bounds( pos, int(nbins), parambounds[0], parambounds[1] )

  
  if upperlimit != 0:
    ct = cumtrapz(n, bins)

    
    ct = np.insert(ct, 0, 0)

    
    ctu, ui = np.unique(ct, return_index=True)
    intf = interp1d(ctu, bins[ui], kind='linear')
    ulval = intf(float(upperlimit))

  return ulval


def upper_limit_greedy(pos, upperlimit=0.95, nbins=100):
  n, binedges = np.histogram(pos, bins=nbins)
  dbins = binedges[1]-binedges[0] 

  frac = 0.0
  j = 0
  for nv in n:
    prevfrac = frac
    frac += float(nv)/len(pos)
    j += 1
    if frac > upperlimit:
      break

  
  ul = binedges[j-1] + (upperlimit-prevfrac)*(dbins/(frac-prevfrac))

  return ul








def plot_posterior_chain(poslist, param, ifos, grr=None, withhist=0, mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt
  from lalapps.pulsarhtmlutils import paramlatexdict

  try:
    from matplotlib import gridspec
  except:
    return None

  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'sans-serif',
      'font.sans-serif': 'Avant Garde, Helvetica, Computer Modern Sans serif',
      'font.size': 15 }

  matplotlib.rcParams.update(mplparams)

  coldict = {'H1': 'r', 'H2': 'c', 'L1': 'g', 'V1': 'b', 'G1': 'm', 'Joint': 'k'}

  
  try:
    if param == 'iota':
      p = 'cosiota'
    else:
      p = param

    paryaxis = paramlatexdict[p.upper()]
  except:
    paryaxis = param

  if grr:
    legendvals = []

  maxiter = 0
  maxn = 0
  minsamp = float('inf')
  maxsamp = -float('inf')

  for idx, ifo in enumerate(ifos):
    if idx == 0:
      myfig = plt.figure(figsize=(12,4),dpi=200)
      myfig.subplots_adjust(bottom=0.15)

      if withhist:
        gs = gridspec.GridSpec(1,4, wspace=0)
        ax1 = plt.subplot(gs[:-1])
        ax2 = plt.subplot(gs[-1])

    pos = poslist[idx]

    
    if 'iota' == param:
      pos_samps = np.cos(pos['iota'].samples)
    else:
      pos_samps = pos[param].samples

    if np.min(pos_samps) < minsamp:
      minsamp = np.min(pos_samps)
    if np.max(pos_samps) > maxsamp:
      maxsamp = np.max(pos_samps)

    if withhist:
      ax1.hold(True)
      ax1.plot(pos_samps, '.', color=coldict[ifo], markersize=1)

      n, binedges = np.histogram( pos_samps, withhist, density=True )
      n = np.append(n, 0)
      ax2.hold(True)
      ax2.step(n, binedges, color=coldict[ifo])

      if np.max(n) > maxn:
        maxn = np.max(n)
    else:
      plt.plot(pos_samps, '.', color=coldict[ifo], markersize=1)
      plt.hold(True)

    if grr:
      try:
        legendvals.append(r'$R = %.2f$' % grr[idx][param])
      except:
        legendvals = []
    else:
      legendvals = None

    if len(pos_samps) > maxiter:
      maxiter = len(pos_samps)

  if not withhist:
    ax1 = plt.gca()

  bounds = [minsamp, maxsamp]

  ax1.set_ylabel(r''+paryaxis, fontsize=16, fontweight=100)
  ax1.set_xlabel(r'Iterations', fontsize=16, fontweight=100)

  ax1.set_xlim(0, maxiter)
  ax1.set_ylim(bounds[0], bounds[1])

  if withhist:
    ax2.set_ylim(bounds[0], bounds[1])
    ax2.set_xlim(0, maxn+0.1*maxn)
    ax2.set_yticklabels([])
    ax2.set_axis_bgcolor("")

  
  if legendvals:
    ax1.legend(legendvals, title='Gelman-Rubins test')

  return myfig














def read_hist_from_file(histfile):
  
  try:
    fp = open(histfile, 'rb')
  except:
    print("Could not open prior file %s" % histfile, file=sys.stderr)
    return None, None, None

  try:
    pd = fp.read() 
  except:
    print("Could not read in data from prior file %s" % histfile, file=sys.stderr)
    return None, None, None

  fp.close()

  
  
  header = struct.unpack("d"*6, pd[:6*8])
  
  "Could not read in header data from prior file %s" % histfile
  

  
  
  grid = struct.unpack("d"*int(header[2])*int(header[5]), pd[6*8:])
  
  "Could not read in header data from prior file %s" % histfile
  

  header = list(header)

  
  g = list(grid) 
  histarr = np.array([g[:int(header[5])]], ndmin=2)
  for i in range(int(header[2])-1):
    histarr = np.append(histarr, [g[(i+1)*int(header[5]):(i+2)*int(header[5])]], axis=0)

  xbins = np.linspace(header[0], header[0]+header[1]*(header[2]-1), int(header[2]))
  ybins = np.linspace(header[3], header[3]+header[4]*(header[5]-1), int(header[5]))

  return xbins, ybins, histarr






def plot_2Dhist_from_file(histfile, ndimlabel, mdimlabel, margpars=True, \
                          mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt
  from lalapps.pulsarhtmlutils import paramlatexdict

  
  xbins, ybins, histarr = read_hist_from_file(histfile)

  if not xbins.any():
    print("Could not read binary histogram file", file=sys.stderr)
    return None

  figs = []

  
  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'serif',
      'font.size': 12 }

  matplotlib.rcParams.update(mplparams)

  fig = plt.figure(figsize=(4,4),dpi=200)

  
  try:
    parxaxis = paramlatexdict[ndimlabel.upper()]
  except:
    parxaxis = ndimlabel

  try:
    paryaxis = paramlatexdict[mdimlabel.upper()]
  except:
    paryaxis = mdimlabel

  plt.xlabel(r''+parxaxis, fontsize=14, fontweight=100)
  plt.ylabel(r''+paryaxis, fontsize=14, fontweight=100, rotation=270)

  dx = xbins[1]-xbins[0]
  dy = ybins[1]-ybins[0]

  extent = [xbins[0]-dx/2., xbins[-1]+dx/2., ybins[-1]+dy/2., ybins[0]-dy/2.]

  plt.imshow(np.transpose(histarr), aspect='auto', extent=extent, \
             interpolation='bicubic', cmap='gray_r')

  fig.subplots_adjust(left=0.18, bottom=0.15) 
  fax = (fig.get_axes())[0].axis()

  figs.append(fig)

  if margpars:
    
    xmarg = []
    for i in range(len(xbins)):
      xmarg.append(np.trapz(histarr[:][i], x=ybins))

    
    xarea = np.trapz(xmarg, x=xbins)
    xmarg = map(lambda x: x/xarea, xmarg)

    ymarg = []
    for i in range(len(ybins)):
      ymarg.append(np.trapz(np.transpose(histarr)[:][i], x=xbins))

    
    yarea = np.trapz(ymarg, x=ybins)
    ymarg = map(lambda x: x/yarea, ymarg)

    
    figx = plt.figure(figsize=(4,4),dpi=200)
    plt.step(xbins, xmarg, color='k')
    plt.ylim(0, max(xmarg)+0.1*max(xmarg))
    plt.xlim(fax[0], fax[1])
    plt.xlabel(r''+parxaxis, fontsize=14, fontweight=100)
    plt.ylabel(r'Probability Density', fontsize=14, fontweight=100)
    figx.subplots_adjust(left=0.18, bottom=0.15) 
    ax = plt.gca()
    ax.set_axis_bgcolor("")

    
    figy = plt.figure(figsize=(4,4),dpi=200)
    plt.step(ybins, ymarg, color='k')
    plt.ylim(0, max(ymarg)+0.1*max(ymarg))
    plt.xlim(fax[3], fax[2])
    plt.xlabel(r''+paryaxis, fontsize=14, fontweight=100)
    plt.ylabel(r'Probability Density', fontsize=14, fontweight=100)
    figy.subplots_adjust(left=0.18, bottom=0.15) 
    ax = plt.gca()
    ax.set_axis_bgcolor("")

    figs.append(figx)
    figs.append(figy)

  return figs




def h0ul_from_prior_file(priorfile, ulval=0.95):
  
  h0bins, cibins, histarr = read_hist_from_file(priorfile)

  if not h0bins.any():
    print("Could not read binary histogram file", file=sys.stderr)
    return None

  
  h0marg = []
  for i in range(len(h0bins)):
    h0marg.append(np.trapz(histarr[:][i], x=cibins))

  
  h0bins = h0bins-(h0bins[1]-h0bins[0])/2
  h0area = np.trapz(h0marg, x=h0bins)
  h0margnorm = map(lambda x: x/h0area, h0marg)

  
  ct = cumtrapz(h0margnorm, h0bins)

  
  ct = np.insert(ct, 0, 0)

  
  ctu, ui = np.unique(ct, return_index=True)
  intf = interp1d(ctu, h0bins[ui], kind='linear')
  return intf(float(ulval))



def plot_posterior_hist2D(poslist, params, ifos, bounds=None, nbins=[50,50], \
                          parfile=None, overplot=False, mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt
  from lalapps.pulsarhtmlutils import paramlatexdict

  if len(params) != 2:
    print("Require 2 parameters", file=sys.stderr)
    sys.exit(1)

  
  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'serif',
      'font.size': 12 }

  matplotlib.rcParams.update(mplparams)

  if overplot:
    coldict = {'H1': 'Reds', 'H2': 'GnBu', 'L1': 'Greens', 'V1': 'Blues', 'G1': 'BuPu', \
               'Joint': 'Greys'}

  myfigs = []

  
  try:
    parxaxis = paramlatexdict[params[0].upper()]
  except:
    parxaxis = params[0]

  try:
    paryaxis = paramlatexdict[params[1].upper()]
  except:
    paryaxis = params[1]

  parval1 = None
  parval2 = None

  if parfile:
    parval1 = parfile[params[0].upper()]
    parval2 = parfile[params[1].upper()]

  if ifos == None:
    ifos = ['H1']

  for idx, ifo in enumerate(ifos):
    if overplot:
      if idx == 0:
        
        myfig = plt.figure(figsize=(4,4),dpi=200)

      if len(ifos) == 1:
        alpha=1.0
        cmap=plt.cm.get_cmap('Greys')
      else:
        alpha=0.5 
        cmap=plt.cm.get_cmap(coldict[ifo]) 
        
    else:
      myfig = plt.figure(figsize=(4,4),dpi=200)
      alpha=1.0 
      cmap=plt.cm.get_cmap('Greys')

    posterior = poslist[idx]

    a = np.squeeze(posterior[params[0]].samples)
    b = np.squeeze(posterior[params[1]].samples)

    
    par1pos_min = a.min()
    par2pos_min = b.min()

    par1pos_max = a.max()
    par2pos_max = b.max()

    plt.xlabel(r''+parxaxis, fontsize=14, fontweight=100)
    plt.ylabel(r''+paryaxis, fontsize=14, fontweight=100, rotation=270)

    H, xedges, yedges = np.histogram2d(a, b, nbins, normed=True)

    
    
    
    
    
    Hm = np.transpose(H)

    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]
    plt.imshow(Hm, aspect='auto', extent=extent, \
interpolation='bilinear', cmap=cmap, alpha=alpha)
    

    if bounds:
      plt.xlim(bounds[0][0], bounds[0][1])
      plt.ylim(bounds[1][0], bounds[1][1])

    
    if parval1 and parval2:
      if overplot and idx == len(ifos)-1:
        
        plt.hold(True)
        plt.plot(parval1, parval2, 'rx', markersize=8, mew=2)
      else:
        plt.hold(True)
        plt.plot(parval1, parval2, 'rx', markersize=8, mew=2)

    if overplot:
      plt.hold(True)
    if not overplot:
      myfig.subplots_adjust(left=0.18, bottom=0.15) 
      myfigs.append(myfig)

  if overplot:
    myfig.subplots_adjust(left=0.18, bottom=0.15) 
    myfigs.append(myfig)

  return myfigs





def hist_norm_bounds(samples, nbins, low=float("-inf"), high=float("inf")):
  
  n, binedges = np.histogram( samples, nbins )

  
  binwidth = binedges[1] - binedges[0]

  
  bincentres = np.array([])
  for i in range(0, len(binedges)-1):
    bincentres = np.append(bincentres, binedges[i]+binwidth/2)

  
  
  if bincentres[0] - binwidth > low:
    
    n = np.insert(n, 0, 0);

    
    bincentres = np.insert(bincentres, 0, bincentres[0] - binwidth)
  else:
    
    
    
    dx = bincentres[0] - low;

    
    bincentres = np.insert(bincentres, 0, low)

    dn = n[1]-n[0]

    nbound = n[0] - (dn/binwidth)*dx

    n = n.astype(float) 

    
    n = np.insert(n, 0, nbound)

  
  if bincentres[-1] + binwidth < high:
    
    n = np.append(n, 0)

    
    bincentres = np.append(bincentres, bincentres[-1] + binwidth)
  else:
    dx = high - bincentres[-1];

    
    bincentres = np.append(bincentres, high)

    dn = n[-1]-n[-2]

    nbound = n[-1] + (dn/binwidth)*dx

    n = n.astype(float) 

    
    n = np.append(n, nbound)

  
  area = np.trapz(n, x=bincentres)

  ns = np.array([])
  for i in range(0, len(bincentres)):
    ns = np.append(ns, float(n[i])/area)

  return ns, bincentres



def tukey_window(N, alpha=0.5):
  
  if alpha >= 1:
    return np.hanning(N)

  
  x = np.linspace(0, 1, N)

  
  win = np.ones(x.shape)

  
  lhs = x<alpha/2
  win[lhs] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[lhs] - alpha/2) ))

  
  rhs = x>=(1 - alpha/2)
  win[rhs] = 0.5 * (1 + np.cos(2*np.pi/alpha * (x[rhs] - 1 + alpha/2)))

  return win



"two-sided" amplitude spectral density


def plot_Bks_ASDs( Bkdata, delt=86400, plotpsds=True, plotfscan=False, removeoutlier=None, mplparams=False ):
  import matplotlib
  from matplotlib.mlab import specgram
  from matplotlib import colors
  from matplotlib import pyplot as plt

  
  Bkfigs = []
  psdfigs = []
  fscanfigs = []
  asdlist = []
  sampledt = []

  
  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'sans-serif',
      'font.sans-serif': 'Avant Garde, Helvetica, Computer Modern Sans serif',
      'font.size': 15 }

  matplotlib.rcParams.update(mplparams)
  matplotlib.rcParams['text.latex.preamble']=r'\usepackage{xfrac}'

  
  coldict = {'H1': 'r', 'H2': 'c', 'L1': 'g', 'V1': 'b', 'G1': 'm'}
  colmapdic = {'H1': 'Reds', 'H2': 'PuBu', 'L1': 'Greens', 'V1': 'Blues', 'G1': 'PuRd'}

  
  for ifo in Bkdata:
    
    try:
      Bk = np.loadtxt(Bkdata[ifo], comments=['
    except:
      print("Could not open file %s" % Bkdata[ifo], file=sys.stderr)
      sys.exit(-1)

    
    Bk = Bk[Bk[:,0].argsort()]

    
    uargs = np.unique(Bk[:,0], return_index=True)[1]
    Bk = Bk[uargs,:]

    
    gpstime = []

    
    
    if removeoutlier:
      n, binedges = np.histogram(np.log(np.fabs(np.concatenate((Bk[:,1], Bk[:,2])))), 50)
      j = n.argmax(0)

      
      stdest = math.exp((binedges[j]+binedges[j+1])/2)

      
      
      vals = np.where(np.fabs(Bk[:,1]) < removeoutlier*stdest)
      Bknew = Bk[vals,:][-1]
      
      vals = np.where(np.fabs(Bknew[:,2]) < removeoutlier*stdest)
      Bk = Bknew[vals,:][-1]

    gpstime = Bk[:,0]

    
    mindt = min(np.diff(gpstime))
    sampledt.append(mindt)

    Bkabs = np.sqrt(Bk[:,1]**2 + Bk[:,2]**2)

    
    Bkfig = plt.figure(figsize=(11,3.5), dpi=200)
    Bkfig.subplots_adjust(bottom=0.15, left=0.09, right=0.94)

    tms = map(lambda x: x-gpstime[0], gpstime)

    plt.plot(tms, Bkabs, '.', color=coldict[ifo], markersize=1)
    plt.xlabel(r'GPS - %d' % int(gpstime[0]), fontsize=14, fontweight=100)
    plt.ylabel(r'$|B_k|$', fontsize=14, fontweight=100)
    
    plt.xlim(tms[0], tms[-1])

    Bkfigs.append(Bkfig)

    if plotpsds or plotfscan:
      
      
      totlen = gpstime[-1] - gpstime[0] 

      
      if math.fmod(mindt, 1) != 0. or mindt < 1:
        print("Error... time steps between data points must be integers", file=sys.stderr)
        sys.exit(-1)

      count = 0

      
      datazeropad = np.zeros(int(math.ceil(totlen/mindt))+1, dtype=complex)

      idx = map(lambda x: int(math.floor((x/mindt)+0.5)), tms)
      for i in range(0, len(idx)):
        datazeropad[idx[i]] = complex(Bk[i,1], Bk[i,2])

      win = tukey_window(math.floor(delt/mindt), alpha=0.1)

      Fs = 1./mindt 

      fscan, freqs, t = specgram(datazeropad, NFFT=int(math.floor(delt/mindt)), Fs=Fs, window=win, noverlap=int(math.floor(delt/(2.*mindt))))

      if plotpsds:
        fshape = fscan.shape

        totalasd = np.zeros(fshape[0])

        for i in range(0, fshape[0]):
          scanasd = np.sqrt(fscan[i,:])
          nonzasd = np.nonzero(scanasd)
          scanasd = scanasd[nonzasd]

          
          
          totalasd[i] = np.median(scanasd)

        
        asdlist.append(totalasd)

        
        psdfig = plt.figure(figsize=(4,3.5), dpi=200)
        psdfig.subplots_adjust(left=0.18, bottom=0.15)

        plt.plot(freqs, totalasd, color=coldict[ifo])
        plt.xlim(freqs[0], freqs[-1])
        plt.xlabel(r'Frequency (Hz)', fontsize=14, fontweight=100)
        plt.ylabel(r'$h/\sqrt{\rm Hz}$', fontsize=14, fontweight=100)

        
        ax = plt.gca()
        xt = [-Fs/2., -Fs/4., 0., Fs/2., Fs/4.]
        ax.set_xticks(xt)
        xl = []
        for item in xt:
          if item == 0:
            xl.append('0')
          else:
            if item < 0:
              xl.append(r'$-\sfrac{1}{%d}$' % (-1./item))
            else:
              xl.append(r'$\sfrac{1}{%d}$' % (1./item))
        ax.set_xticklabels(xl)
        
        plt.tick_params(axis='x', which='major', labelsize=14)

        psdfigs.append(psdfig)

      if plotfscan:
        fscanfig = plt.figure(figsize=(11,3.5), dpi=200)
        fscanfig.subplots_adjust(bottom=0.15, left=0.09, right=0.94)

        extent = [tms[0], tms[-1], freqs[0], freqs[-1]]
        plt.imshow(np.sqrt(np.flipud(fscan)), aspect='auto', extent=extent,
          interpolation=None, cmap=colmapdic[ifo], norm=colors.Normalize())
        plt.ylabel(r'Frequency (Hz)', fontsize=14, fontweight=100)
        plt.xlabel(r'GPS - %d' % int(gpstime[0]), fontsize=14, fontweight=100)

        
        ax = plt.gca()
        yt = [-Fs/2., -Fs/4., 0., Fs/2., Fs/4.]
        ax.set_yticks(yt)
        yl = []
        for item in yt:
          if item == 0:
            yl.append('0')
          else:
            if item < 0:
              yl.append(r'$-\sfrac{1}{%d}$' % (-1./item))
            else:
              yl.append(r'$\sfrac{1}{%d}$' % (1./item))
        ax.set_yticklabels(yl)
        plt.tick_params(axis='y', which='major', labelsize=14)

        fscanfigs.append(fscanfig)

  return Bkfigs, psdfigs, fscanfigs, asdlist, sampledt





def plot_limits_hist(lims, param, ifos, prevlims=None, bins=20, overplot=False, mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt
  from lalapps.pulsarhtmlutils import paramlatexdict

  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'serif',
      'font.size': 12 }

  matplotlib.rcParams.update(mplparams)

  myfigs = []

  
  coldict = {'H1': 'r', 'H2': 'c', 'L1': 'g', 'V1': 'b', 'G1': 'm', 'Joint':'k'}

  try:
    parxaxis = paramlatexdict[param.upper()]
  except:
    parxaxis = param

  paryaxis = 'Number of Pulsars'

  
  logprevlims = None
  if prevlims is not None:
    logprevlims = np.log10(prevlims)

  
  hrange = None
  stacked = False
  if overplot:
    highbins = []
    lowbins = []

    
    stackdata = []
    stacked = True

    for j, ifo in enumerate(ifos):
      theselims = lims[ifo]

      
      for i, val in enumerate(theselims):
        if val == None:
          del theselims[i]

      loglims = np.log10(theselims)

      stackdata.append(loglims)

      highbins.append(np.max(loglims))
      lowbins.append(np.min(loglims))

    if logprevlims is not None:
      highbins.append(max(logprevlims))
      lowbins.append(min(logprevlims))

    hrange = (min(lowbins), max(highbins))

  for j, ifo in enumerate(ifos):
    
    theselims = lims[ifo]

    
    for i, val in enumerate(theselims):
      if val == None:
        del theselims[i]

    loglims = np.log10(theselims)

    if not overplot:
      stackdata = loglims

    
    myfig = plt.figure(figsize=(4,4),dpi=200)
    maxlims = []
    minlims = []

    if overplot:
      edgecolor = []
      facecolor = []
      for ifoname in ifos:
        edgecolor.append(coldict[ifoname])
        facecolor.append(coldict[ifoname])
    else:
      edgecolor = [coldict[ifo]]
      facecolor = [coldict[ifo]]

    
    n, bins, patches = plt.hist(stackdata, bins, range=hrange, histtype='step', stacked=stacked, fill=True, color=edgecolor, alpha=0.6)
    for i, patch in enumerate(patches):
      plt.setp(patch, 'facecolor', facecolor[i])

    if not overplot:
      maxlims.append(np.max(loglims))
      minlims.append(np.min(loglims))

    if logprevlims is not None:
      if not overplot:
        maxlims.append(max(logprevlims))
        minlims.append(min(logprevlims))

        maxlim = max(maxlims)
        minlim = min(minlims)
      else:
        maxlim = hrange[1]
        minlim = hrange[0]

      plt.hold(True)
      plt.hist(logprevlims, bins, range=hrange, edgecolor='k', lw=2, histtype='step', fill=False)
      plt.hold(False)
    else:
      if not overplot:
        maxlim = max(maxlims)
        minlim = min(minlims)
      else:
        maxlim = hrange[1]
        minlim = hrange[0]

    
    ax = plt.gca()

    
    tickvals = range(int(math.ceil(maxlim) - math.floor(minlim)))
    tickvals = map(lambda x: x + int(math.floor(minlim)), tickvals)
    ax.set_xticks(tickvals)
    tls = map(lambda x: '$10^{%d}$' % x, tickvals)
    ax.set_xticklabels(tls)

    plt.ylabel(r''+paryaxis, fontsize=14, fontweight=100)
    plt.xlabel(r''+parxaxis, fontsize=14, fontweight=100)

    myfig.subplots_adjust(left=0.18, bottom=0.15) 

    myfigs.append(myfig)

    if overplot:
      break

  return myfigs












def plot_h0_lims(h0lims, f0gw, ifos, xlims=[10, 1500], ulesttop=None,
                 ulestbot=None, prevlim=None, prevlimf0gw=None, overplot=False, mplparams=False):
  import matplotlib
  from matplotlib import pyplot as plt

  if not mplparams:
    mplparams = { \
      'backend': 'Agg',
      'text.usetex': True, 
      'axes.linewidth': 0.5, 
      'axes.grid': True, 
      'grid.linewidth': 0.5,
      'font.family': 'serif',
      'font.size': 12 }

  matplotlib.rcParams.update(mplparams)

  myfigs = []

  
  coldict = {'H1': 'r', 'H2': 'c', 'L1': 'g', 'V1': 'b', 'G1': 'm', 'Joint':'k'}

  parxaxis = 'Frequency (Hz)'
  paryaxis = '$h_0$'

  for j, ifo in enumerate(ifos):
    h0lim = h0lims[ifo]

    if len(ifos) > 1:
      f0s = f0gw[ifo]
    else:
      f0s = f0gw

    if len(h0lim) != len(f0s):
      return None 

    if not overplot or (overplot and j == 0):
      myfig = plt.figure(figsize=(7,5.5),dpi=200)

    plt.hold(True)
    if ulesttop is not None and ulestbot is not None:
      ult = ulesttop[ifo]
      ulb = ulestbot[ifo]

      if len(ult) == len(ulb) and len(ult) == len(f0s):
        for i in range(len(ult)):
          plt.loglog([f0s[i], f0s[i]], [ulb[i], ult[i]], ls='-', lw=3, c='lightgrey')

    if prevlim is not None and prevlimf0gw is not None and len(prevlim) == len(prevlimf0gw):
      if not overplot or (overplot and j == len(ifos)-1):
        plt.loglog(prevlimf0gw, prevlim, marker='*', ms=10, alpha=0.7, mfc='None', mec='k', ls='None')

    
    plt.loglog(f0s, h0lim, marker='*', ms=10, mfc=coldict[ifo], mec=coldict[ifo], ls='None')

    plt.ylabel(r''+paryaxis, fontsize=14, fontweight=100)
    plt.xlabel(r''+parxaxis, fontsize=14, fontweight=100)

    plt.xlim(xlims[0], xlims[1])

    if not overplot or (overplot and j == len(ifos)-1):
      plt.hold(False)
      myfig.subplots_adjust(left=0.12, bottom=0.10) 
      myfigs.append(myfig)

  return myfigs








def heterodyned_triaxial_pulsar(starttime, duration, dt, detector, pardict):

  
  ts = []
  tmpts = starttime

  
  s = np.array([], dtype=complex)

  sphi = np.sin(pardict['phi0'])
  cphi = np.cos(pardict['phi0'])

  Xplus = 0.25*(1.+pardict['cosiota']*pardict['cosiota'])*pardict['h0']
  Xcross = 0.5*pardict['cosiota']*pardict['h0']
  Xpsinphi = Xplus*sphi
  Xcsinphi = Xcross*sphi
  Xpcosphi = Xplus*cphi
  Xccosphi = Xcross*cphi

  i = 0
  while tmpts < starttime + duration:
    ts.append(starttime+(dt*i))

    
    fp, fc = antenna_response(ts[i], pardict['ra'], pardict['dec'], pardict['psi'], detector)

    
    s = np.append(s, (fp*Xpcosphi + fc*Xcsinphi) + 1j*(fp*Xpsinphi - fc*Xccosphi) )

    tmpts = ts[i]+dt

    i = i+1;

  return ts, s













def heterodyned_pulsar_signal(pardict, detector, starttime=900000000., duration=86400., dt=60., datatimes=None):
  if 'cosiota' in pardict:
    cosiota = pardict['cosiota']
    iota = math.acos(cosiota)
    siniota = math.sin(iota)
  else:
    print("cos(iota) not defined!", file=sys.stderr)
    raise KeyError

  if 'psi' in pardict:
    psi = pardict['psi']
  else:
    print("psi not defined!", file=sys.stderr)
    raise KeyError

  if 'C22' in pardict:
    C22 = pardict['C22']
  else:
    if 'h0' in pardict:
      C22 = -pardict['h0']/2.
    else:
      C22 = 0.

  if 'phi22' in pardict:
    phi22 = pardict['phi22']
  else:
    if 'phi0' in pardict:
      phi22 = 2.*pardict['phi0']
    else:
      phi22 = 0.

  ePhi22 = cmath.exp(phi22*1j)

  if 'C21' in pardict:
    C21 = pardict['C21']
  else:
    C21 = 0.

  if 'phi21' in pardict:
    phi21 = pardict['phi21']
  else:
    phi21 = 0.

  ePhi21 = cmath.exp(phi21*1j)

  s = [] 
  ts = [] 

  if 'C21' in pardict and 'C22' in pardict and 'h0' not in pardict:
    freqs = [1., 2.]
  else:
    freqs = [2.]

  for f in freqs:
    i = 0
    if datatimes is None:
      datatimes = np.arange(starttime, starttime+duration, dt)

    
    fp, fc = antenna_response(datatimes, pardict['ra'], pardict['dec'], pardict['psi'], detector)

    if f == 1.:
      sf = -(C21/4.)*ePhi21*siniota*cosiota*fp + 1j*(C21/4.)*ePhi21*siniota*fc
    elif f == 2.:
      sf = -(C22/2.)*ePhi22*(1.+cosiota**2.)*fp + 1j*(C22)*ePhi22*cosiota*fc

    ts.append(datatimes)
    s.append(sf)

  return ts, s




def convert_model_parameters(pardict):
  costheta = pardict['costheta']
  theta = np.arccos(costheta)
  sintheta = math.sin(theta)
  sin2theta = math.sin( 2.0*theta )
  sinlambda = math.sin(pardict['lambda'])
  coslambda = math.cos(pardict['lambda'])
  sin2lambda = math.sin( 2.0*pardict['lambda'] )

  phi0 = pardict['phi0']

  I21 = pardict['I21']
  I31 = pardict['I31']

  A22 = ( I21 * ( sinlambda**2 - ( coslambda * costheta )**2 ) - I31 * sintheta**2 )
  B22 = I21 * sin2lambda * costheta

  C22 = 2.*math.sqrt( A22**2 + B22**2 )

  A21 = I21 * sin2lambda * sintheta
  B21 = ( I21 * coslambda**2 - I31 ) * sin2theta

  C21 = 2.*math.sqrt( A21**2 + B21**2 )

  phi22 = np.fmod(2.*phi0 - math.atan2( B22, A22 ), 2.*np.pi)
  phi21 = np.fmod(phi0 - math.atan2( B21, A21 ), 2.*np.pi)

  outvals = {'C22': C22, 'C21': C21, 'phi22': phi22, 'phi21': phi21}

  return outvals









def heterodyned_pinsf_pulsar(starttime, duration, dt, detector, pardict):
  iota = np.arccos(pardict['cosiota'])
  theta = np.arccos(pardict['costheta'])
  siniota = math.sin(iota)
  sintheta = math.sin(theta)
  sin2theta = math.sin( 2.0*theta )
  sinlambda = math.sin(pardict['lambda'])
  coslambda = math.cos(pardict['lambda'])
  sin2lambda = math.sin( 2.0*pardict['lambda'] )

  ePhi = cmath.exp( 0.5 * pardict['phi0'] * 1j )
  e2Phi = cmath.exp( pardict['phi0'] * 1j )

  f2_r = pardict['f0']**2 / pardict['dist']

  """
    This model is a complex heterodyned time series for a pinned superfluid
    neutron star emitting at its roation frequency and twice its rotation
    frequency (as defined in Eqns 35-38 of Jones 2012 LIGO DCC T1200265-v3)
  """

  Xplusf = -( f2_r / 2.0 ) * siniota * pardict['cosiota']
  Xcrossf = ( f2_r / 2.0 ) * siniota

  Xplus2f = -f2_r * ( 1.0 + pardict['cosiota']**2 )
  Xcross2f = 2. * f2_r * pardict['cosiota']

  A21 = pardict['I21'] * sin2lambda * sintheta
  B21 = ( pardict['I21'] * coslambda**2 - pardict['I31'] ) * sin2theta

  A22 = pardict['I21'] * ( sinlambda**2 - coslambda**2 * pardict['costheta']**2 ) - \
    pardict['I31'] * sintheta**2
  B22 = pardict['I21'] * sin2lambda * pardict['costheta']

  
  ts1 = []
  ts2 = []
  tmpts = starttime

  
  s1 = np.array([], dtype=complex)
  s2 = np.array([], dtype=complex)

  i = 0
  while tmpts < starttime + duration:
    ts1.append(starttime+(dt*i))
    ts2.append(starttime+(dt*i))

    
    fp, fc = antenna_response(ts1[i], pardict['ra'], pardict['dec'], pardict['psi'], detector)

    
    s1 = np.append(s1, ( fp * Xplusf * ePhi * ( A21 - 1j * B21 ) ) + \
                       ( fc * Xcrossf * ePhi * ( B21 + 1j * A21 ) ) )

    
    s2 = np.append(s2, ( fp * Xplus2f * e2Phi * ( A22 - 1j * B22 ) ) + \
                       ( fc * Xcross2f * e2Phi * ( B22 + 1j * A22 ) ) )

    tmpts = ts1[i]+dt

    i = i+1;

  
  ts = np.vstack([ts1, ts2])
  s = np.vstack([s1, s2])

  return ts, s





def antenna_response( gpsTime, ra, dec, psi, det ):
  import lal

  
  detMap = {'H1': lal.LALDetectorIndexLHODIFF, \
            'H2': lal.LALDetectorIndexLHODIFF, \
            'L1': lal.LALDetectorIndexLLODIFF, \
            'G1': lal.LALDetectorIndexGEO600DIFF, \
            'V1': lal.LALDetectorIndexVIRGODIFF, \
            'T1': lal.LALDetectorIndexTAMA300DIFF, \
            'AL1': lal.LALDetectorIndexLLODIFF, \
            'AH1': lal.LALDetectorIndexLHODIFF, \
            'AV1': lal.LALDetectorIndexVIRGODIFF, \
            'E1': lal.LALDetectorIndexE1DIFF, \
            'E2': lal.LALDetectorIndexE2DIFF, \
            'E3': lal.LALDetectorIndexE3DIFF}

  try:
    detector=detMap[det]
  except KeyError:
    raise ValueError, "ERROR. Key %s is not a valid detector name." % (det)

  
  detval = lal.CachedDetectors[detector]
  response = detval.response

  
  if not isinstance(ra, float):
    if isinstance(ra, basestring):
      try:
        ra = ra_to_rad(ra)
      except:
        raise ValueError, "Right ascension string '%s' not formatted properly" % ra
    else:
      raise ValueError, "Right ascension must be a 'float' in radians or a string of the format 'hh:mm:ss.s'"

  if not isinstance(dec, float):
    if isinstance(dec, basestring):
      try:
        dec = dec_to_rad(dec)
      except:
        raise ValueError, "Declination string '%s' not formatted properly" % ra
    else:
      raise ValueError, "Declination must be a 'float' in radians or a string of the format 'dd:mm:ss.s'"

  
  if isinstance(gpsTime, float) or isinstance(gpsTime, int):
    gpsTime = np.array([gpsTime])
  else: 
    gpsTime = np.copy(gpsTime)

  
  if len(gpsTime) == 1 or np.unique(np.diff(gpsTime)).size == 1:
    gpsStart = lal.LIGOTimeGPS( gpsTime[0] )
    dt = 0.
    if len(gpsTime) > 1:
      dt = gpsTime[1]-gpsTime[0]
    fp, fc = lal.ComputeDetAMResponseSeries(response, ra, dec, psi, gpsStart, dt, len(gpsTime))

    
    return fp.data.data, fc.data.data
  else: 
    fp = np.zeros(len(gpsTime))
    fc = np.zeros(len(gpsTime))

    for i in range(len(gpsTime)):
      gps = lal.LIGOTimeGPS( gpsTime[i] )
      gmst_rad = lal.GreenwichMeanSiderealTime(gps)

      
      fp[i], fc[i] = lal.ComputeDetAMResponse(response, ra, dec, psi, gmst_rad)

    return fp, fc






def inject_pulsar_signal(starttime, duration, dt, detectors, pardict, \
                         freqfac=[2.0], npsds=None, snrscale=None):
  
  if isinstance(detectors, basestring):
    detectors = [detectors]

  
  
  if npsds is None:
    npsds = []

    for det in detectors:
      for frf in freqfac:
        psd = detector_noise( det, frf*pardict['f0'] )

        
        
        ns = np.sqrt( (psd/2.0)/(2.0*dt) )

        npsds.append(ns)
  else:
    
    tmpnpsds = []

    count = 0
    for j, det in enumerate(detectors):
      for frf in freqfac:
        if len(npsds) == 1:
          tmpnpsds.append( np.sqrt( (npsds[0]/2.0)/(2.0*dt) ) )
        else:
          tmpnpsds.append( np.sqrt( (npsds[count]/2.0)/(2.0*dt) ) )

        count = count+1

    npsds = tmpnpsds

  if len(freqfac) == 1 and len(detectors) != len(npsds):
    raise ValueError, "Number of detectors %d not the same as number of "\
                      "noises %d" % (len(detectors), len(npsds))

  if len(freqfac) == 2 and 2*len(detectors) != len(npsds):
    raise ValueError, "Number of detectors %d not half the number of "\
                      "noises %d" % (len(detectors), len(npsds))

  tss = np.array([])
  ss = np.array([])

  snrtot = 0
  for j, det in enumerate(detectors):
    
    if len(freqfac) == 1 and freqfac[0] == 2.0:
      ts, s = heterodyned_pulsar_signal(starttime, duration, dt, det, pardict)

      if j == 0:
        tss = np.append(tss, ts)
        ss = np.append(ss, s)
      else:
        tss = np.vstack([tss, ts])
        ss = np.vstack([ss, s])

      
      snrtmp = get_optimal_snr( s[0], npsds[j] )
    elif len(freqfac) == 2:
      ts, s = heterodyned_pulsar_signal(starttime, duration, dt, det, pardict)

      snrtmp = 0
      for k, frf in enumerate(freqfac):
        if j == 0 and k == 0:
          tss = np.append(tss, ts[k][:])
          ss = np.append(ss, s[k][:])
        else:
          tss = np.vstack([tss, ts[k][:]])
          ss = np.vstack([ss, s[k][:]])

        snrtmp2 = get_optimal_snr( s[k][:], npsds[2*j+k] )
        snrtmp = snrtmp + snrtmp2*snrtmp2

      snrtmp = np.sqrt(snrtmp)

    snrtot = snrtot + snrtmp*snrtmp

  
  snrtot = np.sqrt(snrtot)

  
  if snrscale is not None:
    if snrscale != 0:
      snrscale = snrscale / snrtot
    
  else:
    snrscale = 1

  i = 0
  for det in detectors:
    
    if len(freqfac) == 1:
      
      rs = np.random.randn(len(ts[0]), 2)

      for j, t in enumerate(ts[0]):
        if len(tss.shape) == 1:
          ss[j] = (snrscale*ss[j].real + npsds[i]*rs[j][0]) + 1j*(snrscale*ss[j].imag + npsds[i]*rs[j][1])
        else:
          ss[i][j] = (snrscale*ss[i][j].real + npsds[i]*rs[j][0]) + 1j*(snrscale*ss[i][j].imag + npsds[i]*rs[j][1])

      i = i+1
    elif len(freqfac) == 2:
      
      rs = np.random.randn(len(ts[0][:]), 4)

      for j, t in enumerate(ts[0][:]):
        ss[i][j] = (snrscale*ss[i][j].real + npsds[i]*rs[j][0]) + 1j*(snrscale*ss[i][j].imag + npsds[i]*rs[j][1])
        ss[i+1][j] = (snrscale*ss[i+1][j].real + npsds[i+1]*rs[j][2]) + \
          1j*(snrscale*ss[i+1][j].imag + npsds[i+1]*rs[j][3])

      i = i+2
    else:
      print("Something wrong with injection", file=sys.stderr)
      sys.exit(1)

  snrtot = snrtot*snrscale

  return tss, ss, snrtot, snrscale







def detector_noise( det, f ):
  import lalsimulation

  if det == 'AV1': 
    return lalsimulation.SimNoisePSDAdvVirgo( f )
  elif det == 'H1' or det == 'L1': 
    return lalsimulation.SimNoisePSDiLIGOSRD( f )
  elif det == 'H2':
    return lalsimulation.SimNoisePSDiLIGOSRD( f )*2.
  elif det == 'G1': 
    return lalsimulation.SimNoisePSDGEO( f )
  elif det == 'V1': 
    return lalsimulation.SimNoisePSDVirgo( f )
  elif det == 'T1': 
    return lalsimulation.SimNoisePSDTAMA( f )
  elif det == 'K1': 
    return lalsimulation.SimNoisePSDKAGRA( f )
  elif det == 'AL1' or det == 'AH1':
    return lalsimulation.SimNoisePSDaLIGOZeroDetHighPower( f )
  else:
    raise ValueError, "%s is not a recognised detector" % (det)



def get_optimal_snr( s, sig ):
  ss = 0
  
  for val in s:
    ss = ss + val.real**2 + val.imag**2

  return np.sqrt( ss / sig**2 )





def gelman_rubins(chains):
  chainMeans = [np.mean(data) for data in chains]
  chainVars = [np.var(data) for data in chains]

  BoverN = np.var(chainMeans)
  W = np.mean(chainVars)

  sigmaHat2 = W + BoverN

  m = len(chains)

  VHat=sigmaHat2 + BoverN/m

  R = VHat/W

  return R








def pulsar_mcmc_to_posterior(chainfiles):
  from pylal import bayespputils as bppu

  cl = []
  neffs = []
  grr = {}

  mcmc = []

  for cfile in chainfiles:
    if os.path.isfile(cfile):
      
      mcmcChain = read_pulsar_mcmc_file(cfile)

      
      if mcmcChain is None:
        return None, None, None, None

      
      neffstmp = []
      for j in range(1, mcmcChain.shape[1]):
        neff, acl, acf = bppu.effectiveSampleSize(mcmcChain[:,j])
        neffstmp.append(neff)

      
      
      
      neffs.append(math.floor(np.mean(neffstmp)))

      
      nskip = int(math.ceil(mcmcChain.shape[0]/np.mean(neffstmp)))

      
      mcmc.append(mcmcChain[::nskip,:])
      cl.append(mcmcChain.shape[0])
    else:
      print("File %s does not exist!" % cfile, file=sys.stderr)
      return None, None, None, None

  
  
  cf = open(chainfiles[0], 'r')
  headers = cf.readline()
  headers = cf.readline() 
  
  headers = re.sub('%', '', headers)
  
  headers = re.sub('rads', '', headers)
  
  headers = re.sub('[()]', '', headers)
  cf.close()

  
  for idx, parv in enumerate(headers.split()):
    lgr = []
    if parv != 'logL':
      for j in range(0, len(mcmc)):
        achain = mcmc[j]
        singlechain = achain[:,idx]
        lgr.append(singlechain)
      grr[parv.lower()] = gelman_rubins(lgr)

  
  
  headers = headers.replace('\n', '\tpost\n')

  
  comfile = chainfiles[0] + '_common_tmp.dat'
  try:
    cf = open(comfile, 'w')
  except:
    print("Can't open common posterior file!", file=sys.stderr)
    sys.exit(0)

  cf.write(headers)
  for narr in mcmc:
    for j in range(0, narr.shape[0]):
      mline = narr[j,:]
      
      mline = np.append(mline, np.exp(mline[0]))

      strmline = " ".join(str(x) for x in mline) + '\n'
      cf.write(strmline)
  cf.close()

  
  peparser = bppu.PEOutputParser('common')
  cf = open(comfile, 'r')
  commonResultsObj = peparser.parse(cf)
  cf.close()

  
  os.remove(comfile)

  
  pos = bppu.Posterior( commonResultsObj, SimInspiralTableEntry=None, \
                        votfile=None )

  
  
  cipos = None
  cipos = bppu.PosteriorOneDPDF('cosiota', np.cos(pos['iota'].samples))

  
  pos.append(cipos)

  
  pos.pop('iota')

  return pos, neffs, grr, cl






def read_pulsar_mcmc_file(cf):
  cfdata = None

  
  try:
    cfdata = np.loadtxt(cf, comments='%')
  except:
    try:
      fc = open(cf, 'r')

      
      headers = fc.readline()
      headers = fc.readline() 
      fc.close()
      
      headers = re.sub('%', '', headers)
      
      headers = re.sub('rads', '', headers)
      
      headers = re.sub('[()]', '', headers)

      lh = len(headers.split())

      cfdata = np.array([])

      lines = cf.readlines()

      for i, line in enumerate(lines):
        if '%' in line: 
          continue

        lvals = line.split()

        
        if len(lvals) != lh:
          continue

        
        try:
          lvalsf = map(float, lvals)
        except:
          continue

        
        if i==0:
          cfdata = np.array(lvalsf)
        else:
          cfdata = np.vstack((cfdata, lvalsf))

      if cfdata.size == 0:
        cfdata = None
    except:
      cfdata = None

  return cfdata


def pulsar_nest_to_posterior(postfile, nestedsamples=False, removeuntrig=True):
  """
  This function will import a posterior sample file created by `lalapps_nest2pos` (or a nested
  sample file). It will be returned as a Posterior class object from `bayespputils`. The
  signal evidence and noise evidence are also returned.

  Parameters
  ----------
  postfile : str, required
      The file name of the posterior or nested sample file. In general this should be a HDF5 file with the extension
      '.hdf' or '.h5', although older format ascii files are still supported at the moment.
  nestedsamples : bool, default: False
      If the file being input contains nested samples, rather than posterior samples, then this flag must be set to
      True
  removeuntrig : bool, default: True
      If this is True then any parameters that are sines or cosines of a value will have the value removed if present
      e.g. if cosiota and iota exist then iota will be removed.
  """

  from pylal import bayespputils as bppu
  from pylal.bayespputils import replace_column

  fe = os.path.splitext(postfile)[-1].lower() 

  
  if fe == '.h5' or fe == '.hdf': 
    if nestedsamples:
      
      try:
        from lalinference.io import read_samples
        import lalinference

        samples = read_samples(postfile, tablename=lalinference.LALInferenceHDF5NestedSamplesDatasetName)
        params = samples.colnames

        
        for param in params:
          replace_column(samples, param, samples[param].astype(float))

        nsResultsObject = (samples.colnames, samples.as_array().view(float).reshape(-1, len(params)))
      except:
        raise IOError, "Could not import nested samples"
    else: 
      peparser = bppu.PEOutputParser('hdf5')
      nsResultsObject = peparser.parse(postfile)
  elif fe == '.gz': 
    import gzip
    peparser = bppu.PEOutputParser('common')
    nsResultsObject = peparser.parse(gzip.open(postfile, 'r'))
  else: 
    peparser = bppu.PEOutputParser('common')
    nsResultsObject = peparser.parse(open(postfile, 'r'))

  pos = bppu.Posterior( nsResultsObject, SimInspiralTableEntry=None, votfile=None )

  
  pnames = pos.names
  nsamps = len(pos[pnames[0]].samples)
  permarr = np.arange(nsamps)
  np.random.shuffle(permarr)
  for pname in pnames:
    
    if pos[pname].samples.tolist().count(pos[pname].samples[0]) == len(pos[pname].samples):
      pos.pop(pname)
    else:
      
      shufpos = None
      shufpos = bppu.PosteriorOneDPDF(pname, pos[pname].samples[permarr])
      pos.pop(pname)
      pos.append(shufpos)

  
  try:
    posIota = pos['iota'].samples
  except:
    posIota = None

  if posIota is not None:
    cipos = None
    cipos = bppu.PosteriorOneDPDF('cosiota', np.cos(posIota))
    pos.append(cipos)
    if removeuntrig:
      pos.pop('iota')

  
  try:
    posI = pos['i'].samples
  except:
    posI = None

  if posI is not None:
    sinipos = None
    sinipos = bppu.PosteriorOneDPDF('sini', np.sin(posI))
    pos.append(sinipos)
    if removeuntrig:
      pos.pop('i')

  
  try:
    posC21 = pos['c21'].samples
  except:
    posC21 = None

  try:
    posC22 = pos['c22'].samples
  except:
    posC22 = None

  try:
    posphi22 = pos['phi22'].samples
  except:
    posphi22 = None

  
  if posC22 is not None and posC21 is None:
    h0pos = None
    h0pos = bppu.PosteriorOneDPDF('h0', 2.*pos['c22'].samples)

    pos.append(h0pos)
    pos.pop('c22')

    if posphi22 is not None:
      phi0pos = None
      phi0pos = bppu.PosteriorOneDPDF('phi0', np.fmod(pos['phi22'].samples + math.pi, 2.*math.pi))

      pos.append(phi0pos)
      pos.pop('phi22')

  
  if fe == '.h5' or fe == '.hdf':
    
    hdf = h5py.File(postfile, 'r')
    a = hdf['lalinference']['lalinference_nest']
    sigev = a.attrs['log_evidence']
    noiseev = a.attrs['log_noise_evidence']
    hdf.close()
  else:
    B = np.loadtxt(postfile.replace('.gz', '')+'_B.txt')
    sigev = B[1]
    noiseev = B[2]

  
  return pos, sigev, noiseev



def logplus(x, y):
  return np.logaddexp(x, y)


def logtrapz(lnf, dx):
  """
  Perform trapezium rule integration for the logarithm of a function on a regular grid.

  Inputs
  ------
  lnf - a numpy array of values that are the natural logarithm of a function
  dx  - a float giving the step size between values in the function

  Returns
  -------
  The natural logarithm of the area under the function.
  """

  return np.log(dx/2.) + logsumexp([logsumexp(lnf[:-1]), logsumexp(lnf[1:])])



def marginalise(like, pname, pnames, ranges):
  
  
  
  

  places = ranges[pname]
  axis = pnames.index(pname)

  
  if len(places) > 1:
    x = np.apply_along_axis(logtrapz, axis, like, places[1]-places[0])
  elif len(places) == 1:
    
    z = like.shape
    q = np.arange(0,len(z)).astype(int) != axis
    newshape = tuple((np.array(list(z)))[q])
    x = np.reshape(like, newshape)

  
  del ranges[pname]
  pnames.remove(pname)

  return x



def marginal(lnlike, pname, pnames, ranges, multflatprior=False):
  from copy import deepcopy

  
  lnliketmp = deepcopy(lnlike)
  pnamestmp = deepcopy(pnames)
  rangestmp = deepcopy(ranges)

  for name in pnames:
    if name != pname:
      if multflatprior: 
        lnliketmp = marginalise(lnliketmp + np.log(1./(rangestmp[name][-1]-rangestmp[name][0])), name, pnamestmp, rangestmp)
      else:
        lnliketmp = marginalise(lnliketmp, name, pnamestmp, rangestmp)

  return lnliketmp



def get_chunk_lengths( ts, chunkMax ):
  i = j = count = 0

  length = len(ts)

  chunkLengths = []

  dt = np.min(np.diff(ts)) 

  
  while True:
    count += 1 

    
    if i > length - 2:
      
      chunkLengths.append(count)
      break

    i += 1

    t1 = ts[i-1]
    t2 = ts[i]

    
    if t2 - t1 > 2.*dt or count == chunkMax:
      chunkLengths.append(count)
      count = 0 

      j += 1

  return chunkLengths


def pulsar_estimate_snr(source, det, tstart, duration, Sn, dt=1800):
  """
  A function to estimate the signal-to-noise ratio of a pulsar signal (for a triaxial neutron
  star emitting at twice the rotation frequency from the l=m=2 quadrupole mode) in a given
  detector over a given time range, for a given one-sided power spectral density.

  Inputs
  ------
      source - a dictionary containing 'h0', 'cosiota', 'psi', 'ra' (rads or string), 'dec' (rads or string)
         det - the detector, e.g. 'H1'
      tstart - a GPS start time
    duration - a signal duration (seconds)
          Sn - a one-sided power spectral density
          dt - timestep for antenna response calculation [default: 1800s]

  Returns
  -------
  rho        - an estimate of the optimal matched filter SNR
  """

  
  sidday = 86164.0905 
  Ndays = duration/sidday
  Nsamps = np.floor(sidday/dt) 
  tend = tstart + duration

  sFp = 0
  sFc = 0

  
  if Ndays > 1:
    tts = np.arange(tstart, tstart+sidday, dt)

    
    Fp, Fc = antenna_response(tts, source['ra'], source['dec'], source['psi'], det )

    sFp = np.floor(Ndays)*np.sum(Fp**2)
    sFc = np.floor(Ndays)*np.sum(Fc**2)

  
  if np.floor(Ndays)*sidday > dt:
    tts = np.arange(tstart+sidday*np.floor(Ndays), tend, dt)

    Fp, Fc = antenna_response(tts, source['ra'], source['dec'], source['psi'], det)

    sFp += np.sum(Fp**2)
    sFc += np.sum(Fc**2)

  
  snr2 = (source['h0']**2/Sn)*dt*(sFp*(0.5*(1+source['cosiota']**2))**2 + sFc*source['cosiota']**2)

  return np.sqrt(snr2)


def pulsar_estimate_h0_from_snr(snr, source, det, tstart, duration, Sn, dt=600):
  """
  A function to estimate the signal amplitude of a pulsar signal (for a triaxial neutron star emitting at twice
  the rotation frequency from the l=m=2 quadrupole mode) for a given SNR in a particular detector over
  a given time range, for a given one-sided power spectral density.

  Inputs
  ------
         snr - the optimal matched filter signal-to-noise ratio
      source - a dictionary containing 'cosiota', 'psi', 'ra' (rads or string), 'dec' (rads or string)
         det - the detector, e.g. 'H1'
      tstart - a GPS start time for the signal
    duration - a signal duration (seconds)
          Sn - a one-sided power spectral density
          dt - timestep for antenna response calculation [default: 600s]

  Returns
  -------
  h0         - an estimate of signal amplitude required to give the input SNR
  """

  
  sidday = 86164.0905 
  Ndays = duration/sidday
  Nsamps = np.floor(sidday/dt) 
  tend = tstart + duration

  sFp = 0
  sFc = 0

  
  if Ndays > 1:
    tts = np.arange(tstart, tstart+sidday, dt)

    
    Fp, Fc = antenna_response(tts, source['ra'], source['dec'], source['psi'], det )

    sFp = np.floor(Ndays)*np.sum(Fp**2)
    sFc = np.floor(Ndays)*np.sum(Fc**2)

  
  if np.floor(Ndays)*sidday > dt:
    tts = np.arange(tstart+sidday*np.floor(Ndays), tend, dt)

    Fp, Fc = antenna_response(tts, source['ra'], source['dec'], source['psi'], det)

    sFp += np.sum(Fp**2)
    sFc += np.sum(Fc**2)

  
  h02 = (snr**2*Sn)/(dt*(sFp*(0.5*(1+source['cosiota']**2))**2 + sFc*source['cosiota']**2))

  return np.sqrt(h02)


def pulsar_posterior_grid(dets, ts, data, ra, dec, sigmas=None, paramranges={}, datachunks=30, chunkmin=5,
                          ngrid=50, outputlike=False):
  """
  A function to calculate the 4-parameter posterior probability density for a continuous wave signal
  given a set of processed data from a set of detectors.

  Inputs
  ------
         dets - a list of strings containing the detectors being used in the likelihood calculation
           ts - a dictionary of 1d numpy arrays containing the GPS times of the data for each detector
         data - a dictionary of 1d numpy arrays containing the complex data values for each detector
           ra - the right ascension (in rads) of the source
          dec - the declination (in rads) of the source
       sigmas - a dictionary of 1d numpy arrays containing the times series of standard deviation
                values for each detector. If this is not given a Student's t likelihood will be used,
                but if it is given a Gaussian likelihood will be used (default: None)
  paramranges - a dictionary of tuples for each parameter ('h0', 'phi0', 'psi' and 'cosiota') giving
                the lower and upper ranges of the parameter grid and the number of grid points. If not
                given then defaults will be used.
   datachunks - in the calculation split the data into stationary chunks with a maximum length given
                by this value. If set to 0 or inf then the data will not be split. (default: 30)
     chunkmin - this is the shortest chunk length allowed to be included in the likelihood calculation
                (default: 5)
        ngrid - the number of grid points to use for each dimension of the likelihood calculation. This
                is used if the values are not specified in the paramranges argument (default: 50)
   outputlike - output the log likelihoods rather than posteriors (default: False)

  Returns
  -------
  L           - The 4d posterior (or likelihood) over all parameters
  h0pdf       - The 1d marginal posterior for h0
  phi0pdf     - The 1d marginal posterior for phi0 (the rotation frequency, not GW frequency)
  psipdf      - The 1d marginal posterior for psi
  cosiotapdf  - The 1d marginal posterior for cosiota
  lingrids    - A dictionary of the grid points for each parameter
  sigev       - The log evidence for the signal model
  noiseev     - The log evidence for the noise model

  An example would be:
  
  dets = ['H1', 'L1']

  
  ts = {}
  data = {}
  for det in dets:
    ts[det] = np.arange(900000000., 921000843., 60.)
    data[det] = np.random.randn(len(ts[det])) + 1j*np.random.randn(len(ts[det]))

  
  ra = 0.2
  dec = -0.8
  paramranges = {}
  paramranges['h0'] = (0., 2., 50)
  paramranges['psi'] = (0., np.pi/2., 50)
  paramranges['phi0'] = (0., np.pi, 50)
  paramranges['cosiota'] = (-1., 1., 50)

  L, h0pdf, phi0pdf, psipdf, cosiotapdf, grid, sigev, noiseev = pulsar_posterior_grid(dets, ts, data, ra, dec,
                                                                                      paramranges=paramranges)
  """

  
  import numpy as np
  import sys
  from scipy.special import gammaln

  
  if sigmas == None:
    liketype = 'studentst'
  else:
    liketype = 'gaussian'

  
  if not isinstance(dets, list):
    if isinstance(dets, basestring):
      dets = [dets] 
    else:
      print('Detector not, or incorrectly, set', file=sys.stderr)
      return

  
  alloweddets = ['H1', 'L1', 'V1', 'G1', 'T1', 'H2']

  
  for det in dets:
    if det not in alloweddets:
      print('Detector not in list of allowed detectors (' + ','.join(alloweddets) + ')', file=sys.stderr)
      return

    
    if det not in ts:
      print('No time stamps given for detector %s' % det, file=sys.stderr)
      return

    
    if det not in data:
      print('No data time series given for detector %s' % det, file=sys.stderr)
      return

    
    if sigmas != None:
      if det not in sigmas:
        print('No sigma time series given for detector %s' % det, file=sys.stderr)
        return

    
    if len(ts[det]) != len(data[det]):
      print('Length of times stamps array and data array are inconsistent for %s' % det, file=sys.stderr)

    if sigmas != None:
      if len(ts[det]) != len(sigmas[det]):
        print('Length of times stamps array and sigma array are inconsistent for %s' % det, file=sys.stderr)

  
  params = ['h0', 'phi0', 'psi', 'cosiota']
  defaultranges = {} 
  defaultranges['phi0'] = (0., np.pi, ngrid) 
  defaultranges['psi'] = (0., np.pi/2., ngrid) 
  defaultranges['cosiota'] = (-1., 1., ngrid) 
  
  defaultranges['h0'] = (0., 2.*np.max([np.std(data[dv]) for dv in data])* \
    np.sqrt(1440./np.max([len(ts[dtx]) for dtx in ts])), ngrid)
  lingrids = {}
  shapetuple = ()
  for param in params:
    if param in paramranges:
      if len(paramranges[param]) != 3:
        paramranges[param] = defaultranges[param] 
      else:
        if paramranges[param][1] < paramranges[param][0] or paramranges[param][2] < 1:
          print("Parameter ranges wrong for %s, reverting to defaults" % param, file=sys.stderr)
          paramranges[param] = defaultranges[param]
    else: 
      paramranges[param] = defaultranges[param]

    lingrids[param] = np.linspace(paramranges[param][0], paramranges[param][1], paramranges[param][2])
    shapetuple += (paramranges[param][2],)

  
  [H0S, PHI0S, PSIS, COSIS] = np.meshgrid(lingrids['h0'], lingrids['phi0'], lingrids['psi'],
                                          lingrids['cosiota'], indexing='ij')

  APLUS = 0.5*(1.+COSIS**2)
  ACROSS = COSIS
  SINPHI = np.sin(2.*PHI0S) 
  COSPHI = np.cos(2.*PHI0S)
  SIN2PSI = np.sin(2.*PSIS)
  COS2PSI = np.cos(2.*PSIS)

  Apsinphi_2 = 0.5*APLUS*SINPHI
  Acsinphi_2 = 0.5*ACROSS*SINPHI
  Apcosphi_2 = 0.5*APLUS*COSPHI
  Accosphi_2 = 0.5*ACROSS*COSPHI
  Acpsphicphi_2 = 0.5*APLUS*ACROSS*COSPHI*SINPHI

  AP2 = APLUS**2
  AC2 = ACROSS**2
  TWOAPACSPCP = 2.*APLUS*ACROSS*SINPHI*COSPHI
  SP2 = SINPHI**2
  CP2 = COSPHI**2

  C2PS2P = COS2PSI*SIN2PSI
  C2P2 = COS2PSI**2
  S2P2 = SIN2PSI**2

  H02 = H0S**2

  
  like = np.zeros(shapetuple)
  noiselike = 0.

  
  logprior = 0.
  for p in params:
    logprior -= np.log(paramranges[p][1]-paramranges[p][0])

  
  for det in dets:
    if liketype == 'gaussian':
      nstd = sigmas[det]
    else:
      nstd = np.ones(len(ts[det]))

    
    [As, Bs] = antenna_response( ts[det], ra, dec, 0.0, det )

    
    if np.isfinite(datachunks) and datachunks > 0:
      chunklengths = get_chunk_lengths(ts[det], datachunks)
    else:
      chunklengths = [len(ts[det])]

    startidx = 0
    for cl in chunklengths:
      endidx = startidx + cl

      
      if cl < chunkmin:
        continue

      thisdata = data[det][startidx:endidx]/nstd[startidx:endidx]
      ast = As[startidx:endidx]/nstd[startidx:endidx]
      bst = Bs[startidx:endidx]/nstd[startidx:endidx]

      A = np.sum(ast**2)
      B = np.sum(bst**2)
      AB = np.dot(ast, bst)

      dA1real = np.dot(thisdata.real, ast)
      dA1imag = np.dot(thisdata.imag, ast)

      dB1real = np.dot(thisdata.real, bst)
      dB1imag = np.dot(thisdata.imag, bst)

      dd1real = np.sum(thisdata.real**2)
      dd1imag = np.sum(thisdata.imag**2)

      P1 = A*C2P2 + B*S2P2 + 2.*AB*C2PS2P
      P2 = B*C2P2 + A*S2P2 - 2.*AB*C2PS2P
      P3 = AB*(C2P2 - S2P2) - A*C2PS2P + B*C2PS2P

      hr2 = (Apcosphi_2**2)*P1 + (Acsinphi_2**2)*P2 + Acpsphicphi_2*P3
      hi2 = (Apsinphi_2**2)*P1 + (Accosphi_2**2)*P2 - Acpsphicphi_2*P3

      d1hr = Apcosphi_2*(dA1real*COS2PSI + dB1real*SIN2PSI) + Acsinphi_2*(dB1real*COS2PSI - dA1real*SIN2PSI)
      d1hi = Apsinphi_2*(dA1imag*COS2PSI + dB1imag*SIN2PSI) - Accosphi_2*(dB1imag*COS2PSI - dA1imag*SIN2PSI)

      chiSq = dd1real + dd1imag + H02*(hr2 + hi2) - 2.*H0S*(d1hr + d1hi)

      if liketype == 'gaussian':
        like -= 0.5*(chiSq)
        like -= (cl*np.log(2.*np.pi)) + 2.*np.sum(np.log(nstd[startidx:endidx]))
        noiselike -= 0.5*(dd1real + dd1imag)
        noiselike -= (cl*np.log(2.*np.pi)) + 2.*np.sum(np.log(nstd[startidx:endidx]))
      else:
        like -= float(cl)*np.log(chiSq)
        like += (gammaln(cl) - np.log(2.) - cl*np.log(np.pi))
        noiselike -= float(cl)*np.log(dd1real + dd1imag)
        noiselike += (gammaln(cl) - np.log(2.) - cl*np.log(np.pi))

      startidx += cl 

  
  like += logprior

  
  sigev = marginal(like, 'all', params, lingrids)

  
  if not outputlike:
    like -= sigev
  else:
    like -= logprior 

  
  posts = {}
  for p in params:
    if not outputlike:
      posts[p] = np.exp(marginal(like, p, params, lingrids))
    else:
      posts[p] = marginal(like, p, params, lingrids, multflatprior=True) 

  
  evrat = sigev - noiselike

  return like, posts['h0'], posts['phi0'], posts['psi'], posts['cosiota'], lingrids, sigev, noiselike



ATNF_VERSION = '1.56'

def get_atnf_info(psr):
  """
  Get the pulsar (psr) distance (DIST in kpc), proper motion corrected period derivative (P1_I) and any association
  (ASSOC e.g. GC) from the ATNF catalogue.
  """

  psrname = re.sub('\+', '%2B', psr) 

  atnfurl = 'http://www.atnf.csiro.au/people/pulsar/psrcat/proc_form.php?version=' + ATNF_VERSION
  atnfurl += '&Dist=Dist&Assoc=Assoc&P1_i=P1_i' 
  atnfurl += '&startUserDefined=true&c1_val=&c2_val=&c3_val=&c4_val=&sort_attr=jname&sort_order=asc&condition=&pulsar_names=' + psrname
  atnfurl += '&ephemeris=selected&submit_ephemeris=Get+Ephemeris&coords_unit=raj%2Fdecj&radius=&coords_1=&coords_2='
  atnfurl += '&style=Long+with+last+digit+error&no_value=*&fsize=3&x_axis=&x_scale=linear&y_axis=&y_scale=linear&state=query'

  try:
    urldat = urllib2.urlopen(atnfurl).read() 
    predat = re.search(r'<pre[^>]*>([^<]+)</pre>', urldat) 
    pdat = predat.group(1).strip().split('\n') 
  except:
    print("Warning... could not get information from ATNF pulsar catalogue.", file=sys.stderr)
    return None

  
  dist = None
  p1_I = None
  assoc = None
  for line in pdat:
    if 'WARNING' in line or 'not in catalogue' in line:
      return None
    vals = line.split()
    if 'DIST' in vals[0]:
      dist = float(vals[1])
    if 'P1_I' in vals[0]:
      age = float(vals[1])
    if 'ASSOC' in vals[0]:
      assoc = vals[1]

  return (dist, p1_I, assoc, atnfurl)


def cov_to_cor(cov):
  """
  Convert a covariance matrix to a correlation coefficient matrix.
  Return the correlation coefficient matrix and the standard deviations
  from the covariance matrix.
  """

  
  sigmas = np.sqrt(np.diag(cov))

  
  D = sigmas*np.identity(cov.shape[0])

  
  Dinv = np.linalg.inv(D)

  
  Ccor = np.dot(np.dot(Dinv, cov), Dinv)

  return Ccor, sigmas
