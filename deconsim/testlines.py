import matplotlib.pyplot as plt
import psfs
import phantoms
import forward
import numpy as np

n=765
spacing_px=4
wavelength = 500
na=1.4
pixel_size = 20

print('decon sim test')
img = phantoms.lines(n,spacing_px)
plt.imshow(img)

psf=psfs.paraxial_psf(n, wavelength, na, pixel_size)

plt.figure()
plt.imshow(psf)

img = forward.forward(img, psf,100,1000)
plt.figure()
plt.imshow(np.real(img))

plt.show()