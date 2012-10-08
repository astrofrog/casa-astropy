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

    crpix = casa_wcs.referencepixel()
    if crpix['ar_type'] != 'absolute':
        raise ValueError("Unexpected ar_type: %s" % crpix['ar_type'])
    elif crpix['pw_type'] != 'pixel':
        raise ValueError("Unexpected pw_type: %s" % crpix['pw_type'])
    else:
        wcs.wcs.crpix = crpix['numeric']

    cdelt = casa_wcs.increment()
    if cdelt['ar_type'] != 'absolute':
        raise ValueError("Unexpected ar_type: %s" % cdelt['ar_type'])
    elif cdelt['pw_type'] != 'world':
        raise ValueError("Unexpected pw_type: %s" % cdelt['pw_type'])
    else:
        wcs.wcs.cdelt = cdelt['numeric']

    crval = casa_wcs.referencevalue()
    if crval['ar_type'] != 'absolute':
        raise ValueError("Unexpected ar_type: %s" % crval['ar_type'])
    elif crval['pw_type'] != 'world':
        raise ValueError("Unexpected pw_type: %s" % crval['pw_type'])
    else:
        wcs.wcs.crval = crval['numeric']

    wcs.wcs.cunit = casa_wcs.units()

    # There is no easy way at the moment to extract the orginal projection
    # codes from a coordsys object, so we need to figure out how to do this in
    # the most general way. The code below is still experimental.
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
