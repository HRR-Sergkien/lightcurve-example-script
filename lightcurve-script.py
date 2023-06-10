
import os
import glob
import numpy as np
import matplotlib as mpl
#mpl.use("Qt5Agg")
#import matplotlib as mpl
import matplotlib.pyplot as plt
from astropy.io import fits

#-- import of the lightcurve package
import lightcurve


#-- Increase the default fontsize for the plots
mpl.rcParams['font.size'] = 10

#-- timefilter and CalCOS need reference files to function.
os.environ['lref'] = '/Users/hrrsergio/crds_cache/references/hst/lref'
w1=[1140,1363]
w2=[1140,1363]
step=5
x1d_all=glob.glob('/Users/hrrsergio/PhD_Warwick/HST-data/*_x1d.fits')
corrtag_a=glob.glob('/Users/hrrsergio/PhD_Warwick/HST-data/*_corrtag_a.fits')
x1d=[c for c in x1d_all if fits.open(c)[0].header['rootname']=='le8z01eiq']
corr=[c for c in corrtag_a if fits.open(c)[0].header['rootname']=='le8z01eiq']

x1d_1222=[c for c in x1d_all if fits.open(c)[0].header['cenwave']==1222]
x1d_1291=[c for c in x1d_all if fits.open(c)[0].header['cenwave']==1291]




fig,ax=plt.subplots(nrows=1,ncols=1,sharex=False, sharey=False,gridspec_kw={'hspace': 0.3,'wspace':0.1},figsize=(11,15))


for i in range(len(corrtag_a)):
    #This is where the magic happens
    lc1=lightcurve.cos.extract(filename=corrtag_a[i],step=step,wlim=w1,filter_airglow=True)
    #NOTE: even if wavelength region is not in corrtag_a, the function
    #will look in the same folder to find corrtag_b!!
  
    flux_1=lc1[0]['flux']
    mjd_1=lc1[0]['mjd']
    gross_1=lc1[0]['gross']
    times_1=lc1[0]['times']
    name=lc1[1]['headers']['A'][0][15][1] #Worst way to retrieve the file name XD
    cw=lc1[1]['headers']['A'][0][-25][1]   #TO GET CENTRALWAVE 

    ax.plot(mjd_1,flux_1,'o',markersize=3,linestyle='none',label=name+' -- cw: '+str(cw))
    ax.legend(loc='upper center', bbox_to_anchor=(0.45, 1.15),ncol=3, fancybox=True, shadow=False)

fig.text(0.06, 0.5, 'Flux [erg $cm^{-2}\AA^{-1}s^{-1}$]', va='center', rotation='vertical',size=15)
fig.text(0.5, 0.07, 'MJD', ha='center',size=15)


fig.savefig('lightcurve.pdf', bbox_inches='tight')
