from numpy.fft import fft2, ifft2 
from numpy.random import poisson

def forward(field, otf, max_photons, background_level):
    field_imaged = ifft2(fft2(field)*otf)
    field_imaged = field_imaged/field_imaged.max()
    field_imaged = field_imaged*max_photons+background_level

    return poisson(field_imaged.astype(float))