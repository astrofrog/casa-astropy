from astropy.wcs import WCS


def wcs_casa2astropy(casa_wcs):
    """
    Convert a CASA coordsys object into an astropy.wcs.WCS object
    """

    wcs = WCS(naxis=casa_wcs.naxes())

    wcs.crpix = casa_wcs.referencepixel()['numeric']
    wcs.cdelt = casa_wcs.increment()['numeric']
    wcs.crval = casa_wcs.referencevalue()['numeric']
    wcs.units = casa_wcs.units()

    # There is no easy way at the moment to extract the orginal projection
    # codes from a coordsys object, so we need to figure out how to do this in
    # the most general way.
    # wcs.ctype = ...

    return wcs
