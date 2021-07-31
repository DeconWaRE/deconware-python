import matplotlib.pyplot as plt
import psfs
import phantoms
import forward
import numpy as np
import microscPSF as msPSF
from deconsim.richardson_lucy import richardson_lucy_np, richardson_lucy_cp
from clij2fft.libs import getlib
from clij2fft.richardson_lucy import richardson_lucy as richardson_lucy_clij
import time
from clij2fft.pad import pad, get_pad_size, get_next_smooth, unpad
from clij2fft.libs import getlib

xy=101

size=[50,xy,xy]
pixel_size = 0.05

rv = np.arange(0.0, 3.01, pixel_size)
zv = np.arange(-size[0]*pixel_size/2, size[0]*pixel_size/2, pixel_size)

img = phantoms.sphere3d(size,10) #rg.sphere(size, 20).astype(np.float32)

plt.imshow(img[int(size[0]/2),:,:])

psf_xyz = psfs.gibson_lanni_3D(1.4, 1.53, 1.4, pixel_size, xy, zv, 0.1)
plt.imshow(psf_xyz[int(size[0]/2),:,:])

forward = forward.forward(img, psf_xyz, 100, 100)

lib = getlib()
start = time.time()
rl_clij = richardson_lucy_clij(forward, psf_xyz, 100, 0,lib)
end = time.time()
clijtime = end-start

start = time.time()
rl_cupy = richardson_lucy_cp(forward, psf_xyz, 100)
end = time.time()
cupytime = end-start

start = time.time()
rl_np = richardson_lucy_np(forward, psf_xyz, 100)
end = time.time()
cputime = end-start

print('time cpu is',cputime)
print('time cupy is',cupytime)
print('time clij is',clijtime)

fig = plt.figure()
fig.add_subplot(141)
plt.imshow(forward[int(size[0]/2),:,:])
fig.add_subplot(142)
plt.imshow(rl_np[int(size[0]/2),:,:])
fig.add_subplot(143)
plt.imshow(rl_cupy[int(size[0]/2),:,:])
fig.add_subplot(144)
plt.imshow(rl_clij[int(size[0]/2),:,:])

plt.show()

