import matplotlib.pyplot as plt
import psfs
import phantoms
import forward
import numpy as np

xy_size=int(512);
z_size=int(100);
num_blocks=int(4);
r=30

full_size=[z_size, xy_size, xy_size];
block_size=[z_size, int(xy_size/num_blocks), int(xy_size/num_blocks)];

img = np.zeros(full_size); 

for i in range(num_blocks-1):
    for j in range(num_blocks-1):
        print(i,j)

        img[:,i*block_size[1]+int(block_size[1]/2):i*block_size[1]+int(block_size[1]/2)+block_size[1],j*block_size[2]+int(block_size[2]/2):j*block_size[2]+int(block_size[2]/2)+block_size[2]] = phantoms.sphere3d(block_size,r)

fig = plt.figure()
plt.imshow(img[int(full_size[0]/2),:,:])

pixel_size = 0.05

zv = np.arange(-full_size[0]*pixel_size/2, full_size[0]*pixel_size/2, pixel_size)

plt.figure()
plt.imshow(img[int(full_size[0]/2),:,:])

psf_xyz = psfs.gibson_lanni_3D(1.4, 1.53, 1.4, pixel_size, xy_size, zv, 0.1)
psf_xyz_small = psfs.gibson_lanni_3D(1.4, 1.53, 1.4, pixel_size, 256, zv, 0.1)

plt.imshow(psf_xyz_small[int(full_size[0]/2),:,:])

forward = forward.forward(img, psf_xyz, 100, 100, True)

plt.figure()
plt.imshow(forward[int(forward.shape[0]/2),:,:])

plt.show()

import tifffile
tifffile.imwrite('./spheres.tiff', forward.astype('float32'), imagej=True, metadata={'axes': 'ZYX'})
tifffile.imwrite('./psf.tiff', psf_xyz_small.astype('float32'), imagej=True, metadata={'axes': 'ZYX'})



