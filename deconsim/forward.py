import numpy as np

def forward(img, otf):
    fftimg = np.fft.fft2(img)
    return np.fft.ifft2(fftimg*otf)