About
=====

This is a directory containing experimental code to convert between CASA
and Astropy objects.

Example
=======

    CASA <1>: ia.open("testcube.fits")
      Out[1]: True

    CASA <2>: d = nddata_casa2astropy(ia)

    CASA <3>: d.wcs
      Out[3]: <astropy.wcs.wcs.WCS object at 0x127d73788>

    CASA <4>: d.data.shape
      Out[4]: (128, 128, 50, 1)
