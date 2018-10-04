# pytrack

Find the minimum value using biquadratic interpolation.

## Algorithm

* Find local minima by scipy.ndimage.filters.minimum_filter() assuming a cyclic boundary conditon in longitude
* Find the grid of the minimum closest to the initial guess in geodesic distance
* Generate nine point stencil with the minimum on grid at the centre
* Interpolate for the minimum in-between grid using biquadratic interpolation
* If interpolation fails use the minimum on grid

## Files

* biquadratic.py: biquadratic interpolation
* grid.py: call grid.find_minimum() with an array and initial guess
* track.py.sample: example driver script