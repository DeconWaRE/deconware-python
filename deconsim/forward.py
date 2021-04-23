from numpy.fft import fftn, ifftn, fftshift 
from numpy.random import poisson

def forward(field, psf, max_photons, background_level):
    ''' Implements forward model '''
    otf = fftn(fftshift(psf))
    field_imaged = ifftn(fftn(field)*otf)
    field_imaged = field_imaged/field_imaged.max()
    field_imaged = field_imaged*max_photons+background_level

    return poisson(field_imaged.astype(float))