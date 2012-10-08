import numpy as np
from astropy.wcs import WCS

COORD_TYPE = {}
COORD_TYPE['Right Ascension'] = "RA--"
COORD_TYPE['Declination'] = "DEC-"
COORD_TYPE['Frequency'] = "FREQ"
COORD_TYPE['Stokes'] = "STOKES"


def wcs_casa2astropy(casa_wcs):
    """
    Convert a CASA coordsys object into an astropy.wcs.WCS object
    """

    wcs = WCS(naxis=int(casa_wcs.naxes()))

    wcs.wcs.crpix = casa_wcs.referencepixel()['numeric']
    wcs.wcs.cdelt = casa_wcs.increment()['numeric']
    wcs.wcs.crval = casa_wcs.referencevalue()['numeric']
    wcs.wcs.cunit = casa_wcs.units()

    # There is no easy way at the moment to extract the orginal projection
    # codes from a coordsys object, so we need to figure out how to do this in
    # the most general way.
    ctype = []
    for i, name in enumerate(casa_wcs.names()):
        if name in COORD_TYPE:
            ctype.append(COORD_TYPE[name])
            if casa_wcs.axiscoordinatetypes()[i] == 'Direction':
                ctype[-1] += ("%4s" % casa_wcs.projection()['type']).replace(' ', '-')
        else:
            raise KeyError("Don't know how to convert: %s" % name)

    wcs.wcs.ctype = ctype

    return wcs
