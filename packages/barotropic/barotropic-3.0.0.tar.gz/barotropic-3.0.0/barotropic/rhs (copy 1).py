"""RHS forcing terms in spectral space"""

import functools
import numbers
import numpy as np

from .constants import ZONAL



class RHS:
    """RHS term base class that implements arithmetic operators"""

    def __add__(self, other):
        return RHSSum(self, other)

    def __radd__(self, other):
        return RHSSum(other, self)

    def __mul__(self, other):
        return RHSProduct(self, other)

    def __rmul__(self, other):
        return RHSProduct(other, self)


class RHSSum(RHS):

    def __init__(self, term1, term2):
        self._term1 = term1
        self._term2 = term2

    def __call__(self, state):
        return self._term1(state) + self._term2(state)

    def __repr__(self):
        return "({} + {})".format(repr(self._term1), repr(self._term2))


class RHSProduct(RHS):

    def __init__(self, term1, term2):
        self._term1 = term1
        self._term2 = term2

    def __call__(self, state):
        return self._term1(state) * self._term2(state)

    def __repr__(self):
        return "({} * {})".format(repr(self._term1), repr(self._term2))


class TimedOffSwitch(RHS):
    """Turn off another forcing term after a specified amount of time
    
    The forcing term returns 1 until the specified switch-off time is reached
    after which it returns 0 forever. Multiply with the term that is supposed
    to be switched off.
    """

    def __init__(self, tend):
        """Set the switch-off time with `tend` in s"""
        self._tend = tend

    def __call__(self, state):
        return 1 if state.time <= self._tend else 0


class LinearRelaxation(RHS):
    """Linear relaxation towards a reference PV state"""

    def __init__(self, rate, reference_pv, mask=None):
        """"""
        self._rate = rate
        self._reference_pv = reference_pv
        # TODO: mask (allows implementation of sponge-like forcing)

    def __call__(self, state):
        return self._rate * (self._reference_pv - state.pv)


class Orography(RHS):
    """Pseudo-orographic forcing"""

    def __init__(self, lons, lats, orography, scale_height=10000., wind=("act", 1.), fref=None):
        """TODO"""
        self._lons = lons
        self._lats = lats
        self._orography = orography
        self._scale_height = scale_height
        self._fref = fref
        # ...
        wind_kind, wind_fact = wind
        if wind_kind == "act":
            self._get_wind = lambda state: (wind_fact * state.u, wind_fact * state.v)
        elif wind_kind == "zon":
            self._get_wind = lambda state: (wind_fact * np.mean(state.u, axis=ZONAL, keepdims=True), 0.)
        elif wind_kind == "sbr":
            self._get_wind = lambda state: (wind_fact * np.cos(state.grid.phis)[:,None], 0.)
        else:
            raise ValueError("wind specification error")

    @functools.lru_cache(maxsize=8)
    def orography(self, grid):
        """TODO"""
        # Interpolate given orography to grid. Because np.interp requires
        # increasing x-values, flip sign of lats which range from +90° to -90°.
        lat_interp = lambda x: np.interp(-grid.lats, -self._lats, x)
        lon_interp = lambda x: np.interp( grid.lons,  self._lons, x)
        # 2D linear interpolation
        orog = np.apply_along_axis(lat_interp, 0, self._orography)
        return np.apply_along_axis(lon_interp, 1, orog)

    def __call__(self, state):
        grid = state.grid
        # Fixed coriolis parameter if given or use actual values from grid
        fcor = grid.fcor if self._fref is None else self._fref
        # Get orography height field
        orog = self.orography(grid)
        # Zonal wind to use in forcing term:
        # The current wind
        u, v = self._get_wind(state)
        # Evaluate -f/H u·grad(orog)
        gradx, grady = grid.gradient(orog)
        return -fcor / self._scale_height * (u * gradx + v * grady)


class GaussianMountain(Orography):
    """Gaussian-shaped pseudo-orography"""

    # TODO adapt documentation
    def __init__(self, height=1500, center=(30., 45.), stdev=(7.5, 20.), **orog_kwargs):
        """Gaussian mountain for pseudo-orographic forcing
        
        The mountain is centered at the (lon, lat)-tuple `center` (in degrees),
        decays with zonal and meridional standard deviations given by the tuple
        or value `stdev` (in degrees) and has an amplitude of `amplitude`
        (dimensionless). The forcing is calculated with a fixed coriolis
        parameter `fcor0` (in 1/s) and reference zonal wind `u_ref` (in m/s).
        """
        super().__init__(None, None, None, **orog_kwargs)
        # Mountain properties for orography method
        self._height = height
        self._center_lon, self._center_lat = center
        if isinstance(stdev, numbers.Number):
            stdev = (stdev, stdev)
        self._stdev_lon_sq = stdev[0] ** 2
        self._stdev_lat_sq = stdev[1] ** 2

    @functools.lru_cache(maxsize=8)
    def orography(self, grid):
        return (self._height
                # Decaying in zonal direction
                * ( np.exp(-0.5 * (grid.lon - self._center_lon)**2 / self._stdev_lon_sq) )
                # Decaying in meridional direction
                * ( np.exp(-0.5 * (grid.lat - self._center_lat)**2 / self._stdev_lat_sq) ))


class ZonalSineMountains(Orography):
    """Sinusoidal pseudo-orography in the zonal direction"""

    def __init__(self, height=1500, center_lat=45., stdev_lat=10., wavenumber=4, **orog_kwargs):
        """Sinusoidal mountain-chain for pseudo-orographic forcing

        The mountains are centered at latitude `center_lat` (in degrees) and
        decay in meridional direction with a standard deviation of `stdev_lat`
        (in degrees). Their `wavenumber` and `amplitude` are dimensionless
        parameters. The forcing is calculated with a fixed coriolis parameter
        `fcor0` (in 1/s) and reference zonal wind `u_ref` in (m/s).
        """
        super().__init__(None, None, None, **orog_kwargs)
        # Mountain chain properties for orography method
        self._height = height
        self._center_lat = center_lat
        self._stdev_lat_sq = stdev_lat ** 2
        self._wavenumber = wavenumber

    @functools.lru_cache(maxsize=8)
    def orography(self, grid):
        return (self._height
                # Periodic in zonal direction
                * ( 0.5 * (1 + np.cos(self._wavenumber * grid.lam)) )
                # Decaying in meridional direction
                * ( np.exp(-0.5 * (grid.lat - self._center_lat)**2 / self._stdev_lat_sq) ))


class EarthOrography(Orography):
    """"""

    _lons = np.linspace( 0, 360, 37, endpoint=True) # 0° = 360° is duplicated
    _lats = np.linspace(90, -90, 37, endpoint=True)
    # Earth's orography with 5° lat- and 10° lon-resolution
    _orography = 100. * np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,11,0,9,19,21,16,1,0,0],
        [0,0,0,0,0,0,2,0,0,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,3,1,0,0,24,29,26,0,0,0],
        [0,0,0,0,0,0,0,0,1,6,4,6,2,7,5,2,0,0,0,0,0,1,0,0,0,1,0,0,0,7,0,4,29,19,0,0,0],
        [0,0,3,2,0,2,10,1,0,4,5,5,2,13,11,2,5,2,0,0,4,2,10,14,4,5,2,3,0,3,0,9,0,0,7,0,0],
        [0,3,0,0,2,2,2,1,1,1,3,4,3,3,7,4,0,0,0,0,6,12,7,11,5,3,3,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,2,1,1,4,1,1,5,6,12,8,7,0,0,7,0,0,0,0,0,0,5,9,7,3,1,0,5,1,0,0,0,0,0,0],
        [0,3,3,2,1,0,3,4,4,22,18,15,7,2,4,0,0,0,0,0,0,0,0,0,15,8,5,5,3,5,0,0,0,0,0,0,0],
        [1,1,1,0,1,-0,0,2,33,10,21,10,9,4,0,0,0,0,0,0,0,0,0,0,11,26,6,4,2,3,0,0,0,0,0,0,1],
        [1,0,4,9,20,-0,2,15,11,8,15,13,0,0,0,0,0,0,0,0,0,0,0,0,16,17,7,2,3,0,0,0,0,0,0,0,1],
        [7,2,0,0,3,15,17,29,50,50,40,5,0,0,0,0,0,0,0,0,0,0,0,0,8,16,6,1,1,0,0,0,0,0,0,0,7],
        [5,4,0,2,7,0,14,12,20,54,45,13,2,0,0,0,0,0,0,0,0,0,0,0,0,11,7,0,0,0,0,0,0,0,0,0,5],
        [3,9,4,2,10,2,0,1,2,0,19,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,13,0,0,0,0,0,0,0,0,3,3],
        [4,5,6,3,0,3,0,0,2,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,26,1,0,0,0,0,0,0,0,4,4],
        [3,5,4,5,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,0,0,0,0,0,0,0,3,3],
        [2,5,4,4,13,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,5,2],
        [0,8,4,7,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,10,0,0,0,0,0,0],
        [0,0,4,11,2,0,0,0,0,0,4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,1,0,0,0,0,0,0],
        [0,0,5,10,0,0,0,0,0,0,0,0,5,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,11,1,0,2,5,0,0,0,0],
        [0,0,11,15,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,2,5,0,0,0,0],
        [0,0,12,8,2,4,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,3,6,4,0,0,0,0],
        [0,0,12,11,0,0,0,0,0,0,0,0,0,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,2,4,0,0,0,0,0],
        [0,0,11,12,0,0,0,0,0,0,0,0,6,6,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,21,1,10,0,0,0,0,0],
        [0,0,10,11,0,0,0,0,0,0,0,0,5,2,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,38,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,31,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,9,24,26,1,19,26,25,25,24,26,24,14,4,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0],
        [29,33,35,34,35,33,23,19,30,36,35,32,32,31,27,24,12,0,0,0,0,0,0,6,9,1,1,10,9,14,0,0,0,0,0,24,29],
        [23,28,31,34,36,37,37,39,40,38,36,33,31,28,24,20,4,1,0,1,1,1,4,11,15,18,21,20,4,1,1,4,1,2,9,18,23],
        [26,26,27,29,32,33,34,34,34,33,32,31,30,29,28,27,24,20,23,17,1,1,3,9,17,21,22,20,13,13,13,16,18,21,23,24,26],
        [28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28]
    ])

    def __init__(self, **orog_kwargs):
        super().__init__(self._lons, self._lats, self._orography, **orog_kwargs)

