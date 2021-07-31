import numpy as np
import raster_geometry as rg

def lines(n, spacing_px):
    size=[n,n]
    field=np.empty(size,'float32')

    field[int(n/4):int(3*n/4), int(n/2) - spacing_px] = 1
    field[int(n/4):int(3*n/4), int(n/2) + spacing_px] = 1
    field = field + np.roll(field, [0, round(n/3)]) + np.roll(field, [0, -round(n/3)])

    field[int(7*n/8) - spacing_px, int(n/4):int(3*n/4)] = 1
    field[int(7*n/8) + spacing_px, int(n/4):int(3*n/4)] = 1

    field[int(n/2) - spacing_px, int(n/16):int(15*n/16)] = 1
    field[int(n/2) + spacing_px, int(n/16):int(15*n/16)] = 1 
    
    return field

def sphere3d(size, radius):
    return rg.sphere(size, radius).astype(np.float32)




