from astropy.constants import c
from astropy.coordinates import Galactic
import warnings
import os
import PIL
import numpy as np
import healpy as hp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mycmap import get_continuous_cmap

def histeq(im,nbr_bins=256):
   # adapted from 
   # https://web.archive.org/web/20151219221513/http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html

   #get image histogram
   infmask = im==-np.inf
   imhist,bins = np.histogram(im.flatten(),nbr_bins,density=True,range=(0,im.max()))
   cdf = imhist.cumsum() #cumulative distribution function
   cdf = 255 * cdf / cdf[-1] #normalize

   #use linear interpolation of cdf to find new pixel values
   im2 = np.interp(im.flatten(),bins[:-1],cdf).reshape(im.shape)
   im2[infmask] = np.nan

   return im2, cdf

def generate_projection_set(m,size,dname,coord=['G'],cmap='viridis',norm='hist'):
    """
    Generate a set of 6 square, unpadded orthographic projections of a 
    healpix map, with centers at the following lon/lat:

    (0,90)  / (0,-90)    North pole / South pole
    (0,0)   / (180/0)    centered on equator
    (45,45) / (215,-45)  off-axis

    Parameters
    ----------
    m : ndarray
        healpix array to be mapped

    size : int
        width of each image in pixels

    dname : str
        name of directory to contain output images

    coord : sequence of character
        Either one of ‘G’, ‘E’ or ‘C’ to describe the coordinate system of 
        the map, or a sequence of 2 of these to rotate the map from the 
        first to the second coordinate system. (default "G")

    norm : {‘hist’, ‘log’, None}
        Color normalization, hist= histogram equalized color mapping, log= logarithmic color mapping, default: None (linear color mapping)
    
    cmap : a color map
        The colormap to use (see matplotlib.cm)

    """
    
    # Check whether size is power of 2
    if not np.ceil(np.log2(size))==np.log2(size):
        warnings.warn("Image size is not a power of 2")
    
    # Check if directory exists, make _copy if not, make directory
    def unique_dname(dname):
        if os.path.exists(os.path.join(os.getcwd(),dname)):
            warnings.warn("Directory already exists; ")
            return unique_dname(dname+'_copy')
        else:
            return dname
    
    dirname = unique_dname(dname)
    os.mkdir(dirname)

    centers = [(0,90),
               (0.0),
               (45,45)]
    fnames = [('northpole','southpole'),
              ('primemeridian','antimeridian'),
              ('offaxis','antioffaxis')]

    for i,rot in enumerate(centers):
        image_linear = hp.orthview(m,rot=rot,xsize=2*size,coord=coord,return_projected_map=True,cmap=cmap,norm=norm,min=0)
        
        if norm=='hist':
            # renormalize with histogram equalization
            image,_ = histeq(image_linear)
            vmin = 0
            vmax = np.max(image[~np.isnan(image)])
        
        elif norm=='log':
            warnings.warn('Log normalization not yet implemented')
        
        plt.imsave(fname=dirname+'/'+fnames[i][0]+'.png',
                   arr=image[:,:size],
                   vmin=vmin,
                   vmax=vmax,
                   origin='lower',
                   cmap=cmap,
                   format='png')

        plt.imsave(fname=dirname+'/'+fnames[i][1]+'.png',
                   arr=image[:,size:],
                   vmin=vmin,
                   vmax=vmax,
                   origin='lower',
                   cmap=cmap,
                   format='png')


if __name__=="__main__":
    lon = 215
    lat = -45
    print('lat: {:0.2f} \nlon: {:0.2f}'.format(lat,lon))

    ns = 16
    test_map = np.arange(hp.nside2npix(ns))

    ipix = hp.ang2pix(ns,np.pi/2-np.pi*lat/180,np.pi*lon/180)
    test_map[ipix] = 1.5*test_map.max()

    generate_projection_set(test_map,512,'testset')