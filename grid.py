# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.minimum_filter
# https://stackoverflow.com/questions/3986345/how-to-find-the-local-minima-of-a-smooth-multidimensional-array-in-numpy-efficie
import numpy as np
from scipy import ndimage
import biquadratic

def __set_stencil(g, i0, j0):
    ny, nx = g.shape
    ia = (i0 + nx - 1) % nx
    ib = (i0 + 1) % nx
    ja = max(j0 - 1, 0)
    jb = min(j0 + 1, ny - 1)
    f = np.zeros(9)
    f[0] = g[j0, i0]
    f[1] = g[ja, ia]
    f[2] = g[ja, i0]
    f[3] = g[ja, ib]
    f[4] = g[j0, ib]
    f[5] = g[jb, ib]
    f[6] = g[jb, i0]
    f[7] = g[jb, ia]
    f[8] = g[j0, ia]
    return f

def find_minimum(g, lon, lat, lon0, lat0):
    loc_min = np.where( \
        ndimage.filters.minimum_filter( \
            g, size=(3,3), mode=('nearest', 'wrap')) == g)
    dx = np.deg2rad(lon[loc_min[1]] - lon0)
    y1 = np.deg2rad(lat[loc_min[0]])
    y0 = np.deg2rad(lat0)
    d = np.arccos(np.sin(y0) * np.sin(y1) + np.cos(y0) * np.cos(y1) * np.cos(dx))
    n = np.argmin(d)
    imin = loc_min[1][n]
    jmin = loc_min[0][n]
    f = __set_stencil(g, imin, jmin)
    x, y, gmin = biquadratic.interpolate(f)
    dlon = lon[1] - lon[0]
    lon0 = (lon[imin] + x * dlon) % 360
    dlat = 0.5 * (lat[min(jmin + 1, lat.size-1)] - lat[max(jmin - 1, 0)])
    lat0 = min(max(lat[jmin] + y * dlat, -90), 90)
    return lon0, lat0, gmin

    